import asyncio
import dataclasses
import inspect
import random
import time
from contextlib import AbstractContextManager
from enum import Enum
from functools import wraps
from typing import Any, Callable, Tuple, Type, TypeVar, Union

from spanlib.common.exceptions import DataClassConversionError

T = TypeVar("T")

# Decorators to preserve function signature using this pattern:
# https://github.com/python/mypy/issues/1927
FuncT = TypeVar("FuncT", bound=Callable[..., Any])


class reraise(AbstractContextManager):
    """
    Context manager to reraise one exception from another
    """

    def __init__(self, exc_a: Type[Exception], exc_b: Type[Exception], **kwargs):
        self.exc_a = exc_a
        self.exc_b = exc_b
        self.kwargs = kwargs

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type and issubclass(exc_type, self.exc_a):
            raise self.exc_b(**self.kwargs) from exc_value

    def __call__(self, func: FuncT) -> FuncT:
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_decorated(*args, **kwargs):
                with self:
                    return await func(*args, **kwargs)

            return async_decorated  # type: ignore

        @wraps(func)
        def decorated(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return decorated  # type: ignore


def retry_on_exception(  # noqa: C901
    exc: Union[Exception, Type[Exception]], wait: int, tries: int
):
    """
    Decorator to retry a function if an exception `exc` occurs.
    :param exc: Exception to catch.
    :param wait: Random wait between 0 and `wait` seconds between retries.
    :param tries: Number of retries. Set to -1 for infinite retries.
    """

    def decorator(func: FuncT) -> FuncT:
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def async_decorated(*args, **kwargs):
                attempt = tries
                while attempt != 0:
                    attempt -= 1
                    try:
                        return await func(*args, **kwargs)
                    except exc:
                        if attempt == 0:
                            raise exc
                    if wait:
                        await asyncio.sleep(random.random() * wait)

            return async_decorated  # type: ignore

        @wraps(func)
        def decorated(*args, **kwargs):
            attempt = tries
            while attempt != 0:
                attempt -= 1
                try:
                    return func(*args, **kwargs)
                except exc:
                    if attempt == 0:
                        raise exc
                if wait:
                    time.sleep(random.random() * wait)

        return decorated  # type: ignore

    return decorator


def as_dataclass(obj: Any, dataclass_: Type[T], **kwargs) -> T:
    """Cast object to a dataclass

    :param Any obj: Object to cast
    :param Type[T] dataclass_: Target dataclass
    :param kwargs: Fields => override values; will not override fields of nested dataclasses
    :raises DataClassConversionError: Failed to convert object to given type
    :return T: Casted object

    FIXME: [BDRK-326] Convert to an iterative solution to avoid stack overflow.
    FIXME: [BDRK-327] mypy complains that `cast_type` is being fed too many arguments
    """

    if not dataclasses.is_dataclass(dataclass_):
        raise DataClassConversionError(
            f"as_dataclass: Attempted to convert object {obj} to non-dataclass type {dataclass_}"
        )

    try:
        return dataclass_(  # type: ignore
            **{
                field.name: _cast_dataclass_field_value(
                    obj=obj, field_name=field.name, field_type=field.type, **kwargs
                )
                for field in dataclasses.fields(dataclass_)
            }
        )
    except DataClassConversionError as ex:
        raise DataClassConversionError(
            f"as_dataclass: Could not convert object={obj} to type={dataclass_} "
            f"with kwargs={kwargs}"
        ) from ex


def _cast_dataclass_field_value(  # noqa: C901 -- Too complex
    obj: Any, field_name: str, field_type: Type[T], **kwargs
) -> T:
    """Helper function to convert an object's field with some given name to the given type.

    Notes on conversion:
    - If field_type is a Dataclass, conversion uses duck typing by recursing on the field.
    - If field_type is an enum, conversion succeeds if the enum object can be initialised using
      the field value.
    - If field_type is a Union, conversion is attempted for each of the type parameters,
      in the same order as the Union definition (nested Unions are flattened). The first
      successful conversion is returned.
    - If field_type is some other Generic (e.g. List[T], Dict[T, U]), type parameters are not
      checked, and the field is returned if it matches the origin type (e.g. List, Dict
      respectively) using isinstance().
    - For other field_types, conversion succeeds if isinstance(value, field_type) is True.
    - kwarg overrides are type checked against field_type.

    :param Any obj: Object to cast
    :param str field_name: Field name
    :param Type[T] field_type: Field type
    :param kwargs: Fields => override values; will not override fields of nested dataclasses
    :raises DataClassConversionError: Failed to convert field to given type
    :return T: Casted object
    """
    types_to_check = _get_types_to_check(field_type)

    # Try to get the value from the object
    if isinstance(obj, dict):
        field_value = obj.get(field_name, None)
    else:
        field_value = getattr(obj, field_name, None)
    # Replace it with kwargs if it is present
    field_value = kwargs.get(field_name, field_value)

    for possible_type in types_to_check:
        if dataclasses.is_dataclass(possible_type):
            try:
                return as_dataclass(field_value, possible_type)
            except DataClassConversionError:
                continue
        elif inspect.isclass(possible_type) and issubclass(possible_type, Enum):
            try:
                return possible_type(field_value)  # type: ignore
            except ValueError:
                continue
        elif isinstance(field_value, possible_type):
            return field_value
    else:
        value_type = type(field_value)
        dict_repr = None
        if hasattr(obj, "__dict__"):
            dict_repr = obj.__dict__

        raise DataClassConversionError(
            f"as_dataclass: Could not match any types for from_object=({obj}, {dict_repr}). "
            f"field={field_name} with value={field_value} of type={value_type} could not "
            f"be converted to target_type={field_type} which can be one of "
            f"types_to_check={types_to_check}"
        )


def _get_types_to_check(field_type: Type) -> Tuple[Type, ...]:
    """Helper function to get ordered tuple of types to check for as_dataclass()
       field conversion.
    """
    # NOTE: __origin__ is the best way to get the original type for now:
    # https://github.com/python/typing/issues/136#issuecomment-138392956
    if hasattr(field_type, "__origin__"):  # field_type is a template
        if field_type.__origin__ == Union:
            # Return all union types (flattened with sum())
            return sum((_get_types_to_check(t) for t in field_type.__args__), ())

        # field_type is some other generic, incl. List, Dict, etc.
        return (field_type.__origin__,)

    return (field_type,)
