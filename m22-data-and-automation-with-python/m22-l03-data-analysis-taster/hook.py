import csv

totals = {}
with open("enrollments.csv", newline="") as f:
    for row in csv.DictReader(f):
        course = row["course_id"]
        totals[course] = totals.get(course, 0) + int(row["price"])
print(totals)
