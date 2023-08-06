from dataclasses import dataclass
from typing import List

from spanlib.infrastructure.span_config.config_objects.command import ShellCommand


@dataclass(frozen=True)
class ServeConfig:
    image: str
    install: List[str]
    script_commands: List[ShellCommand]
