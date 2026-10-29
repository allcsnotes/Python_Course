import csv

rows = [
    ["amount", "category", "note"],
    [250.0, "food", "Lunch"],
    [80.5, "travel", "Auto ride"],
    [120.0, "food", "Dinner"],
]

with open("expenses.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(rows)
