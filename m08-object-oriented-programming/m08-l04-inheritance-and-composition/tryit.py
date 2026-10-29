class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"


class Instructor(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def greet(self):
        return super().greet() + f", I teach {self.subject}"


meera = Instructor("Meera", "Python")
print(meera.greet())
print(isinstance(meera, Person))
