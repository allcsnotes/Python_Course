import psycopg

URL = "postgresql://allcs:allcs@localhost:17401/allcs"

with psycopg.connect(URL) as db:
    rows = db.execute("SELECT * FROM students_plain")
    print("the table a thief copies tonight:")
    for row in rows:
        print(row)
