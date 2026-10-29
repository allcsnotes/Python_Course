import csv

with open("expenses.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

total = 0
for row in rows:
    total += row["amount"]
print(total)
