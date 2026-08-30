from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Self


class Settings(BaseSettings):
    """Application settings, loaded from environment variables and .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "sensor-analytics"
    environment: str = "local"
    log_level: str = "INFO"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sensor_analytics"
    temp_min_celsius: float = 0.0
    temp_max_celsius: float = 40.0

    @model_validator(mode="after")
    def check_threshold_order(self) -> Self:
        if self.temp_min_celsius >= self.temp_max_celsius:
            msg = "temp_min_celsius must be lower than temp_max_celsius"
            raise ValueError(msg)
        return self


@lru_cache
def get_settings() -> Settings:
    """Build Settings once per process, then return the cached instance."""
    return Settings()
