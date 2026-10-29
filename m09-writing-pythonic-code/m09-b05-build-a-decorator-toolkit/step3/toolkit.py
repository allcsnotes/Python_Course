import time
from functools import wraps


class RetryableError(Exception):
    pass


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            ms = (time.perf_counter() - start) * 1000
            print(f"{func.__name__} took {ms:.0f} ms")
    return wrapper


def retry(times, delay=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except RetryableError as error:
                    print(f"attempt {attempt} failed: {error}")
                    if attempt == times:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


def cache_for(seconds):
    def decorator(func):
        saved = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in saved:
                value, stamp = saved[key]
                if now - stamp < seconds:
                    return value
            value = func(*args, **kwargs)
            saved[key] = (value, now)
            return value
        return wrapper
    return decorator
