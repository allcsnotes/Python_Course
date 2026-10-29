class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes


class Course:
    def __init__(self, title):
        self.title = title
        self.lessons = []

    def add(self, lesson):
        self.lessons.append(lesson)

    def total_minutes(self):
        total = 0
        for lesson in self.lessons:
            total += lesson.minutes
        return total


basics = Course("Python Basics")
basics.add(Lesson("Variables", 12))
basics.add(Lesson("Loops", 18))
print(basics.total_minutes())
