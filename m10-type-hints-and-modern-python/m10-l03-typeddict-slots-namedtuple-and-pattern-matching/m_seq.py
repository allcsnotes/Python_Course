def run(command):
    match command:
        case ["quit"]:
            return "bye"
        case ["enrol", name]:
            return f"enrolling {name}"
        case ["enrol", name, *courses]:
            return f"{name} takes {len(courses)} courses"
        case _:
            return "unknown command"


print(run(["quit"]))
print(run(["enrol", "Lukas"]))
print(run(["enrol", "Priya", "C101", "C102"]))
print(run(["enrol"]))
