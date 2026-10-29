from pydantic import BaseModel, Field


class Instructor(BaseModel):
    name: str
    email: str


class Lesson(BaseModel):
    title: str
    minutes: int = Field(gt=0)


class Course(BaseModel):
    title: str
    instructor: Instructor
    lessons: list[Lesson] = []
