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
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=3, max_length=60)
    price: int = Field(gt=0, le=100_000)
    level: Level = Level.BEGINNER


class CourseOut(CourseIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int | None
    lessons: list[LessonOut]


class CoursePage(BaseModel):
    items: list[CourseOut]
    total: int
    limit: int
    offset: int


class StudentIn(BaseModel):
    name: str = Field(min_length=2, max_length=60)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+$")


class SignUp(StudentIn):
    model_config = ConfigDict(extra="forbid")

    password: str = Field(
        min_length=10, max_length=128, repr=False
    )


class CourseBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class StudentOut(StudentIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    courses: list[CourseBrief]


class EnrollmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    student_id: int
    course_id: int
    enrolled_on: date


class NewUser(SignUp):
    role: Literal["student", "instructor", "admin"] = "student"


class EnrollmentView(BaseModel):
    course_id: int
    title: str
    enrolled_on: date
