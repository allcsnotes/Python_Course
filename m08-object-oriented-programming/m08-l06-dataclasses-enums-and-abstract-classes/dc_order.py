from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    free: bool = False
    minutes: int
