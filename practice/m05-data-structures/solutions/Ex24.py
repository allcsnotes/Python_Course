# Exercise 24 - Does the function change my list?
def add_bonus_in_place(marks, bonus):
    for i, mark in enumerate(marks):
        marks[i] = mark + bonus


def with_bonus(marks, bonus):
    result = []
    for mark in marks:
        result.append(mark + bonus)
    return result


def reassign(marks):
    marks = [0, 0, 0]


def extend_in_place(marks):
    marks.extend([100])


def concat(marks):
    marks = marks + [100]
    return marks


original = [50, 60, 70]

new_list = with_bonus(original, 5)
print(original, new_list)

reassign(original)
print(original)

concat(original)
print(original)

extend_in_place(original)
print(original)

add_bonus_in_place(original, 10)
print(original)

result = concat(original)
print(result is original, result == original + [100])
