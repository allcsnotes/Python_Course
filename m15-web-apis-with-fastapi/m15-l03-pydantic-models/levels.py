from enum import Enum

from pydantic import BaseModel


class Level(Enum):
    BEGINNER = "beginner"
    ADVANCED = "advanced"


class Course(BaseModel):
    title: str
    price: int
    level: Level = Level.BEGINNER
