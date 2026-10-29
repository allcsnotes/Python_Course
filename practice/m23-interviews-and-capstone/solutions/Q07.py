# Q07 - Context managers
from contextlib import contextmanager, suppress

class Timer:
    def __enter__(self):
        print("start")
        return self
    def __exit__(self, exc_type, exc, tb):
        print("stop, error was:", exc_type.__name__ if exc_type else None)
        return False                # False: do not swallow the error

with Timer():
    print("working")

try:
    with Timer():
        1 / 0
except ZeroDivisionError:
    print("the error still came out")

@contextmanager
def tag(name):
    print(f"<{name}>")
    try:
        yield
    finally:                        # runs even when the body fails
        print(f"</{name}>")

with tag("p"):
    print("hello")

with suppress(FileNotFoundError):
    open("no-such-file.txt")
print("carried on")
