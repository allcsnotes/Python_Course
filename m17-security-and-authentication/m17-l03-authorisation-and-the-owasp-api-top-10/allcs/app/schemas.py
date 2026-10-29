from datetime import date
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Level(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class LessonIn(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    position: int = Field(ge=1)


class LessonOut(LessonIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CourseIn(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    price: int = Field(gt=0, le=100_000)
    level: Level = Level.BEGINNER


class CourseOut(CourseIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    lessons: list[LessonOut]


class CoursePage(BaseModel):
    items: list[CourseOut]
    total: int
    limit: int
    offset: int


class SignUp(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=2, max_length=60)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+$")
    password: str = Field(min_length=8, max_length=100)


class NewUser(SignUp):
    role: Literal["student", "instructor", "admin"] = "student"


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    role: str


class EnrollmentView(BaseModel):
    student: str
    course_id: int
    title: str
    enrolled_on: date


class EnrollmentIn(BaseModel):
    student_id: int


class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    student_id: int
    course_id: int
    enrolled_on: date
