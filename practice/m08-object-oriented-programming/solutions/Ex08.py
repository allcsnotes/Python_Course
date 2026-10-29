# Exercise 08 - A lesson that checks its minutes
class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        if value < 1:
            raise ValueError(f"minutes must be at least 1, got {value}")
        self._minutes = value

    @property
    def is_long(self):
        return self._minutes > 60


lesson = Lesson("Classes", 45)
print(lesson.is_long)

lesson.minutes = 90
print(lesson.minutes, lesson.is_long)

try:
    lesson.minutes = 0
except ValueError as error:
    print("Rejected:", error)
print(lesson.minutes)

try:
    Lesson("Empty", -5)
except ValueError as error:
    print("Rejected:", error)

try:
    lesson.is_long = True
except AttributeError as error:
    print("Cannot set:", error)
