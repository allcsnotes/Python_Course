class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons

    def __str__(self):
        return f"{self.title} (Rs {self.price})"


course = Course("Python Basics", 499, ["Intro", "Loops"])
print(course)
print(f"Now watching: {course}")
