from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_store
from app.store import Store

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("")
def list_courses(store: Store = Depends(get_store)):
    return list(store.courses.values())


@router.get("/{course_id}")
def get_course(
    course_id: int, store: Store = Depends(get_store)
):
    if course_id not in store.courses:
        raise HTTPException(404, "Course not found")
    return store.courses[course_id]
