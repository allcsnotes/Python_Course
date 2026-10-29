def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}!"

    return greet


hello = make_greeter("Hello")
namaste = make_greeter("Namaste")
print(hello("Lukas"))
print(namaste("Priya"))
