class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], int(data["price"]))


row = {"title": "Python", "price": "499"}
python_course = Course.from_dict(row)
print(python_course.title, python_course.price + 1)
