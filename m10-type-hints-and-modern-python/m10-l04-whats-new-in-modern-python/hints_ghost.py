def enrol(student: Ghost, course: str):
    return f"{course} for {student}"


print(enrol("Lukas", "Python"))
print(enrol.__annotations__)
