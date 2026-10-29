from pydantic import BaseModel, ConfigDict, ValidationError


class Course(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    title: str
    price: int


course = Course(title="Python Basics", price=1499)
try:
    course.price = "free"
except ValidationError as err:
    print(err.errors()[0]["msg"])
print(course.price)
