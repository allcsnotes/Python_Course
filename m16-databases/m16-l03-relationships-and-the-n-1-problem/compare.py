import time

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from counting import QueryCounter
from db import engine
from models import Course

counter = QueryCounter(engine)
with engine.connect():
    pass  # open the first connection before timing


def run(name, stmt):
    counter.count = 0
    start = time.perf_counter()
    with Session(engine) as session:
        for course in session.scalars(stmt).unique():
            len(course.lessons)
    ms = (time.perf_counter() - start) * 1000
    print(f"{name:<13}queries: {counter.count:>3}   {ms:>3.0f} ms")


base = select(Course)
run("lazy", base)
run("selectinload", base.options(selectinload(Course.lessons)))
run("joinedload", base.options(joinedload(Course.lessons)))
