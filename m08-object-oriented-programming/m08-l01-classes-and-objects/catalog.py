class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


courses = [
    Course("Python", 499),
    Course("SQL", 399),
    Course("Docker", 449),
]

total = 0
for course in courses:
    print(course.title, course.price)
    total += course.price
print("Total:", total)
