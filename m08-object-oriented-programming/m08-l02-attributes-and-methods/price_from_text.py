class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @staticmethod
    def price_from_text(text):
        return int(text.replace("Rs", "").replace(",", ""))


print(Course.price_from_text("Rs 1,499"))
