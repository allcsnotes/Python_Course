# Exercise 18 - Students, statuses and reports
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    ACTIVE = "active"
    PAUSED = "paused"


@dataclass(frozen=True)
class Lesson:
    title: str
    minutes: int

    def __post_init__(self):
        if self.minutes <= 0:
            raise ValueError("minutes must be positive")


@dataclass
class Student:
    name: str
    status: Status = Status.ACTIVE
    done: list = field(default_factory=list)


class Report(ABC):
    @abstractmethod
    def render(self, student):
        pass


class ShortReport(Report):
    def render(self, student):
        return f"{student.name}: {len(student.done)} lessons"


class LongReport(Report):
    def render(self, student):
        text = f"{student.name} ({student.status.value}) finished:"
        for lesson in student.done:
            text = f"{text} {lesson.title}"
        return text


asha = Student("Asha")
lukas = Student("Lukas", Status.PAUSED)
asha.done.append(Lesson("Variables", 12))
asha.done.append(Lesson("Loops", 15))

print(asha)
print(lukas)
for status in Status:
    print(status.name, status.value)
for report in [ShortReport(), LongReport()]:
    print(report.render(asha))
print(ShortReport().render(lukas))

try:
    Lesson("Empty", 0)
except ValueError as error:
    print("Rejected:", error)

try:
    Report()
except TypeError as error:
    print("TypeError:", error)
