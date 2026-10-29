from functools import lru_cache

from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    database_url: PostgresDsn
    redis_url: RedisDsn
    secret_key: SecretStr
    access_minutes: int = 30
    search_limit: int = 20
    cache_seconds: int = 300
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    mail_from: str = "copilot@allcsvideos.com"
    log_level: str = "INFO"


@lru_cache
def get_settings():
    return Settings()  # pyright: ignore
