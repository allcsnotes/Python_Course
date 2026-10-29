class Course:
    def __init__(self, title, code):
        self.title = title
        self.__code = code


course = Course("Python", "PY-2026")
print(vars(course))
print(course._Course__code)
