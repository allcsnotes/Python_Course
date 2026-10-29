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
    """Add two numbers."""
    return a + b


print(add.__name__)
print(add.__doc__)
