class Course:
    def __del__(self):
        raise ValueError("oops")


c = Course()
del c
print("done")
