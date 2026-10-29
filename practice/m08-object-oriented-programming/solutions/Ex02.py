# Exercise 02 - Predict the output (objects, labels and their own data)
class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes


a = Lesson("Variables", 12)
b = Lesson("Loops", 18)
c = a
c.minutes = 15
twin = Lesson("Loops", 18)

print(a.minutes, b.minutes)
print(c is a, b is twin)
print(type(a) is Lesson)
print(vars(b))
print(a.minutes + b.minutes)
b.title = "Loops 2"
print(twin.title, b.title)
print(b.minutes == twin.minutes)
