import time

from toolkit import cache_for, timed

PRICES = {"C101": 499, "C102": 799}


@timed
@cache_for(1)
def get_price(course_id):
    print("looking up", course_id)
    time.sleep(0.2)
    return PRICES[course_id]


print(get_price("C101"))
print(get_price("C101"))
print(get_price("C102"))
time.sleep(1.2)
print(get_price("C101"))
