def make_rows(count):
    rows = []
    for i in range(count):
        student = f"student{i % 9000}"
        rows.append(f"{student},course{i % 40},{(i % 7) * 100 + 99}")
    return rows


def split_row(row):
    student, course, price = row.split(",")
    return student, course, int(price)
