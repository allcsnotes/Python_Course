import json
from typing import TypedDict


class CourseData(TypedDict):
    title: str
    price: int


text = '{"title": "Python Basics", "price": "free"}'
course: CourseData = json.loads(text)
print(course["price"] + 100)
