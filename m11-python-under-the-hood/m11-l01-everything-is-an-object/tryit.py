import math

title = "Python"
print(id(title) > 0, type(title), title)
print((2.5).is_integer())


def greet():
    pass


class Course:
    pass


for thing in [greet, Course, math]:
    print(type(thing).__name__)
big = int("1000")
same = int("1000")
print(big is same, big == same)


class Always:
    def __eq__(self, other):
        return True


item = Always()
print(item == None, item is None)
