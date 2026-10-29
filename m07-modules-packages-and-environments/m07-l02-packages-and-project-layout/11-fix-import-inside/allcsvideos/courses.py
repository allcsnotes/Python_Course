SEATS = {"Python Basics": 30}


def seats_left(title):
    from allcsvideos.students import enrolled_count
    return SEATS[title] - enrolled_count(title)
