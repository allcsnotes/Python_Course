import random

students = ["Lukas", "Priya", "Meera", "Rahul"]
print(random.randint(1, 6))
print(random.choice(students))
print(random.sample(students, 2))
random.shuffle(students)
print(students)
