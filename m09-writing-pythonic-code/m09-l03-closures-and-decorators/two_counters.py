def make_counter():
    count = 0

    def add_one():
        nonlocal count
        count += 1
        return count

    return add_one


views = make_counter()
logins = make_counter()
print(views())
print(views())
print(logins())
print(views())
