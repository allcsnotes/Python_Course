from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    minutes: int
    free: bool


lesson = Lesson("Variables", 12, True)
print(lesson)
print(lesson == Lesson("Variables", 12, True))
