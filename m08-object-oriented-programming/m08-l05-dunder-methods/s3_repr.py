class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons

    def __str__(self):
        return f"{self.title} (Rs {self.price})"

    def __repr__(self):
        return f"Course({self.title!r}, {self.price}, {self.lessons})"


basics = Course("Python Basics", 499, ["Intro", "Loops"])
loops = Course("Loops Deep Dive", 299, ["while", "for"])
print(basics)
print([basics, loops])
