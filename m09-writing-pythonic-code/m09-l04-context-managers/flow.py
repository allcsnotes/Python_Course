from contextlib import contextmanager


@contextmanager
def door():
    print("enter: open the door")
    yield
    print("exit: close the door")


with door():
    print("inside")
print("after the block")
