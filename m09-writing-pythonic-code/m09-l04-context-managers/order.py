from contextlib import contextmanager


@contextmanager
def step(name):
    print("start", name)
    try:
        yield
    finally:
        print("end", name)


with step("A"), step("B"):
    print("inside")
