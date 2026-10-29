class Course:
    currency = "Rs"

    def __init__(self, title, price):
        self.title = title
        self.price = price


python_course = Course("Python", 499)
sql_course = Course("SQL", 399)
print(python_course.currency, sql_course.currency)
Course.currency = "INR"
print(python_course.currency, sql_course.currency)
python_course.currency = "USD"
print(python_course.currency, sql_course.currency)
print(Course.currency)
