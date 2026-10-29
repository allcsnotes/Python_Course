class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, email):
        self.email = email


priya = Student("Priya", "priya@example.com")
print(priya.email)
print(priya.name)
