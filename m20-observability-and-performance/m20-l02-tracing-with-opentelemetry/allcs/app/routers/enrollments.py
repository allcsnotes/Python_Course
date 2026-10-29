import logging

from fastapi import APIRouter, Depends
from opentelemetry import trace
from sqlalchemy.orm import Session

from app.cache import r
from app.db import get_or_404, get_session, save
from app.deps import get_current_user
from app.models import Course, Enrollment, Student
from app.schemas import EnrollmentOut
from app.worker import send_welcome_email

log = logging.getLogger("allcs.enroll")
tracer = trace.get_tracer("allcs.enroll")

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
    with tracer.start_as_current_span("course.title") as span:
        key = f"course:{course_id}:title"
        title = r.get(key)
        span.set_attribute("cache.hit", title is not None)
        if title is None:
            course = get_or_404(session, Course, course_id)
            title = course.title
            r.set(key, title, ex=60)
    enrollment = Enrollment(
        student_id=user.id, course_id=course_id
    )
    session.add(enrollment)
    save(session)
    send_welcome_email.delay(
        student_id=user.id,
        course_id=course_id,
        name=user.name,
        email=user.email,
        title=title,
    )
    log.info(
        "student %s enrolled in course %s", user.id, course_id
    )
    return enrollment
