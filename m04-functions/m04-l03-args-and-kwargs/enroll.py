def enroll(course, *students):
    for student in students:
        print(f"{student} joined {course}")

enroll("Python Basics", "Asha", "Lukas", "Priya")
