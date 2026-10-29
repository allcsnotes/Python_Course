class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons

    def __str__(self):
        return f"{self.title} (Rs {self.price})"


basics = Course("Python Basics", 499, ["Intro", "Loops"])
loops = Course("Loops Deep Dive", 299, ["while", "for"])
print(basics)
print([basics, loops])
