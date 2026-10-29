from dataclasses import dataclass
from enum import Enum


class Level(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class DomainError(Exception):
    pass


class AlreadyEnrolledError(DomainError):
    pass


class UnknownLessonError(DomainError):
    pass


@dataclass(frozen=True)
class Lesson:
    title: str
    minutes: int

    def __post_init__(self):
        if self.minutes < 1:
            raise ValueError("minutes must be positive")


@dataclass(frozen=True)
class Student:
    name: str
    email: str

    def __post_init__(self):
        if "@" not in self.email:
            raise ValueError("email needs an @ sign")
