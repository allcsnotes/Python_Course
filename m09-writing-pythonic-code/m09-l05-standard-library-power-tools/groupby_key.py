from itertools import groupby

orders = [
    ("Python", "Lukas"),
    ("SQL", "Priya"),
    ("Python", "Asha"),
    ("SQL", "Rahul"),
]
orders.sort()
for course, rows in groupby(orders, key=lambda o: o[0]):
    names = [o[1] for o in rows]
    print(course, names)
