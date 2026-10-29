class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


sql_course = Course("SQL", 399)
same_course = sql_course
same_course.price = 349
print(sql_course.price)
print(same_course is sql_course)
