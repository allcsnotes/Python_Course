import json
from datetime import datetime

from app.worker import DEAD, redis, send_welcome_email
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_session, save
from app.models import Course, Enrollment, Student
from app.permissions import require_role
from app.schemas import NewUser, StudentOut
from app.security import hash_password

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_role("admin"))],
)


@router.post(
    "/students", status_code=201, response_model=StudentOut
)
def create_user(
    data: NewUser, session: Session = Depends(get_session)
):
    student = Student(
        name=data.name,
        email=data.email,
        role=data.role,
        password_hash=hash_password(data.password),
    )
    session.add(student)
    save(session)
    return student


@router.get("/students", response_model=list[StudentOut])
def list_students(session: Session = Depends(get_session)):
    query = select(Student).order_by(Student.id)
    query = query.options(
        selectinload(Student.enrollments).selectinload(
            Enrollment.course
        )
    )
    return session.scalars(query).all()


@router.get("/dead-letters")
def list_dead_letters():
    return [
        json.loads(raw) for raw in redis.lrange(DEAD, 0, -1)
    ]


@router.post("/dead-letters/replay")
def replay_dead_letters():
    count = 0
    while True:
        raw = redis.rpop(DEAD)
        if raw is None:
            break
        send_welcome_email.delay(
            **json.loads(raw)["kwargs"]
        )
        count += 1
    return {"replayed": count}


@router.get("/report")
def report(start: datetime, end: datetime, session: Session = Depends(get_session)):
    """Enrollments made, and refunds paid, in [start, end)."""
    def rows(column):
        query = (
            select(Enrollment, Course.title)
            .join(Course, Course.id == Enrollment.course_id)
            .where(column >= start, column < end)
            .order_by(column)
        )
        return [
            {
                "student_id": e.student_id,
                "course_id": e.course_id,
                "course": title,
                "amount": e.amount,
                "enrolled_at": e.enrolled_at.isoformat(),
                "refunded_at": e.refunded_at.isoformat() if e.refunded_at else None,
            }
            for e, title in session.execute(query)
        ]

    return {
        "enrollments": rows(Enrollment.enrolled_at),
        "refunds": rows(Enrollment.refunded_at),
    }
