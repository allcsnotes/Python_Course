import psycopg

URL = "postgresql://postgres:devpass@localhost:15402/allcs"

with psycopg.connect(URL) as conn:
    sql = "SELECT id, title, price FROM courses LIMIT 3"
    rows = conn.execute(sql).fetchall()

print(rows)
print(rows[0][1])
