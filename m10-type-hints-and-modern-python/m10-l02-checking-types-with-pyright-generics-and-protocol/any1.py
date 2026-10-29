from typing import Any


def read_price(course: Any) -> int:
    return course.price


print(read_price("Python"))
