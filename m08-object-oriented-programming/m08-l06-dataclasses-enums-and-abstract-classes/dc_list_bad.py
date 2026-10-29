from dataclasses import dataclass


@dataclass
class Course:
    title: str
    lessons: list = []
