class Person:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_line(cls, line):
        return Person(line.strip())


class Student(Person):
    pass


priya = Student.from_line("  Priya ")
print(priya.name)
print(isinstance(priya, Student))
