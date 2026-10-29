import gc


class Course:
    def __init__(self, title):
        self.title = title

    def __del__(self):
        print("freed", self.title)


gc.collect()
x = Course("Python")
y = Course("SQL")
x.partner = y
y.partner = x
del x
del y
print("both labels deleted")
print("collecting")
print(gc.collect())
