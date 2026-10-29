from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import aggregate_order_by
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Course, Enrollment, Student
from app.permissions import require_role

router = APIRouter(tags=["dashboard"])
teacher = Depends(require_role("instructor", "admin"))


@router.get("/me/dashboard")
def dashboard(
    user: Student = teacher,
    session: Session = Depends(get_session),
):
    first = aggregate_order_by(Student.name, Student.id)
    names = func.array_agg(first)
    query = (
        select(Course.title, Course.price, func.count(), names)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .join(Student, Student.id == Enrollment.student_id)
        .where(Course.owner_id == user.id)
        .group_by(Course.id)
        .order_by(Course.id)
    )
    return [
        {
            "course": title,
            "students": count,
            "revenue": price * count,
            "first_three": firsts[:3],
        }
        for title, price, count, firsts in session.execute(query)
    ]
