# Gotcha 8 - class and instance attributes (the same code as lesson one of this module)
class Course:
    students = []


python = Course()
sql = Course()
python.students.append("Lukas")
print(sql.students)


class Counter:
    total = 0


c = Counter()
c.total += 1
print(c.total, Counter.total)
