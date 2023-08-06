from typing import Dict, List

from spanlib.infrastructure.span_config.base_mapper.base_mapper import BaseMapper
from spanlib.infrastructure.span_config.config_objects import ServeConfig
from spanlib.utils.common import as_dataclass


class V1ServeConfigMapper(BaseMapper):
    @staticmethod
    def create_config_object(config_dict) -> ServeConfig:
        mapper = V1ServeConfigMapper(config_dict)
        return as_dataclass(mapper, ServeConfig, install=mapper.install_commands)

    def __init__(self, config_dict: Dict):
        self.config_dict = config_dict

    @property
    def install_commands(self) -> List[str]:
        return self.config_dict.get("install", [])

    @property
    def script_commands(self) -> List[str]:
        return self.config_dict["script"]

    @property
    def image(self) -> str:
        return self.config_dict.get("image", "scratch")
