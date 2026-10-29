from typing import TypedDict


class CourseData(TypedDict):
    title: str
    price: int


data = {"title": "SQL", "price": 999}
print(isinstance(data, dict))
print(isinstance(data, CourseData))
