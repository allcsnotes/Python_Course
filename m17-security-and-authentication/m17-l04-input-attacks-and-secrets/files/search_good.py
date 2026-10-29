from sqlalchemy import text

from db import engine

SQL = text("""SELECT title FROM courses
WHERE published
  AND title ILIKE :pattern""")


def search(q):
    with engine.connect() as conn:
        return conn.execute(SQL, {"pattern": f"%{q}%"}).all()
