def make_counter():
    count = 0

    def add_one():
        nonlocal count
        count += 1
        return count

    return add_one


counter = make_counter()
print(counter())
print(counter())
print(counter())
