import timeit

from data import make_rows, split_row
from stats import total_revenue, unique_students


def total_sum(rows):
    return sum(split_row(row)[2] for row in rows)


def report(total):
    unique_students(rows)
    total(rows)


rows = make_rows(60000)
for total in (total_revenue, total_sum):
    runs = timeit.repeat(lambda: report(total), number=1, repeat=3)
    print(f"{total.__name__}: {min(runs):.2f} seconds")
