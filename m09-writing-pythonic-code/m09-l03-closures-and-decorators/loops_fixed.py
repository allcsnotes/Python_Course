greeters = []
for name in ["Lukas", "Priya", "Meera"]:
    greeters.append(lambda name=name: f"Hello, {name}!")

for greeter in greeters:
    print(greeter())
