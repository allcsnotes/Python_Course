class Student:
    def __init__(self, name, city):
        self.name = name
        self.city = city


lukas = Student("Lukas", "Frankfurt")
priya = Student("Priya", "Delhi")
print(lukas.name, "lives in", lukas.city)
print(priya.name, "lives in", priya.city)
