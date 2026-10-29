def add_student(name, students=None):
    if students is None:
        students = []
    students.append(name)
    return students

print(add_student("Lukas"))
print(add_student("Priya"))
team = ["Asha"]
print(add_student("Meera", team))
