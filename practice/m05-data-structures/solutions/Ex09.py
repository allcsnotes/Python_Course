# Exercise 09 - A student record
student = {"name": "Asha", "course": "Python", "lessons_done": 12}
print(student)

print(student["name"], student["lessons_done"])

student["lessons_done"] = 13
student["email"] = "asha@mail.com"
print(student)

removed = student.pop("email")
print("Removed:", removed)
del student["course"]
print(student, len(student))

print("name" in student, "Asha" in student)
