from itertools import batched

students = ["Lukas", "Priya", "Asha", "Meera", "Rahul"]
for group in batched(students, 2):
    print(group)
