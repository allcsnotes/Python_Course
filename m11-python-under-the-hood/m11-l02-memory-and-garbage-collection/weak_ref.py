import weakref


class Course:
    def __init__(self, title):
        self.title = title


course = Course("Python")
ref = weakref.ref(course)
print(ref().title)
del course
print(ref())
