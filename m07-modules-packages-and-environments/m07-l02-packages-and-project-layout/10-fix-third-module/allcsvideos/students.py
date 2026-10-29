from allcsvideos.courses import seats_left


def describe(name, title):
    left = seats_left(title)
    return f"{name}: {left} seats left in {title}"
