import json
import time
from collections import defaultdict

import orjson
import polars as pl
import psycopg

URL = "postgresql://allcs:allcs@localhost:20504/allcs"
SQL = (
    "select e.course_id, c.price from enrollments e "
    "join courses c on c.id = e.course_id"
)


def best(func, repeat=5):
    times = []
    for _ in range(repeat):
        start = time.perf_counter()
        func()
        times.append(time.perf_counter() - start)
    return min(times) * 1000


def revenue_loop(rows):
    total = defaultdict(int)
    for course_id, price in rows:
        total[course_id] += price
    return total


def revenue_polars(frame):
    return frame.group_by("course_id").agg(pl.col("price").sum())


with psycopg.connect(URL) as conn:
    small = conn.execute(SQL).fetchall()
items = [{"course_id": c, "price": p} for c, p in small]
print(f"json.dumps, 193 thousand rows  {best(lambda: json.dumps(items)):6.1f} ms")
print(f"orjson.dumps, same rows        {best(lambda: orjson.dumps(items)):6.1f} ms")

big = small * 25
for label, rows in (("193 thousand rows", small), ("4.8 million rows", big)):
    frame = pl.DataFrame(rows, schema=["course_id", "price"], orient="row")
    print(f"{label:<18} python loop {best(lambda: revenue_loop(rows)):7.1f} ms"
          f"   polars {best(lambda: revenue_polars(frame)):6.1f} ms")

report = [{"course": "Python Basics", "students": 250, "revenue": 125000,
           "first_three": ["Student 1", "Student 2", "Student 3"]}] * 8
many = 20000
print(f"json.dumps, 8-item report      {best(lambda: [json.dumps(report) for _ in range(many)]) / many * 1000:6.1f} us")
print(f"orjson.dumps, 8-item report    {best(lambda: [orjson.dumps(report) for _ in range(many)]) / many * 1000:6.1f} us")
