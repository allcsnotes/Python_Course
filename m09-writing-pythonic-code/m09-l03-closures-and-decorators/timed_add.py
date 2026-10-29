import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        took = time.perf_counter() - start
        print(f"Took {took:.1f} seconds")
        return result

    return wrapper


@timer
def add(a, b):
    time.sleep(0.2)
    return a + b


print(add(2, 3))
print(add(a=10, b=5))
