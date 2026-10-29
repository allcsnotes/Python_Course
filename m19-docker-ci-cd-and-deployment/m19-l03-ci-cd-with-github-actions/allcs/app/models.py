from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    func,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db import Base


class Course(Base):
    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint("price > 0", name="price_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(60), unique=True
    )
    price: Mapped[int]
    level: Mapped[str] = mapped_column(String(12))
    owner_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "students.id", name="courses_owner_id_fkey"
        )
    )
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="course",
        order_by="Lesson.position",
        cascade="all, delete-orphan",
    )


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id")
    )
    title: Mapped[str] = mapped_column(String(80))
    position: Mapped[int]
    course: Mapped[Course] = relationship(
        back_populates="lessons"
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(
        String(120), unique=True
    )
    password_hash: Mapped[str | None] = mapped_column(
        String(255)
    )
    role: Mapped[str] = mapped_column(
        String(12), server_default="student"
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )

    @property
    def courses(self):
        return [e.course for e in self.enrollments]


class Enrollment(Base):
    __tablename__ = "enrollments"

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id"), primary_key=True
    )
    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"), primary_key=True
    )
    enrolled_on: Mapped[date] = mapped_column(
        server_default=func.current_date()
    )
    student: Mapped[Student] = relationship(
        back_populates="enrollments"
    )
    course: Mapped[Course] = relationship()


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id")
    )
    token_hash: Mapped[str] = mapped_column(
        String(64), unique=True
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )
    revoked: Mapped[bool] = mapped_column(default=False)
    student: Mapped[Student] = relationship()
