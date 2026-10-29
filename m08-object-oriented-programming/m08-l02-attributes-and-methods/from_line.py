class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @classmethod
    def from_line(cls, line):
        title, price = line.split(",")
        return cls(title.strip(), int(price))


sql_course = Course.from_line("SQL, 399")
print(sql_course.title, sql_course.price)
