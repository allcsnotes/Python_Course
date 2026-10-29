from dataclasses import dataclass
from typing import TypedDict

from pydantic import BaseModel


class CourseDict(TypedDict):
    title: str
    price: int


@dataclass
class CourseData:
    title: str
    price: int


class CourseModel(BaseModel):
    title: str
    price: int
