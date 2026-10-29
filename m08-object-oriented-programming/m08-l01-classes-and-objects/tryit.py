class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes


first = Lesson("Variables", 12)
second = Lesson("Loops", 18)
print(first.minutes + second.minutes)
