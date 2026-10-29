# Exercise 01 - The student class
class Student:
    def __init__(self, name, city):
        self.name = name
        self.city = city


lukas = Student("Lukas", "Frankfurt")
priya = Student("Priya", "Delhi")
sofia = Student("Sofia", "Madrid")

students = [lukas, priya, sofia]
for student in students:
    print(student.name, "lives in", student.city)

priya.city = "Mumbai"
print(priya.name, "moved to", priya.city)
print(lukas.city, sofia.city)
print(type(lukas) is Student)
