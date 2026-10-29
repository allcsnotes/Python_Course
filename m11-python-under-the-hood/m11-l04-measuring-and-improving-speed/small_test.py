import time

from data import make_rows
from stats import unique_students

for count in (200, 60000):
    rows = make_rows(count)
    start = time.perf_counter()
    unique_students(rows)
    seconds = time.perf_counter() - start
    print(f"{count} rows: {seconds:.3f} seconds")
