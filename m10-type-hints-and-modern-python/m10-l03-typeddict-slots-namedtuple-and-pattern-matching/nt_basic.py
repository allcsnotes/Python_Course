from typing import NamedTuple


class Course(NamedTuple):
    title: str
    price: int
    level: str = "beginner"


course = Course("Python Basics", 1499)
print(course)
print(course.price, course[1])
title, price, level = course
print(title, level)
