class Quiet:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return True


with Quiet():
    print("start")
    print(totl)
    print("end")
print("done")
