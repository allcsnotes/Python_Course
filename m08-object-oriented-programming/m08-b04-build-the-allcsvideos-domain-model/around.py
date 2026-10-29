from domain import Course, Level

course = Course("Python Basics", 499, Level.BEGINNER)
course._price = -500
print(course.price)
