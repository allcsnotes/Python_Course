class Lesson:
    def __init__(self, title, minutes, free):
        self.title = title
        self.minutes = minutes
        self.free = free

    def __repr__(self):
        return f"Lesson({self.title}, {self.minutes}, {self.free})"

    def __eq__(self, other):
        a = (self.title, self.minutes, self.free)
        b = (other.title, other.minutes, other.free)
        return a == b


lesson = Lesson("Variables", 12, True)
print(lesson)
print(lesson == Lesson("Variables", 12, True))
