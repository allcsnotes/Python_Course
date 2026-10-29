# Exercise 04 - Discounts and tax
class Course:
    tax_percent = 18

    def __init__(self, title, price):
        self.title = title
        self.price = price

    def describe(self):
        return f"{self.title} costs Rs {self.price}"

    def price_after(self, percent):
        return self.price * (100 - percent) // 100

    def apply_discount(self, percent):
        self.price = self.price_after(percent)

    def with_tax(self):
        return self.price * (100 + self.tax_percent) // 100


py = Course("Python", 499)
print(py.describe())
print(py.price_after(20), py.price)
py.apply_discount(20)
print(py.describe())
print(py.with_tax())

Course.tax_percent = 5
print(py.with_tax())

py.tax_percent = 0
sql = Course("SQL", 399)
print(py.with_tax(), sql.with_tax())
