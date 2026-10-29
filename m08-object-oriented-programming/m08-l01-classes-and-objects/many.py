class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


python_course = Course("Python", 499)
sql_course = Course("SQL", 399)
docker_course = Course("Docker", 449)

sql_course.price = 349
print(python_course.price)
print(sql_course.price)
print(docker_course.price)
