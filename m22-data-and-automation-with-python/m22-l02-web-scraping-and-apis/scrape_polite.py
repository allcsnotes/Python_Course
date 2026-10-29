import csv
import time

from polite import BASE, get
from read_page import read_page

start = time.perf_counter()
url = BASE + "/courses?page=1"
courses = []
while url:
    rows, url = read_page(get(url))
    courses.extend(rows)
    print(len(courses), "courses so far")

with open("courses.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, ["title", "price", "url"])
    writer.writeheader()
    writer.writerows(courses)

took = time.perf_counter() - start
print(f"saved {len(courses)} courses in {took:.1f} s")
