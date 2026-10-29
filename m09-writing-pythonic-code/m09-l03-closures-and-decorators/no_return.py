def timer(func):
    def wrapper(*args, **kwargs):
        print("Timing...")
        func(*args, **kwargs)

    return wrapper


@timer
def add(a, b):
    return a + b


print(add(2, 3))
