from pydantic import BaseModel


class Course(BaseModel):
    title: str
    price: int
    level: str = "beginner"


one = Course(title="Python Basics", price=1499)
print(one)
print(one.title, one.price)

two = Course(title="Pydantic", price="1499")
print(two.price, type(two.price))
