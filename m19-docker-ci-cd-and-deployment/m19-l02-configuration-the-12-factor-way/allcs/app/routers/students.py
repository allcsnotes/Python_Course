import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_or_404, get_session, save
from app.models import Student
from app.permissions import own_student
from app.schemas import EnrollmentView, SignUp, StudentOut
from app.security import hash_password
from app.settings import get_settings

log = logging.getLogger("allcs")
router = APIRouter(prefix="/students", tags=["students"])


@router.post("", status_code=201, response_model=StudentOut)
def sign_up(
    data: SignUp,
    session: Session = Depends(get_session),
):
    if not get_settings().signup_open:
        raise HTTPException(403, "Sign-ups are closed")
    log.debug("sign-up request for %s", data.email)
    student = Student(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    session.add(student)
    save(session)
    return student


@router.get(
    "/{student_id}/enrollments", response_model=list[EnrollmentView]
)
def list_enrollments(
    student_id: int = Depends(own_student),
    session: Session = Depends(get_session),
):
    student = get_or_404(session, Student, student_id)
    return [
        EnrollmentView(
            course_id=e.course_id,
            title=e.course.title,
            enrolled_on=e.enrolled_on,
        )
        for e in student.enrollments
    ]
