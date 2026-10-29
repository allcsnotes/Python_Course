class Student:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Namaste, I am {self.name}"


class Instructor:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"


print(Student("Lukas").greet())
print(Instructor("Meera").greet())
