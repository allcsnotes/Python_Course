from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ALLCS_")

    app_name: str = "allcsvideos"
    page_size: int = 20
    debug: bool = False
    secret_key: SecretStr


settings = Settings()
print(settings.app_name, settings.page_size, settings.debug)
print(settings.secret_key)
