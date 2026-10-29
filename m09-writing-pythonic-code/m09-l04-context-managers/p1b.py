class Door:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


with Door:
    print("inside")
