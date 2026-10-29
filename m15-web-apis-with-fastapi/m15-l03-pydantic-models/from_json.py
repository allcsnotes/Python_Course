from pydantic import BaseModel, ValidationError


class Course(BaseModel):
    title: str
    price: int


text = '{"title": "Pydantic", "price": 999}'
print(Course.model_validate_json(text))

data = {"title": "Pydantic", "price": 999.5}
try:
    Course.model_validate(data)
except ValidationError as err:
    print(err.errors()[0]["msg"])
