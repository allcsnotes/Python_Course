from enum import Enum


class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


level = Level.BEGINNER
print(level == Level.BEGINNER)
print(level == 1)
print(Level.BEGINNER.value < Level.ADVANCED.value)
print(Level.BEGINNER < Level.ADVANCED)
