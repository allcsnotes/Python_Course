# Q14 - Does Python check type hints?
from pydantic import TypeAdapter, ValidationError


def double(x: int) -> int:
    return x * 2

print(double("ha"))                 # no error: Python ignores hints while running
print(double.__annotations__)       # they are just stored

try:                                # pydantic USES hints, at run time
    TypeAdapter(int).validate_python("abc")
except ValidationError as error:
    print("pydantic:", error.errors()[0]["msg"])

print(TypeAdapter(int).validate_python("42") + 1)   # and converts safe text for you
