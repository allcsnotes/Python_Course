from fastapi import APIRouter

router = APIRouter(prefix="/students", tags=["students"])

STUDENTS = ["Lukas", "Priya"]


@router.get("")
def list_students():
    return STUDENTS
