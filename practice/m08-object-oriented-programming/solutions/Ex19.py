# Exercise 19 - Predict the output (dataclass and Enum)
from dataclasses import dataclass
from enum import Enum


class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


@dataclass
class Lesson:
    title: str
    minutes: int
    free: bool = False


print(Lesson("Variables", 12))
print(Lesson("Welcome", 3, True))
a = Lesson("Loops", 15, free=True)
b = Lesson("Loops", 15, True)
print(a == b, a is b)
a.minutes = 20
print(a == b, a)

try:
    done = {a, b}
except TypeError as error:
    print("TypeError:", error)

level = Level.INTERMEDIATE
print(level)
print(level.name, level.value)
print(Level(3), Level["BEGINNER"])
for item in Level:
    print(item.value, item.name)
print(len(Level))
print(level == Level.INTERMEDIATE, level == 2)

try:
    print(Level.BEGINNER < Level.ADVANCED)
except TypeError as error:
    print("TypeError:", error)

try:
    print(Level(9))
except ValueError as error:
    print("ValueError:", error)
