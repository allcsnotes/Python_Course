# Q26 - __repr__, __str__, __eq__ and __hash__
class Course:
    def __init__(self, title, price):
        self.title, self.price = title, price

    def __repr__(self):                       # for developers
        return f"Course({self.title!r}, {self.price})"

    def __str__(self):                        # for users
        return f"{self.title} (Rs {self.price})"

    def __eq__(self, other):
        return (self.title, self.price) == (other.title, other.price)

    def __hash__(self):                       # equal objects must hash alike
        return hash((self.title, self.price))

a, b = Course("Python", 499), Course("Python", 499)
print(a, [a], repr(a))
print(a == b, a is b, len({a, b}))

class NoHash:
    def __eq__(self, other):
        return True

try:
    {NoHash()}
except TypeError as error:
    print("TypeError:", error)
