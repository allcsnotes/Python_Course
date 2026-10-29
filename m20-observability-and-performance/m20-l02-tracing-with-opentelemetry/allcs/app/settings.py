from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import (
    Field,
    PostgresDsn,
    RedisDsn,
    SecretStr,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

SECRETS = Path("/run/secrets")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        secrets_dir=SECRETS if SECRETS.is_dir() else None,
        extra="ignore",
    )

    environment: Literal["dev", "test", "prod"] = "dev"
    database_url: PostgresDsn
    redis_url: RedisDsn
    secret_key: SecretStr = Field(min_length=16)
    access_seconds: int = Field(900, gt=0)
    smtp_host: str = "localhost"
    smtp_port: int = 18625
    signup_open: bool = True
    pool_size: int = Field(5, gt=0)
    max_overflow: int = Field(10, ge=0)
    app_version: str = "1"
    log_level: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR"
    ] = "INFO"

    @model_validator(mode="after")
    def quiet_prod(self):
        if self.environment == "prod" and self.log_level == "DEBUG":
            raise ValueError("prod must not log at DEBUG")
        return self


@lru_cache
def get_settings():
    return Settings()
