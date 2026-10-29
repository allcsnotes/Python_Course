class Door:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit got:", exc_type, exc_value)


with Door():
    print("fine")

try:
    with Door():
        raise ValueError("bad price")
except ValueError:
    print("caught outside")
