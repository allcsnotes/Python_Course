class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons

    def __str__(self):
        return f"{self.title} (Rs {self.price})"

    def __repr__(self):
        return f"Course({self.title!r}, {self.price}, {self.lessons})"

    def __eq__(self, other):
        return self.title == other.title


first = Course("Python Basics", 499, ["Intro", "Loops"])
print(first == 5)
