# Exercise 11 - People of allcsvideos
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"


class Student(Person):
    def __init__(self, name, email):
        super().__init__(name)
        self.email = email


class Instructor(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def greet(self):
        return super().greet() + f", I teach {self.subject}"


lukas = Student("Lukas", "lukas@example.com")
meera = Instructor("Meera", "Python")

for person in [lukas, meera]:
    print(person.greet())

print(lukas.email)
print(isinstance(meera, Person), isinstance(meera, Student), type(meera) is Person)
print(isinstance(lukas, Person), isinstance(lukas, Instructor))
