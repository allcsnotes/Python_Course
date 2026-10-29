from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import hasher
from app.deps import get_current_user
from app.db import get_or_404, get_session, save
from app.domain import NotFound
from app.models import Student
from app.schemas import EnrollmentView, SignUp, StudentOut

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", status_code=201, response_model=StudentOut)
def sign_up(
    data: SignUp, session: Session = Depends(get_session)
):
    values = data.model_dump(exclude={"password"})
    student = Student(
        **values, password_hash=hasher.hash(data.password)
    )
    session.add(student)
    save(session)
    return student


@router.get(
    "/{student_id}/enrollments", response_model=list[EnrollmentView]
)
def list_enrollments(
    student_id: int,
    user: Student = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if user.id != student_id and user.role != "admin":
        raise NotFound("Student", student_id)
    student = get_or_404(session, Student, student_id)
    return [
        EnrollmentView(
            student=student.email,
            course_id=e.course_id,
            title=e.course.title,
            enrolled_on=e.enrolled_on,
        )
        for e in student.enrollments
    ]
