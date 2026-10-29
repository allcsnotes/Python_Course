import sys


class Course:
    pass


a = Course()
print(sys.getrefcount(a))
b = a
print(sys.getrefcount(a))
team = [a]
print(sys.getrefcount(a))
del b
print(sys.getrefcount(a))
