from sqlalchemy import text

from db import engine


def search(q):
    sql = f"""SELECT title FROM courses
WHERE published
  AND title ILIKE '%{q}%'"""
    with engine.connect() as conn:
        return conn.execute(text(sql)).all()


for q in ["python", "zzz' OR true --"]:
    rows = search(q)
    print(f"{q!r}: {len(rows)} found")
    for row in rows:
        print("   ", row.title)
