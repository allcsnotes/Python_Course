from sqlalchemy import func, select
from sqlalchemy.orm import Session

from db import engine
from models import Enrollment


def count(s):
    return s.scalar(select(func.count()).select_from(Enrollment))


def run(level, student_id):
    reader_engine = engine.execution_options(isolation_level=level)
    with Session(reader_engine) as reader:
        first = count(reader)
        with Session(engine) as writer, writer.begin():
            writer.add(Enrollment(student_id=student_id, course_id=3))
        print(f"{level}: {first} then {count(reader)}")


run("READ COMMITTED", 1)
run("REPEATABLE READ", 2)
