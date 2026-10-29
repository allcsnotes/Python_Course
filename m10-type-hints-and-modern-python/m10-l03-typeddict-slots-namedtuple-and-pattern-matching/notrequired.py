from typing import NotRequired, TypedDict


class CourseData(TypedDict):
    title: str
    price: int
    note: NotRequired[str]


a: CourseData = {"title": "Python Basics", "price": 1499}
b: CourseData = {"title": "SQL", "price": 999, "note": "new"}
for course in (a, b):
    print(course["title"], course.get("note", "no note"))
