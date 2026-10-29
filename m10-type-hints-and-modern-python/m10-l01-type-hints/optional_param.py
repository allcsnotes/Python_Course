from typing import Optional


def greet(name: Optional[str]):
    return f"Hello, {name}"


print(greet(None))
print(greet())
