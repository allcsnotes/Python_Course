from collections.abc import Iterator

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine, show_sql
from models import Course

show_sql()
app = FastAPI()


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


class CourseIn(BaseModel):
    title: str
    price: int
    level: str


class CourseOut(CourseIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


@app.get("/courses", response_model=list[CourseOut])
def list_courses(session: Session = Depends(get_session)):
    stmt = select(Course).order_by(Course.id)
    return session.scalars(stmt).all()


@app.get("/courses/{course_id}", response_model=CourseOut)
def get_course(
    course_id: int, session: Session = Depends(get_session)
):
    course = session.get(Course, course_id)
    if course is None:
        raise HTTPException(404, "Course not found")
    return course


@app.post("/courses", response_model=CourseOut, status_code=201)
def add_course(
    data: CourseIn, session: Session = Depends(get_session)
):
    course = Course(**data.model_dump())
    session.add(course)
    session.commit()
    return course
