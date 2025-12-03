from pydantic_settings import BaseSettings, SettingsConfigDict

from .broker import BrokerSettings
from .database import DatabaseSettings


class Settings(BaseSettings):
    database: DatabaseSettings = None
    broker: BrokerSettings = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="allow",
    )


settings = Settings()
