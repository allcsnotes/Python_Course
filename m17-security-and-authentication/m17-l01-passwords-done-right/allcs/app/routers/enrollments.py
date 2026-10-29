from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_or_404, get_session, save
from app.models import Course, Enrollment, Student
from app.schemas import EnrollmentIn, EnrollmentOut

router = APIRouter(
    prefix="/courses/{course_id}/enrollments", tags=["enrollments"]
)


@router.post("", status_code=201, response_model=EnrollmentOut)
def enroll(
    course_id: int,
    data: EnrollmentIn,
    session: Session = Depends(get_session),
):
    get_or_404(session, Course, course_id)
    get_or_404(session, Student, data.student_id)
    enrollment = Enrollment(
        student_id=data.student_id, course_id=course_id
    )
    session.add(enrollment)
    save(session)
    return enrollment
