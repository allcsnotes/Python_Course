from pydantic import BaseModel, Field, ValidationError


class Course(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    price: int = Field(gt=0, le=100000)


try:
    Course(title="Go", price=0)
except ValidationError as err:
    for e in err.errors():
        print(e["loc"][0], "->", e["msg"])
