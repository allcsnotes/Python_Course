def announce(func):
    print("Decorating now")

    def wrapper():
        print("Calling now")
        func()

    return wrapper


@announce
def hello():
    print("Hello")


print("Defined")
hello()
hello()
