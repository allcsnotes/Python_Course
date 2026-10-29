class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    pass


class Instructor(Person):
    pass


lukas = Student("Lukas")
print(isinstance(lukas, Student))
print(isinstance(lukas, Person))
print(isinstance(lukas, Instructor))
print(type(lukas) is Person)
