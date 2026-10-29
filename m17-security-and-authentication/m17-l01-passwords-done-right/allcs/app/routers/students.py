from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_or_404, get_session, save
from app.domain import NotFound
from app.models import Enrollment, Student
from app.schemas import SignUp, StudentOut
from app.security import hash_password

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", status_code=201, response_model=StudentOut)
def sign_up(
    data: SignUp, session: Session = Depends(get_session)
):
    student = Student(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    session.add(student)
    save(session)
    return student


@router.get("/{student_id}", response_model=StudentOut)
def read_student(
    student_id: int, session: Session = Depends(get_session)
):
    query = select(Student).where(Student.id == student_id)
    query = query.options(
        selectinload(Student.enrollments).selectinload(
            Enrollment.course
        )
    )
    student = session.scalars(query).first()
    if student is None:
        raise NotFound("Student", student_id)
    return student
