# Exercise 07 - Courses from text
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @staticmethod
    def price_from_text(text):
        return int(text.replace("Rs", "").replace(",", ""))

    @classmethod
    def from_line(cls, line):
        title, price_text = line.split(";")
        return cls(title.strip(), cls.price_from_text(price_text))

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], int(data["price"]))


print(Course.price_from_text("Rs 1,499"))

lines = ["Python; Rs 499", "SQL; Rs 399", "Docker; Rs 449"]
courses = []
for line in lines:
    courses.append(Course.from_line(line))

total = 0
for course in courses:
    print(course.title, course.price)
    total += course.price
print("Total: Rs", total)

row = {"title": "Git", "price": "299"}
git = Course.from_dict(row)
print(git.title, git.price + 1)
