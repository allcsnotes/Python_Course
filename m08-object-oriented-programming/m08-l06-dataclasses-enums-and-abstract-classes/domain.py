from dataclasses import dataclass, field
from enum import Enum


class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


@dataclass(frozen=True)
class Lesson:
    title: str
    minutes: int


@dataclass
class Course:
    title: str
    price: int
    level: Level = Level.BEGINNER
    lessons: list = field(default_factory=list)

    def total_minutes(self):
        return sum([x.minutes for x in self.lessons])


course = Course("Python", 2499)
course.lessons.append(Lesson("Variables", 12))
course.lessons.append(Lesson("Loops", 15))
print(course)
print(course.total_minutes())
