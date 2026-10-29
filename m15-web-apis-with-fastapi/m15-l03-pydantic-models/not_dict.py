from pydantic import BaseModel


class Course(BaseModel):
    title: str
    price: int


course = Course(title="Python Basics", price=1499)
print(course["title"])
