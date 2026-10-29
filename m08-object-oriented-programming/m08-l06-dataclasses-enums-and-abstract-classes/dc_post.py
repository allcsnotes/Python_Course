from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    minutes: int

    def __post_init__(self):
        if self.minutes <= 0:
            raise ValueError("minutes must be positive")


print(Lesson("Variables", 12))
print(Lesson("Empty", 0))
