from enum import Enum


class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


level = Level.BEGINNER
print(level)
print(level.name)
print(level.value)
print(Level(2))
print(Level["ADVANCED"])
