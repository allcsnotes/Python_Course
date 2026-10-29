# Exercise 15 - Equal courses and sets
class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons

    def __repr__(self):
        return f"Course({self.title!r}, {self.price})"

    def __eq__(self, other):
        if not isinstance(other, Course):
            return NotImplemented
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)


first = Course("Python Basics", 499, ["Intro", "Loops"])
twin = Course("Python Basics", 399, ["Intro"])
other = Course("Loops Deep Dive", 299, ["while", "for"])

print(first == twin, first is twin)
print(first == other, first != other)
print(first == 5)

seen = {first, twin, other}
print(len(seen))

sales = {first: 3}
print(sales[twin])
print(twin in sales, other in sales)
