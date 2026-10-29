from functools import wraps


def remember(func):
    notebook = {}

    @wraps(func)
    def wrapper(*args):
        if args not in notebook:
            notebook[args] = func(*args)
        return notebook[args]

    return wrapper


@remember
def course_price(course_id):
    print(f"Looking up course {course_id}")
    prices = {7: 1499, 8: 999}
    return prices[course_id]


print(course_price(7))
print(course_price(7))
print(course_price(8))
