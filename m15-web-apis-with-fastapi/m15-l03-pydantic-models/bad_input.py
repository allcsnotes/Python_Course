from pydantic import BaseModel, ValidationError


class Course(BaseModel):
    title: str
    price: int


try:
    Course(price="free")
except ValidationError as err:
    print(err.error_count(), "problems")
    for e in err.errors():
        print(e["loc"], e["msg"])
        print("  type:", e["type"], " input:", e["input"])
