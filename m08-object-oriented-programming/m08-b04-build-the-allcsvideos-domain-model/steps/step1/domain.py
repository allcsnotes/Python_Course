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
