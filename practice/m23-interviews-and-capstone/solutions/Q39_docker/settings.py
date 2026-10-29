from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost/dev"
    debug: bool = False
    workers: int = 2


settings = Settings()
print(settings)
