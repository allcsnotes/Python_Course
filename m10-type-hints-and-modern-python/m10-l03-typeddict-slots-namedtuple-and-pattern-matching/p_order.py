def run(command):
    match command:
        case [first, *rest]:
            return f"first word is {first}"
        case ["quit"]:
            return "bye"


print(run(["quit"]))
