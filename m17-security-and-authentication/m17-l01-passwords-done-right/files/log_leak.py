import logging

from pydantic import BaseModel

logging.basicConfig(level="INFO", format="%(message)s")


class SignUp(BaseModel):
    name: str
    password: str


data = SignUp(
    name="Lukas", password="Monsoon-Chai-Lamp-84"
)
logging.info("new sign up: %s", data)
