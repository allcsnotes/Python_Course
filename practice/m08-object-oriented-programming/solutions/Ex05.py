# Exercise 05 - Predict the output (class attributes)
class Course:
    currency = "Rs"
    students = []

    def __init__(self, title, price):
        self.title = title
        self.price = price


py = Course("Python", 499)
sql = Course("SQL", 399)
print(py.currency, sql.currency, Course.currency)
Course.currency = "INR"
print(py.currency, sql.currency)
py.currency = "USD"
print(py.currency, sql.currency, Course.currency)
py.students.append("Lukas")
print(sql.students)
print(py.students is sql.students)
print(vars(py))
