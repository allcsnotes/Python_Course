# Q23 - A decorator that takes arguments
import functools

def retry(times, exceptions=(Exception,)):      # layer 1: the settings
    def decorator(func):                        # layer 2: the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):           # layer 3: each call
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    print(f"attempt {attempt} failed: {error}")
                    if attempt == times:
                        raise
        return wrapper
    return decorator

calls = {"n": 0}

@retry(times=3, exceptions=(ConnectionError,))
def fetch():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("network down")
    return "ok"

print(fetch())
