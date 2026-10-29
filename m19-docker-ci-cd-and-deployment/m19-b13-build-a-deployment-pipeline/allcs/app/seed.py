"""Create the first admin and two demo courses (safe to run twice)."""

import os

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import engine
from app.models import Course, Student
from app.security import hash_password

PASSWORD = os.environ.get(
    "SEED_ADMIN_PASSWORD", "change-me-now"
)

with Session(engine) as session:
    admin = session.scalars(
        select(Student).where(
            Student.email == "asha@example.com"
        )
    ).first()
    if admin is None:
        admin = Student(
            name="Asha",
            email="asha@example.com",
            role="admin",
            password_hash=hash_password(PASSWORD),
        )
        session.add(admin)
        session.commit()
    if session.scalars(select(Course)).first() is None:
        for title, price in [
            ("Python Basics", 499),
            ("FastAPI in Practice", 899),
        ]:
            session.add(
                Course(
                    title=title,
                    price=price,
                    level="beginner",
                    owner_id=admin.id,
                )
            )
        session.commit()
print("seed done")
