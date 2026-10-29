def label(title: str, minutes: int) -> str:
    return f"{title} ({minutes} min)"


def total_minutes(lessons: int, minutes: int) -> int:
    return lessons * minutes


def is_free(price: int) -> bool:
    return price == 0


print(label("Python Basics", 15))
print(total_minutes(12, 15))
print(is_free(499))
