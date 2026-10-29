class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"


class Student(Person):
    pass


lukas = Student("Lukas")
print(lukas.name)
print(lukas.greet())
