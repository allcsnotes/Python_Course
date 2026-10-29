from sqlalchemy import text

from db import engine

SORTABLE = {"title", "price"}


def list_courses(sort):
    if sort not in SORTABLE:
        raise ValueError(f"cannot sort by {sort!r}")
    sql = f"""SELECT title, price FROM courses
WHERE published ORDER BY {sort}"""
    with engine.connect() as conn:
        return conn.execute(text(sql)).all()


print(list_courses("price")[:2])
print(list_courses("price; DROP TABLE courses"))
