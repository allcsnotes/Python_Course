from pydantic import BaseModel


class Course(BaseModel):
    title: str
    price: int


course = Course(title="Python Basics", price=1499)
course.price = "free"
print(course.price)
print(course.price * 2)
