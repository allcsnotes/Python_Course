import time

from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql+psycopg://allcs:allcs@localhost:20504/allcs"
)
INSERT = text(
    "insert into students (name, email, role) "
    "values (:name, :email, 'student')"
)


def rows(tag):
    return [
        {"name": f"Bulk {n}", "email": f"{tag}{n}@x.com"}
        for n in range(2000)
    ]


def one_commit_each():
    for row in rows("a"):
        with engine.begin() as conn:
            conn.execute(INSERT, row)


def one_commit_for_all():
    with engine.begin() as conn:
        for row in rows("b"):
            conn.execute(INSERT, row)


def one_call_for_all():
    with engine.begin() as conn:
        conn.execute(INSERT, rows("c"))


for func in (one_commit_each, one_commit_for_all, one_call_for_all):
    start = time.perf_counter()
    func()
    print(f"{func.__name__:<20} {time.perf_counter() - start:.2f} s")

with engine.begin() as conn:
    conn.execute(text("delete from students where name like 'Bulk %'"))
