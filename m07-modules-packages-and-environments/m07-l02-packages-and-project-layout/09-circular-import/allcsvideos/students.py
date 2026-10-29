from allcsvideos.courses import seats_left

ENROLLED = {"Python Basics": ["Lukas", "Priya"]}


def enrolled_count(title):
    return len(ENROLLED[title])


def describe(name, title):
    left = seats_left(title)
    return f"{name}: {left} seats left in {title}"
