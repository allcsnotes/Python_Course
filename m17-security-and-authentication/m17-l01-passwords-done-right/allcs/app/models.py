from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Course(Base):
    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint("price > 0", name="price_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60), unique=True)
    price: Mapped[int]
    level: Mapped[str] = mapped_column(String(12))
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
    course: Mapped[Course] = relationship(back_populates="lessons")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(255))
    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
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
