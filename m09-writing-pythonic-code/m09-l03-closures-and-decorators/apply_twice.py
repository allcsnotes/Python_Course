def excite(text):
    return text + "!"


def apply_twice(func, value):
    return func(func(value))


print(apply_twice(excite, "Hi"))
