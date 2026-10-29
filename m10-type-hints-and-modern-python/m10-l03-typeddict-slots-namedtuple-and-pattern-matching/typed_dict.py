from typing import TypedDict


class CourseData(TypedDict):
    title: str
    price: int
    level: str


def show(course: CourseData) -> str:
    return f"{course['title']} costs Rs {course['price']}"


data: CourseData = {
    "title": "Python Basics",
    "price": 1499,
    "level": "beginner",
}
print(show(data))
print(type(data))
