import os

from pydantic_settings import BaseSettings


class Flags(BaseSettings):
    signup_open: bool = True


os.environ["SIGNUP_OPEN"] = "false"
print("plain:", bool(os.environ["SIGNUP_OPEN"]))
print("Settings:", Flags().signup_open)
