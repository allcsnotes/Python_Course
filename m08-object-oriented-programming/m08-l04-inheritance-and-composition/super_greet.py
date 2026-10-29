class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"


class Instructor(Person):
    def greet(self):
        base = super().greet()
        return base + ", and I teach here"


print(Instructor("Meera").greet())
