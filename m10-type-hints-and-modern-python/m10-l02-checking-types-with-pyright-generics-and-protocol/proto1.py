from dataclasses import dataclass
from typing import Protocol


class Payable(Protocol):
    def amount(self) -> int: ...


@dataclass
class Course:
    title: str
    price: int

    def amount(self) -> int:
        return self.price


@dataclass
class Bundle:
    courses: list[Course]

    def amount(self) -> int:
        return sum(c.price for c in self.courses)


@dataclass
class Student:
    name: str


def checkout(item: Payable) -> str:
    return f"Pay Rs {item.amount()}"


python = Course("Python", 999)
sql = Course("SQL Basics", 499)
print(checkout(python))
print(checkout(Bundle([python, sql])))
print(checkout(Student("Lukas")))
