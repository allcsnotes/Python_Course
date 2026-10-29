import math


def greet(name):
    return f"Hello, {name}"


class Course:
    pass


things = [
    1999, 0.75, "Lukas", None,
    greet, Course, math, len, type,
]
for thing in things:
    print(type(thing).__name__)
