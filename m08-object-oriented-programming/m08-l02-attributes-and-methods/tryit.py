class Course:
    tax_percent = 18

    def __init__(self, title, price):
        self.title = title
        self.price = price

    def with_tax(self):
        return self.price * (100 + self.tax_percent) // 100

    @classmethod
    def from_line(cls, line):
        title, price = line.split(",")
        return cls(title, int(price))


print(Course.from_line("Python,500").with_tax())
