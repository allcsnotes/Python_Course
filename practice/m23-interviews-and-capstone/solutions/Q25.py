# Q25 - MRO and super()
class Person:
    def hello(self):
        return ["Person"]

class Student(Person):
    def hello(self):
        return ["Student"] + super().hello()

class Mentor(Person):
    def hello(self):
        return ["Mentor"] + super().hello()

class StudentMentor(Student, Mentor):
    def hello(self):
        return ["StudentMentor"] + super().hello()

print([c.__name__ for c in StudentMentor.__mro__])
print(StudentMentor().hello())      # Person appears once: super() follows the MRO
