from data import make_rows
from stats import total_revenue, unique_students

rows = make_rows(60000)
for _ in range(30):
    unique_students(rows)
    total_revenue(rows)
