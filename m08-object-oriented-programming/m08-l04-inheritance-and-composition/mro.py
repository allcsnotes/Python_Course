class Person:
    pass


class Student(Person):
    pass


print(Student.__mro__)
print([c.__name__ for c in Student.__mro__])
