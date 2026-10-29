from contextlib import contextmanager


@contextmanager
def opened(path):
    file = open(path)
    try:
        yield file
    finally:
        file.close()
        print("closed")


with opened("prices.txt") as f:
    print(f.readline().strip())
print(f.closed)
