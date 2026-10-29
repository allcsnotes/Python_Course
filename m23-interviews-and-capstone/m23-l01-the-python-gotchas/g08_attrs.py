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
