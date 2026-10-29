class Person:
    def __init__(self, name):
        self.name = name
        self.__token = "person-token"


class Student(Person):
    def __init__(self, name):
        super().__init__(name)
        self.__token = "student-token"


lukas = Student("Lukas")
print(vars(lukas))
