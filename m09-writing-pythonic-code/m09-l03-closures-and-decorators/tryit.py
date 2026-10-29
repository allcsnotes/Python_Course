from functools import wraps


def make_multiplier(n):
    def multiply(x):
        return x * n

    return multiply


def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}")
        return func(*args, **kwargs)

    return wrapper


@log_calls
def add(a, b):
    return a + b


triple = make_multiplier(3)
print(triple(5))
print(add(2, 3))
print(add.__name__)

