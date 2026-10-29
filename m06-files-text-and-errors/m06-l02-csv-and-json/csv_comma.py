import csv

line = "250.0,food,Chai, snacks"
print(line.split(","))

row = [250.0, "food", "Chai, snacks"]
with open("chai.csv", "w", newline="", encoding="utf-8") as file:
    csv.writer(file).writerow(row)

with open("chai.csv", newline="", encoding="utf-8") as file:
    print(repr(file.read()))

with open("chai.csv", newline="", encoding="utf-8") as file:
    print(list(csv.reader(file)))
