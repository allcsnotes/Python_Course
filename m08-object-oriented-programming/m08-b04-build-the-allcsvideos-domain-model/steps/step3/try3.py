from domain import Course, Level

course = Course("Python Basics", 499, Level.BEGINNER)
course.add_lesson("Variables", 12)
course.add_lesson("Loops", 15)
course.add_lesson("Functions", 18)

print(course)
print([course])
print(len(course), "lessons,", course.minutes, "minutes")
for lesson in course:
    print("-", lesson.title)

course.price = 599
print(course.price)
course.price = -500
