from pydantic import FilePath
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mapproxy_config_path: FilePath
    mapproxy_context_path: str
    mapproxy_app_title: str
    debug: bool

    class Config:
        env_file = ".env_mapproxy"
        env_file_encoding = "utf-8"
