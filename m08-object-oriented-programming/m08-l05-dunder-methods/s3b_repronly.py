class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons

    def __repr__(self):
        return f"Course({self.title!r}, {self.price}, {self.lessons})"


basics = Course("Python Basics", 499, ["Intro", "Loops"])
print(basics)
