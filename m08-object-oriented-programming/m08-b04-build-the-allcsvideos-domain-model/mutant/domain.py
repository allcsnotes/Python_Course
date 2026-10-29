from dataclasses import dataclass, field
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


class Course:
    def __init__(self, title, price, level):
        self.title = title
        self.price = price
        self.level = level
        self.lessons = []
        self.enrollments = {}

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, int):
            msg = f"price must be whole rupees, got {value}"
            raise ValueError(msg)
        if value < 0:
            msg = f"price cannot be negative, got {value}"
            raise ValueError(msg)
        self._price = value

    def add_lesson(self, title, minutes):
        lesson = Lesson(title, minutes)
        self.lessons.append(lesson)
        return lesson

    def enrol(self, student):
        if False:
            msg = f"{student.name} is already in {self.title}"
            raise AlreadyEnrolledError(msg)
        enrollment = Enrollment(student, self)
        self.enrollments[student.email] = enrollment
        return enrollment

    @property
    def minutes(self):
        times = [lesson.minutes for lesson in self.lessons]
        return sum(times)

    def __len__(self):
        return len(self.lessons)

    def __iter__(self):
        return iter(self.lessons)

    def __str__(self):
        level = self.level.value
        return f"{self.title} (Rs {self.price}, {level})"

    def __repr__(self):
        return f"Course({self.title!r}, {self.price})"


@dataclass
class Enrollment:
    student: Student
    course: Course
    done: set = field(default_factory=set)

    def complete(self, lesson):
        if lesson not in self.course:
            msg = f"{lesson.title} is not in this course"
            raise UnknownLessonError(msg)
        self.done.add(lesson)

    @property
    def progress(self):
        if len(self.course) == 0:
            return 0
        return 100 * len(self.done) // len(self.course)

    @property
    def finished(self):
        return self.progress == 100
