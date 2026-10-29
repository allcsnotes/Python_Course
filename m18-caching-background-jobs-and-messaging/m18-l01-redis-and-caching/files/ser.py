import redis
from pydantic import BaseModel


class Course(BaseModel):
    id: int
    title: str
    price: int


r = redis.Redis(port=18401, decode_responses=True)
course = Course(id=1, title="Python Basics", price=499)

r.set("course:1", course.model_dump_json())
text = r.get("course:1")
print(text)
print(Course.model_validate_json(text))
