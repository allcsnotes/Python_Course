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
print(lesson.is_long)
lesson.minutes = 0
