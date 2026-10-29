from enum import Enum

from pydantic import BaseModel, Field


class Level(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class CourseIn(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    price: int = Field(gt=0, le=100_000)
    level: Level = Level.BEGINNER


class Course(CourseIn):
    id: int


class CoursePage(BaseModel):
    items: list[Course]
    total: int
    limit: int
    offset: int
