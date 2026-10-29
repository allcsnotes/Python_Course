class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price
        self.students = []


python_course = Course("Python", 499)
sql_course = Course("SQL", 399)
python_course.students.append("Lukas")
print(sql_course.students)
print(python_course.students is sql_course.students)
