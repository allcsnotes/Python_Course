from dataclasses import dataclass


@dataclass(slots=True)
class Course:
    title: str
    price: int


course = Course("Python Basics", 1499)
try:
    course.pirce = 999
except AttributeError as error:
    print("error:", error)
try:
    print(vars(course))
except TypeError as error:
    print("error:", error)
