class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"


class Student(Person):
    pass


class Instructor(Person):
    def greet(self):
        return f"Welcome! I am {self.name}, your instructor"


print(Student("Lukas").greet())
print(Instructor("Meera").greet())
