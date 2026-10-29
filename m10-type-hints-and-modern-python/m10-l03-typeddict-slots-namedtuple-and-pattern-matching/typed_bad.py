from typing import TypedDict


class CourseData(TypedDict):
    title: str
    price: int
    level: str


def show(course: CourseData) -> str:
    return f"{course['title']} costs Rs {course['pirce']}"


data: CourseData = {
    "title": "Python Basics",
    "price": "free",
    "level": "beginner",
}
print(show(data))
