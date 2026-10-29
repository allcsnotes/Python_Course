import csv

with open("expenses.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.reader(file))

amount = rows[1][0]
print(amount, type(amount))
print(amount * 2)
print(float(amount) * 2)
