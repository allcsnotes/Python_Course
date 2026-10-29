from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    minutes: int


lesson = Lesson(minutes=12, title="Variables")
print(lesson)
lesson.minutes = 15
print(lesson.minutes)
print(lesson == Lesson("Variables", 12))
