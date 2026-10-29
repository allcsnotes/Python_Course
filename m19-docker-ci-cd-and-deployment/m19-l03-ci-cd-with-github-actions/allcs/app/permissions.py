from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_or_404, get_session
from app.deps import get_current_user
from app.domain import NotFound
from app.models import Course, Student


def require_role(*allowed):
    def check(user: Student = Depends(get_current_user)):
        if user.role not in allowed:
            raise HTTPException(
                403, "Your role may not do this"
            )
        return user

    return check


def own_student(
    student_id: int,
    user: Student = Depends(get_current_user),
):
    if user.id != student_id and user.role != "admin":
        raise NotFound("Student", student_id)
    return student_id


def own_course(
    course_id: int,
    session: Session = Depends(get_session),
    user: Student = Depends(
        require_role("instructor", "admin")
    ),
):
    course = get_or_404(session, Course, course_id)
    if user.role != "admin" and course.owner_id != user.id:
        raise HTTPException(403, "This is not your course")
    return course
