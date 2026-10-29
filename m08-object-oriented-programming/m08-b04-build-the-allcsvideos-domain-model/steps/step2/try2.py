from domain import Lesson, Student

loops = Lesson("Loops", 15)
print(loops)
print(loops == Lesson("Loops", 15))

priya = Student("Priya", "priya@example.com")
twin = Student("Priya", "priya@example.com")
print(priya)
print(len({priya, twin}))

loops.minutes = 20
