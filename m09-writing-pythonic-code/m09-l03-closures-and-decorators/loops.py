greeters = []
for name in ["Lukas", "Priya", "Meera"]:
    greeters.append(lambda: f"Hello, {name}!")

for greeter in greeters:
    print(greeter())
