from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

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
    mine = select(Course).where(Course.owner_id == user.id)
    report = []
    for course in session.scalars(mine).all():
        query = (
            select(Enrollment)
            .where(Enrollment.course_id == course.id)
            .options(selectinload(Enrollment.student))
        )
        rows = session.scalars(query).all()
        names = [row.student.name for row in rows]
        report.append(
            {
                "course": course.title,
                "students": len(names),
                "revenue": course.price * len(names),
                "first_three": names[:3],
            }
        )
    return report
