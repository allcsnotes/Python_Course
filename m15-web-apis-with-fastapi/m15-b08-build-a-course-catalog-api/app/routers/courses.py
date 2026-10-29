from fastapi import APIRouter, Depends, Query

from app.deps import get_store
from app.models import Course, CourseIn, CoursePage, Level
from app.store import CourseStore

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("", status_code=201, response_model=Course)
def create_course(
    data: CourseIn, store: CourseStore = Depends(get_store)
):
    return store.create(data)


@router.get("", response_model=CoursePage)
def list_courses(
    level: Level | None = None,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    store: CourseStore = Depends(get_store),
):
    found = store.find_all(level)
    page = found[offset : offset + limit]
    return CoursePage(
        items=page, total=len(found), limit=limit, offset=offset
    )


@router.get("/{course_id}", response_model=Course)
def read_course(
    course_id: int, store: CourseStore = Depends(get_store)
):
    return store.get(course_id)


@router.put("/{course_id}", response_model=Course)
def replace_course(
    course_id: int,
    data: CourseIn,
    store: CourseStore = Depends(get_store),
):
    return store.replace(course_id, data)


@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: int, store: CourseStore = Depends(get_store)
):
    store.delete(course_id)
