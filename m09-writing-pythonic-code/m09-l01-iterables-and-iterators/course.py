class Course:
    def __init__(self, title, lessons):
        self.title = title
        self.lessons = lessons

    def __iter__(self):
        return iter(self.lessons)


basics = Course("Python Basics", ["Intro", "Loops"])
walker = iter(basics)
print(next(walker))
print(next(walker))
for lesson in basics:
    print(lesson)
