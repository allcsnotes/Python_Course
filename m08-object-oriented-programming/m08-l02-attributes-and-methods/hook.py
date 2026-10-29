class Course:
    students = []

    def __init__(self, title, price):
        self.title = title
        self.price = price


python_course = Course("Python", 499)
sql_course = Course("SQL", 399)
python_course.students.append("Lukas")
print(sql_course.students)
