import csv

rows = [["amount", "category"], [250.0, "food"], [80.5, "travel"]]

with open("windows.csv", "w", newline="\r\n", encoding="utf-8") as file:
    csv.writer(file).writerows(rows)

with open("windows.csv", newline="", encoding="utf-8") as file:
    for row in csv.reader(file):
        print(row)
