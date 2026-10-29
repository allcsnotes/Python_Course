# Exercise 07 - Fix the broken tuple code (all four repaired)
course = ("Python", 1499)
course = (course[0], 999)        # was: course[1] = 999
print(course)

one = ("Asha",)                  # was: ("Asha")  (no comma)
print(type(one))

name, price, lessons = ("Python", 1499, 12)   # was: only two names
print(name, price, lessons)

students = ("Lukas", "Asha")
print(sorted(students))          # was: students.sort()
