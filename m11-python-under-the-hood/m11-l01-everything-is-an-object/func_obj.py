def greet(name):
    return f"Hello, {name}"


welcome = greet
print(welcome("Lukas"))
print(welcome is greet)
print(greet.__name__)
greet.language = "English"
print(welcome.language)
