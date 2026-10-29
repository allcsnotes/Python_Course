def greet(name):
    return f"Hello, {name}!"


shout = greet
print(shout("Lukas"))
print(shout is greet)
