from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hasher
from app.db import get_session, save
from app.models import Student
from app.permissions import require_role
from app.schemas import NewUser, StudentOut

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_role("admin"))],
)


@router.get("/students", response_model=list[StudentOut])
def all_students(session: Session = Depends(get_session)):
    query = select(Student).order_by(Student.id)
    return session.scalars(query).all()


@router.post(
    "/students", status_code=201, response_model=StudentOut
)
def create_user(
    data: NewUser, session: Session = Depends(get_session)
):
    values = data.model_dump(exclude={"password"})
    student = Student(
        **values, password_hash=hasher.hash(data.password)
    )
    session.add(student)
    save(session)
    return student
