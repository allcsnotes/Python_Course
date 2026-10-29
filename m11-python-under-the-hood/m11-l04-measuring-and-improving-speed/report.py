import time
from data import make_rows
from stats import total_revenue, unique_students


def build_report(rows):
    students = unique_students(rows)
    revenue = total_revenue(rows)
    return len(students), revenue


rows = make_rows(60000)
start = time.perf_counter()
print(build_report(rows))
print(f"{time.perf_counter() - start:.3f} seconds")
