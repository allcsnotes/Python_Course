# Q34 - The N+1 query problem (Postgres in Docker, SQLAlchemy 2)
from sqlalchemy import ForeignKey, create_engine, event, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload

URL = "postgresql+psycopg://practice:practice@localhost:23604/practice"
engine = create_engine(URL)


class Base(DeclarativeBase):
    pass


class Course(Base):
    __tablename__ = "q34_course"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="course")


class Lesson(Base):
    __tablename__ = "q34_lesson"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    course_id: Mapped[int] = mapped_column(ForeignKey("q34_course.id"))
    course: Mapped[Course] = relationship(back_populates="lessons")


queries = []
@event.listens_for(engine, "before_cursor_execute")
def count(conn, cursor, statement, params, context, executemany):
    queries.append(statement)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
with Session(engine) as db:
    db.add_all([Course(title=f"Course {i}", lessons=[Lesson(title=f"L{j}") for j in range(3)])
                for i in range(20)])
    db.commit()

def total_lessons(options=()):
    queries.clear()
    with Session(engine) as db:
        courses = db.scalars(select(Course).options(*options)).all()
        total = sum(len(course.lessons) for course in courses)
    return total, len(queries)

print("lazy loading  : lessons, queries =", total_lessons())
print("selectinload  : lessons, queries =", total_lessons([selectinload(Course.lessons)]))
Base.metadata.drop_all(engine)
