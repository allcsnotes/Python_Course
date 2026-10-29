from dataclasses import dataclass


@dataclass(frozen=True)
class Lesson:
    title: str
    minutes: int


done = {
    Lesson("Variables", 12),
    Lesson("Loops", 15),
    Lesson("Variables", 12),
}
print(len(done))
