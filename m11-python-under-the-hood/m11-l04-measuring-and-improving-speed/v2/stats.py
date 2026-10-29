from data import split_row


def unique_students(rows):
    seen = set()
    for row in rows:
        student = split_row(row)[0]
        if student not in seen:
            seen.add(student)
    return seen


def total_revenue(rows):
    total = 0
    for row in rows:
        total += split_row(row)[2]
    return total
