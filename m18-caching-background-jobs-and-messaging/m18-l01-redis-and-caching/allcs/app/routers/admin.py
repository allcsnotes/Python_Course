from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_session, save
from app.models import Enrollment, Student
from app.permissions import require_role
from app.schemas import NewUser, StudentOut
from app.security import hash_password

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_role("admin"))],
)


@router.post("/students", status_code=201, response_model=StudentOut)
def create_user(
    data: NewUser, session: Session = Depends(get_session)
):
    student = Student(
        name=data.name,
        email=data.email,
        role=data.role,
        password_hash=hash_password(data.password),
    )
    session.add(student)
    save(session)
    return student


@router.get("/students", response_model=list[StudentOut])
def list_students(session: Session = Depends(get_session)):
    query = select(Student).order_by(Student.id)
    query = query.options(
        selectinload(Student.enrollments).selectinload(
            Enrollment.course
        )
    )
    return session.scalars(query).all()
