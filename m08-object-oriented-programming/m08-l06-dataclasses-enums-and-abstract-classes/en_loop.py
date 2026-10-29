from enum import Enum


class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


for level in Level:
    print(level.value, level.name)
print(len(Level))
