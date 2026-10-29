"""Task 9 - enrollments in Postgres: constraints, transactions and seat limits."""
from sqlalchemy import ForeignKey, UniqueConstraint, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "t09_student"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="student")


class Course(Base):
    __tablename__ = "t09_course"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    seats: Mapped[int]


class Enrollment(Base):
    __tablename__ = "t09_enrollment"
    __table_args__ = (UniqueConstraint("student_id", "course_id"),)   # the database enforces it
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("t09_student.id"), index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("t09_course.id"), index=True)
    student: Mapped[Student] = relationship(back_populates="enrollments")
    course: Mapped[Course] = relationship()


class CourseFull(Exception):
    pass


class AlreadyEnrolled(Exception):
    pass


def enroll(engine, student_id: int, course_id: int) -> int:
    """One transaction. The course row is locked, so two people cannot take the last seat."""
    with Session(engine) as session, session.begin():
        course = session.execute(
            select(Course).where(Course.id == course_id).with_for_update()
        ).scalar_one()                                     # NoResultFound if it does not exist
        taken = session.scalar(
            select(func.count()).select_from(Enrollment).where(Enrollment.course_id == course_id))
        if taken >= course.seats:
            raise CourseFull(course.title)
        row = Enrollment(student_id=student_id, course_id=course_id)
        session.add(row)
        try:
            session.flush()
        except IntegrityError as error:
            raise AlreadyEnrolled(f"{student_id} in {course_id}") from error
        return row.id


def titles_for(engine, student_id: int) -> list[str]:
    """All titles with three queries in total, however many enrollments (no N+1)."""
    with Session(engine) as session:
        student = session.scalars(
            select(Student).where(Student.id == student_id)
            .options(selectinload(Student.enrollments).selectinload(Enrollment.course))
        ).one()
        return sorted(e.course.title for e in student.enrollments)
