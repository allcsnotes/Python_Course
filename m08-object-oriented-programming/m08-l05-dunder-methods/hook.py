class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons


course = Course("Python Basics", 499, ["Intro", "Loops"])
print(course)
