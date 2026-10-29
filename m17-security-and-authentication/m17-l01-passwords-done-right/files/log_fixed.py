import logging

from pydantic import BaseModel, Field

logging.basicConfig(level="INFO", format="%(message)s")


class SignUp(BaseModel):
    name: str
    password: str = Field(repr=False)


data = SignUp(
    name="Lukas", password="Monsoon-Chai-Lamp-84"
)
logging.info("new sign up: %s", data)
