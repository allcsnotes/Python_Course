def make_counter():
    count = 0

    def add_one():
        count += 1

    return add_one


counter = make_counter()
counter()
