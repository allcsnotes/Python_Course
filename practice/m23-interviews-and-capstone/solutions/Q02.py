# Q02 - A decorator that keeps the original name
import functools
import time

def timed_plain(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

def timed(func):
    @functools.wraps(func)          # copies __name__, __doc__ and more
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

@timed_plain
def a():
    "Adds."
    return 1

@timed
def b():
    "Adds."
    return 1

print(a.__name__, a.__doc__)
print(b.__name__, b.__doc__)
b()
