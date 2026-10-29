from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    minutes: int


lesson = Lesson("Variables", "twelve")
print(lesson)
