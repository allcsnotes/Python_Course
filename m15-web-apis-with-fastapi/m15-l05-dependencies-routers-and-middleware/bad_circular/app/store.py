class Store:
    """All courses live in memory, in a dictionary."""

    def __init__(self, courses=None):
        if courses is None:
            courses = {
                1: {"id": 1, "title": "Python Basics", "price": 499},
                2: {"id": 2, "title": "Web APIs", "price": 799},
            }
        self.courses = courses

    def add(self, title, price):
        new_id = max(self.courses, default=0) + 1
        course = {"id": new_id, "title": title, "price": price}
        self.courses[new_id] = course
        return course
