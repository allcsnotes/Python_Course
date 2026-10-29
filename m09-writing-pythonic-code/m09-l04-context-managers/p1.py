class Door:
    def __enter__(self):
        return self


with Door():
    print("inside")
