import asyncio
import csv
import io

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_session
from app.models import Course, Enrollment, Student
from app.permissions import require_role
from app.worker import export_enrollments

router = APIRouter(tags=["extras"])
admin = Depends(require_role("admin", "instructor"))


@router.get("/demo/rating/{course_id}")
async def rating(course_id: int):
    await asyncio.sleep(0.2)  # stands in for a separate ratings service
    return {"course_id": course_id, "stars": 4.5}


@router.post("/me/export/inline")
def export_inline(
    user: Student = admin, session: Session = Depends(get_session)
):
    query = (
        select(Student.name, Student.email, Course.title, Enrollment.enrolled_on)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .join(Course, Course.id == Enrollment.course_id)
    )
    out = io.StringIO()
    writer = csv.writer(out)
    for row in session.execute(query):
        writer.writerow(row)
    return {"rows": out.getvalue().count("\n")}


@router.post("/me/export", status_code=202)
def export_job(user: Student = admin):
    job = export_enrollments.delay()
    return {"job": job.id}
