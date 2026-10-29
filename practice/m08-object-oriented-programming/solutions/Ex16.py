# Exercise 16 - A course that feels built-in
class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons

    def __str__(self):
        return f"{self.title} (Rs {self.price})"

    def __len__(self):
        return len(self.lessons)

    def __iter__(self):
        return iter(self.lessons)

    def __getitem__(self, index):
        return self.lessons[index]

    def __lt__(self, other):
        return self.price < other.price


basics = Course("Python Basics", 499, ["Intro", "Loops", "Lists"])
loops = Course("Loops Deep Dive", 299, ["while", "for"])
soon = Course("Coming Soon", 0, [])
data = Course("Data Structures", 899, ["List", "Dict"])

print(len(basics), len(loops))
print(bool(basics), bool(soon))
for lesson in basics:
    print(lesson)
print("Loops" in basics, "Dict" in basics)
print(basics[0], basics[-1], basics[:2])
print(list(loops))

for course in sorted([basics, loops, data]):
    print(course)
print(min(basics, loops, data))
print(max(basics, loops, data))

by_title = sorted([basics, loops, data], key=lambda c: c.title)
for course in by_title:
    print(course)
