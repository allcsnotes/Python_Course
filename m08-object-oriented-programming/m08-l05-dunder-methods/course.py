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
        if not isinstance(other, Course):
            return NotImplemented
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)

    def __len__(self):
        return len(self.lessons)

    def __iter__(self):
        return iter(self.lessons)

    def __getitem__(self, index):
        return self.lessons[index]

    def __lt__(self, other):
        return self.price < other.price
