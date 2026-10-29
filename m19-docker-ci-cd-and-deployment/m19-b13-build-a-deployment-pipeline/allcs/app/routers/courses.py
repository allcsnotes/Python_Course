from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.db import get_or_404, get_session, save
from app.models import Course, Lesson, Student
from app.permissions import own_course, require_role
from app.schemas import (
    CourseIn,
    CourseOut,
    CoursePage,
    LessonIn,
    LessonOut,
    Level,
)

router = APIRouter(prefix="/courses", tags=["courses"])
teacher = Depends(require_role("instructor", "admin"))


@router.post("", status_code=201, response_model=CourseOut)
def create_course(
    data: CourseIn,
    session: Session = Depends(get_session),
    user: Student = teacher,
):
    values = data.model_dump(mode="json")
    course = Course(**values, owner_id=user.id)
    session.add(course)
    save(session)
    return course


@router.get("", response_model=CoursePage)
def list_courses(
    level: Level | None = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    query = select(Course)
    if level:
        query = query.where(Course.level == level.value)
    total = session.scalar(
        select(func.count()).select_from(query.subquery())
    )
    page = (
        query.options(selectinload(Course.lessons))
        .order_by(Course.id)
        .limit(limit)
        .offset(offset)
    )
    items = session.scalars(page).all()
    return CoursePage(
        items=items,  # pyright: ignore
        total=total,  # pyright: ignore
        limit=limit,
        offset=offset,
    )


@router.get("/{course_id}", response_model=CourseOut)
def read_course(
    course_id: int, session: Session = Depends(get_session)
):
    return get_or_404(session, Course, course_id)


@router.put("/{course_id}", response_model=CourseOut)
def replace_course(
    data: CourseIn,
    course: Course = Depends(own_course),
    session: Session = Depends(get_session),
):
    course.title = data.title
    course.price = data.price
    course.level = data.level.value
    save(session)
    return course


@router.delete("/{course_id}", status_code=204)
def delete_course(
    course: Course = Depends(own_course),
    session: Session = Depends(get_session),
):
    session.delete(course)
    save(session)


@router.post(
    "/{course_id}/lessons",
    status_code=201,
    response_model=LessonOut,
)
def add_lesson(
    data: LessonIn,
    course: Course = Depends(own_course),
    session: Session = Depends(get_session),
):
    lesson = Lesson(
        course_id=course.id, **data.model_dump()
    )
    session.add(lesson)
    save(session)
    return lesson
