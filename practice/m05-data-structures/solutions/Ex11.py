# Exercise 11 - Fix the broken dictionary code (all five repaired)
student = {"name": "Asha"}
print(student.get("email", "no email"))     # was: student["email"]

course_key = ("python", 3)                  # was: a list
prices = {course_key: 1499}
print(prices)

scores = {"Asha": 80, "Lukas": 40, "Rahul": 65}
to_remove = []
for name in scores:                         # first collect ...
    if scores[name] < 50:
        to_remove.append(name)
for name in to_remove:                      # ... then delete
    del scores[name]
print(scores)

student = {"name": "Asha", "city": "Pune"}
for key, value in student.items():          # was: for key, value in student
    print(key, "=", value)

prices = {"python": 1499, "python_advanced": 1299}   # was: "python" twice
print(prices, len(prices))
