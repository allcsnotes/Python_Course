import csv

item = {"note": "Lunch", "tags": ["office", "weekday"]}

with open("item.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["note", "tags"])
    writer.writeheader()
    writer.writerow(item)

with open("item.csv", newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))
print(rows[0]["tags"], type(rows[0]["tags"]))
print(rows[0]["tags"][0])
