class Door:
    def __enter__(self):
        print("enter: open the door")
        return "the key"

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit: close the door")


with Door() as key:
    print("inside, holding", key)
    int("abc")
    print("never printed")
print("after the block")
