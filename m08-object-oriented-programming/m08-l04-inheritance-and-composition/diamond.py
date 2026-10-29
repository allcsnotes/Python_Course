class Person:
    pass


class Student(Person):
    def role(self):
        return "learns"


class Instructor(Person):
    def role(self):
        return "teaches"


class TeachingAssistant(Student, Instructor):
    pass


priya = TeachingAssistant()
print(priya.role())
print([c.__name__ for c in TeachingAssistant.__mro__])
