def first_names(students: list[str]) -> list[str]:
    return [name.split()[0] for name in students]


print(first_names(["Asha Rao", "Lukas Weber"]))
