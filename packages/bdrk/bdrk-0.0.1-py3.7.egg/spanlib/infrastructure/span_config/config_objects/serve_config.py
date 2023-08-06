from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ServeConfig:
    image: str
    install: List[str]
    script_commands: List[str]
