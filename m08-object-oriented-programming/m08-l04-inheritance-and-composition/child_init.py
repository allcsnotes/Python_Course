class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"


class Student(Person):
    def __init__(self, name, email):
        super().__init__(name)
        self.email = email


priya = Student("Priya", "priya@example.com")
print(priya.name)
print(priya.email)
print(priya.greet())
