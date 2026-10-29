"""Task 2 - a retry decorator with exponential backoff."""
import functools
import time


def retry(times: int = 3, delay: float = 0.1, factor: float = 2.0,
          exceptions=(Exception,), sleep=time.sleep):
    """Call the function up to `times` times.

    Waits delay, delay*factor, delay*factor**2 ... between tries and re-raises
    the last error. `sleep` can be replaced in tests so they run instantly.
    """
    if times < 1:
        raise ValueError("times must be at least 1")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
                    sleep(wait)
                    wait *= factor
        return wrapper
    return decorator
