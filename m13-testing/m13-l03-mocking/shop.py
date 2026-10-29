from store import fetch_price


def label(course_id):
    return f"Rs {fetch_price(course_id)}"
