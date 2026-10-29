# Q09 - Instance, class and static methods
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def describe(self):             # needs the object
        return f"{self.title} costs Rs {self.price}"

    @classmethod
    def from_text(cls, text):       # needs the class: an alternative constructor
        title, price = text.split(",")
        return cls(title, int(price))

    @staticmethod
    def is_valid_price(price):      # needs neither
        return price >= 0

print(Course.from_text("SQL,399").describe())
print(Course.is_valid_price(-5))

class Premium(Course):
    pass

print(type(Premium.from_text("Rust,999")).__name__)   # cls follows the subclass
