from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    title: str
    minutes: int


lesson = Lesson("Variables", 12)
print(lesson)
lesson.minutes = 15
