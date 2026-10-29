from typing import TypeVar

T = TypeVar("T")


def first(items: list[T]) -> T:
    return items[0]


reveal_type(first(["Python", "SQL Basics"]))
print(first([999, 499]))
