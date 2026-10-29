# Exercise 16 - Who watched what
python_viewers = ["Asha", "Lukas", "Priya", "Asha", "Rahul", "Lukas"]
sql_viewers = ["Priya", "Meera", "Rahul", "Priya"]

py = set(python_viewers)
sq = set(sql_viewers)

print("Python viewers:", sorted(py))
print("Unique counts:", len(python_viewers), "->", len(py))
print("Both:", sorted(py & sq))
print("Either:", sorted(py | sq))
print("Only Python:", sorted(py - sq))
print("Only SQL:", sorted(sq - py))
print("Exactly one course:", sorted(py ^ sq))
print("Asha watched Python?", "Asha" in py)

seen = set()
unique_in_order = []
for name in python_viewers:
    if name not in seen:
        seen.add(name)
        unique_in_order.append(name)
print("In first-seen order:", unique_in_order)
