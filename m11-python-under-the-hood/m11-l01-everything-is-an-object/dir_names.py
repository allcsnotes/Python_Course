seats = 7
names = [
    n for n in dir(seats)
    if not n.startswith("_")
]
print(", ".join(names))
