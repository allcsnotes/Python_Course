from app.worker import send_welcome_email
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_or_404, get_session, save
from app.deps import get_current_user
from app.models import Course, Enrollment, Student
from app.schemas import EnrollmentOut

router = APIRouter(
    prefix="/courses/{course_id}/enrollments",
    tags=["enrollments"],
)


@router.post(
    "", status_code=201, response_model=EnrollmentOut
)
def enroll(
    course_id: int,
    user: Student = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    course = get_or_404(session, Course, course_id)
    enrollment = Enrollment(
        student_id=user.id,
        course_id=course_id,
        amount=course.price,
    )
    session.add(enrollment)
    save(session)
    send_welcome_email.delay(
        student_id=user.id,
        course_id=course_id,
        name=user.name,
        email=user.email,
        title=course.title,
    )
    return enrollment
