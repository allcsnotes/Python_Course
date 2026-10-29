from fastapi import APIRouter, Depends

from app.main import get_store
from app.store import Store

router = APIRouter(prefix="/courses")


@router.get("")
def list_courses(store: Store = Depends(get_store)):
    return list(store.courses.values())
