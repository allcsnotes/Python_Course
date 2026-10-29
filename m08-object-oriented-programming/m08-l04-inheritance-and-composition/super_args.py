class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, email):
        super().__init__()
        self.email = email


priya = Student("Priya", "priya@example.com")
