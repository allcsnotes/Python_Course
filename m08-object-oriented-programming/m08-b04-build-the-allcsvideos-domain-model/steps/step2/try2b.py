from domain import Lesson, Student

try:
    Lesson("Empty", 0)
except ValueError as err:
    print("refused:", err)

try:
    Student("Lukas", "lukas.example.com")
except ValueError as err:
    print("refused:", err)
