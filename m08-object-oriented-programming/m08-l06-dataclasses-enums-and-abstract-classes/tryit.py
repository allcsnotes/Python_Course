from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    ACTIVE = "active"
    PAUSED = "paused"


@dataclass
class Student:
    name: str
    status: Status = Status.ACTIVE
    courses: list = field(default_factory=list)


class Report(ABC):
    @abstractmethod
    def render(self, student):
        pass


class ShortReport(Report):
    def render(self, student):
        return f"{student.name} -> {student.courses}"


asha = Student("Asha")
asha.courses.append("Python")
for status in Status:
    print(status.name, status.value)
print(ShortReport().render(asha))
print(asha)
