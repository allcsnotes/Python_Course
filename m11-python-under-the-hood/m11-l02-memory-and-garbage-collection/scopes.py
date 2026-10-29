class Course:
    def __init__(self, title):
        self.title = title

    def __del__(self):
        print("freed", self.title)


def make():
    temp = Course("Temp")
    print("made", temp.title)


make()
print("after the call")
x = Course("Python")
x = Course("SQL")
print("moved the label")
del x
print("done")
