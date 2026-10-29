from typing import NamedTuple


class Course(NamedTuple):
    title: str
    price: int


course = Course("Python Basics", 1499)
try:
    course.price = 999
except AttributeError as error:
    print("error:", error)
cheaper = course._replace(price=999)
print(course.price, cheaper.price)
print(cheaper._asdict())
