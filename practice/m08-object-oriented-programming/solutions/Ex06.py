# Exercise 06 - Fix the broken method code (all four repaired)
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price
        self.students = []                  # was: students = [] on the class (shared)

    def describe(self):                     # was: def describe():  (no self)
        return f"{self.title} costs Rs {self.price}"

    @classmethod                            # was: missing this line
    def from_dict(cls, data):
        return cls(data["title"], int(data["price"]))

    def is_free(self):
        return self.price == 0              # was: price == 0


py = Course("Python", 499)
print(py.describe())

sql = Course.from_dict({"title": "SQL", "price": "399"})
print(sql.title, sql.price + 1)

print(py.is_free(), Course("Intro", 0).is_free())

py.students.append("Lukas")
print(sql.students)
print(py.students)
