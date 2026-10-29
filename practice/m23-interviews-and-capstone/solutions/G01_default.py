# Gotcha 1 - the mutable default (the same code as lesson one of this module)
def add(name, students=[]):
    students.append(name)
    return students


def add_fixed(name, students=None):
    if students is None:
        students = []
    students.append(name)
    return students


print(add("Lukas"))
print(add("Priya"))
print(add_fixed("Lukas"))
print(add_fixed("Priya"))
