from dataclasses import dataclass

from toolkit import cache_for


@dataclass
class User:
    name: str


@cache_for(10)
def greeting(user):
    return f"Welcome back, {user.name}"


print(greeting(User("Priya")))
