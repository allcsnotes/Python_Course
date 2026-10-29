from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    minutes: int
    free: bool = False


print(Lesson("Variables", 12))
print(Lesson("Welcome", 3, True))
print(Lesson("Loops", 15, free=True))
