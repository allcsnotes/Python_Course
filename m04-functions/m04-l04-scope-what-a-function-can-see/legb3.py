label = "global"

def outer():
    # label = "enclosing"

    def inner():
        # label = "local"
        print(label)

    inner()

outer()
