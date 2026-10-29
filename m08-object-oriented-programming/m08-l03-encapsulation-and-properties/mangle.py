class Course:
    def __init__(self, title, code):
        self.title = title
        self.__code = code


course = Course("Python", "PY-2026")
print(course.title)
print(course.__code)
