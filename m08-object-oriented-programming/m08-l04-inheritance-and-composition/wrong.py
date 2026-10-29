class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes


class Course(Lesson):
    pass


course = Course("Python Basics", 600)
print(isinstance(course, Lesson))
