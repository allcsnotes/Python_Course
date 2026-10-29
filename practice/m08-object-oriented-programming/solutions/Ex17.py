# Exercise 17 - Fix the broken dunder code (all five repaired)
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):                  # was: return self.price  (a number, not text)
        return f"{self.title} (Rs {self.price})"

    def __eq__(self, other):            # was: no isinstance check (first == 5 crashed)
        if not isinstance(other, Course):
            return NotImplemented
        return self.title == other.title

    def __hash__(self):                 # was: missing, so a set of courses crashed
        return hash(self.title)


course = Course("Python Basics", 499)
print(course)                           # was: def __str_  (one underscore short)
print(course == 5)

basics = Course("Python Basics", 499)
seen = {basics, Course("Loops", 299)}
print(len(seen))

print(basics in seen)
renamed = Course("Python Advanced", 499)  # was: basics.title = "Python Advanced" on an object inside a set
print(renamed in seen)
