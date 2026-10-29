# Exercise 25 - The class gradebook
import copy


def average(marks):
    if not marks:
        return 0
    return round(sum(marks) / len(marks), 1)


def add_mark(book, name, mark):
    if name not in book:
        book[name] = []
    book[name].append(mark)


def ranking(book):
    pairs = [(name, average(marks)) for name, marks in book.items()]
    return sorted(pairs, key=lambda pair: pair[1], reverse=True)


def passed(book, limit=60):
    return {name for name, marks in book.items() if average(marks) >= limit}


def group_by_grade(book):
    groups = {}
    for name, marks in book.items():
        avg = average(marks)
        if avg >= 85:
            grade = "A"
        elif avg >= 70:
            grade = "B"
        else:
            grade = "C"
        if grade not in groups:
            groups[grade] = []
        groups[grade].append(name)
    return groups


gradebook = {
    "Asha": [92, 88, 95],
    "Lukas": [70, 65],
    "Priya": [85, 90, 78, 88],
    "Rahul": [],
    "Meera": [60, 72, 58],
}

add_mark(gradebook, "Rahul", 81)
add_mark(gradebook, "Sofia", 77)

for position, pair in enumerate(ranking(gradebook), start=1):
    print(f"{position}. {pair[0]:<8}{pair[1]:>6}")

print(sorted(passed(gradebook)))
print(group_by_grade(gradebook))

backup = copy.deepcopy(gradebook)
add_mark(gradebook, "Lukas", 100)
print("Real book:", gradebook["Lukas"])
print("Backup   :", backup["Lukas"])
