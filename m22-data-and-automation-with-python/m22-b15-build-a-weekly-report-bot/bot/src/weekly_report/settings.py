from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_url: str = "http://localhost:8725"
    api_user: str
    api_password: SecretStr
    smtp_host: str = "localhost"
    smtp_port: int = 22525
    mail_from: str = "reports@allcsvideos.com"
    mail_to: str = "meera@allcsvideos.com"
    alert_to: str = "asha@allcsvideos.com"
    out_dir: Path = Path("out")
    timezone: str = "Asia/Kolkata"
    tries: int = 3
    wait: float = 2.0
