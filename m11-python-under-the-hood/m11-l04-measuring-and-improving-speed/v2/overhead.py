import cProfile
import time

from data import make_rows
from stats import total_revenue, unique_students

rows = make_rows(60000)
start = time.perf_counter()
unique_students(rows)
total_revenue(rows)
plain = time.perf_counter() - start

with cProfile.Profile():
    start = time.perf_counter()
    unique_students(rows)
    total_revenue(rows)
    profiled = time.perf_counter() - start

print(f"normal:   {plain:.3f} seconds")
print(f"profiled: {profiled:.3f} seconds")
