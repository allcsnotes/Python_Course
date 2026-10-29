from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    minutes: int


done = {Lesson("Variables", 12)}
print(len(done))
