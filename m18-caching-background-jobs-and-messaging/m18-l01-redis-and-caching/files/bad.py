import redis
from pydantic import BaseModel


class Course(BaseModel):
    id: int
    title: str


r = redis.Redis(port=18401, decode_responses=True)
r.set("course:1", Course(id=1, title="Python Basics"))
