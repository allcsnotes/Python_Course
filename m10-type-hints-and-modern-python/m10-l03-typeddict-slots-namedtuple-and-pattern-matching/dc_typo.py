from dataclasses import dataclass


@dataclass
class Course:
    title: str
    price: int


course = Course("Python Basics", 1499)
course.pirce = 999
print(course.price)
print(vars(course))
