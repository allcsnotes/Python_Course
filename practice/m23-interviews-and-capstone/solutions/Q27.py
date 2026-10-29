# Q27 - Properties
class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes      # goes through the setter below

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        if value <= 0:
            raise ValueError("minutes must be positive")
        self._minutes = value

    @property
    def hours(self):                # computed, read-only
        return round(self._minutes / 60, 2)

lesson = Lesson("Loops", 90)
print(lesson.minutes, lesson.hours)
for bad in (lambda: setattr(lesson, "minutes", -5), lambda: setattr(lesson, "hours", 2)):
    try:
        bad()
    except (ValueError, AttributeError) as error:
        print(type(error).__name__ + ":", error)
