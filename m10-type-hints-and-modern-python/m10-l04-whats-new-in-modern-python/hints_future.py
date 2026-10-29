from __future__ import annotations

class Enrollment:
    def __init__(self, student: Student, course: str):
        self.student = student
        self.course = course


class Student:
    def __init__(self, name: str):
        self.name = name


print(Enrollment(Student("Lukas"), "Python").student.name)
