from functools import wraps


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper


@decorator
def greet(name):
    return f"Hello, {name}"


print(greet("Priya"))
