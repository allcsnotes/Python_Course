class Course:
    def __init__(self, title):
        self.title = title

    def __del__(self):
        print("freed", self.title)


a = Course("Python")
b = a
del a
print("after del a")
del b
print("after del b")
