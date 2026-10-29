from allcsvideos.enrollments import enrolled_count

SEATS = {"Python Basics": 30}


def seats_left(title):
    return SEATS[title] - enrolled_count(title)
