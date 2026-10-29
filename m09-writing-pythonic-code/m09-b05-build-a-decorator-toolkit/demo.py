import time
from dataclasses import dataclass

from toolkit import timed, retry, cache_for, require_login
from toolkit import RetryableError, LoginRequiredError

PRICES = {"C101": 499, "C102": 799}
state = {"calls": 0}


@dataclass
class User:
    name: str
    logged_in: bool = False


@timed
@retry(times=3, delay=0.1)
def load_catalog():
    state["calls"] += 1
    if state["calls"] < 3:
        raise RetryableError("server busy")
    return list(PRICES)


@cache_for(1)
def get_price(course_id):
    print("looking up", course_id)
    time.sleep(0.2)
    return PRICES[course_id]


@require_login
def enrol(user, course_id):
    price = get_price(course_id)
    return f"{user.name} bought {course_id} for Rs {price}"


def main():
    print(load_catalog())
    priya, lukas = User("Priya", True), User("Lukas")
    print(enrol(priya, "C101"))
    print(enrol(priya, "C101"))
    try:
        enrol(lukas, "C101")
    except LoginRequiredError as error:
        print("refused:", error)
    funcs = enrol, get_price, load_catalog
    print([func.__name__ for func in funcs])


if __name__ == "__main__":
    main()
