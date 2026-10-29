from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
courses = []


class CourseIn(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    price: int = Field(gt=0)


@app.post("/courses", status_code=201)
def add_course(course: CourseIn):
    courses.append(course)
    return course
