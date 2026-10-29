from sqlalchemy import text

from db import engine


def build_sql(q):
    return f"""SELECT title FROM courses
WHERE published
  AND title ILIKE '%{q}%'"""


def search(q):
    with engine.connect() as conn:
        return conn.execute(text(build_sql(q))).all()
