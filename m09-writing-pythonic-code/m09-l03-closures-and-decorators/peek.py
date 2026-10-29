def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}!"

    return greet


hello = make_greeter("Hello")
namaste = make_greeter("Namaste")
print(hello.__closure__[0].cell_contents)
print(namaste.__closure__[0].cell_contents)
