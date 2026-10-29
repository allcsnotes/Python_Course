import time


def timer(func):
    def wrapper():
        start = time.perf_counter()
        result = func()
        took = time.perf_counter() - start
        print(f"Took {took:.1f} seconds")
        return result

    return wrapper


@timer
def add(a, b):
    return a + b


print(add(2, 3))
