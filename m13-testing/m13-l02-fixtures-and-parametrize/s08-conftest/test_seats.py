def test_all_seats_free(course):
    assert course.seats_left() == 2


def test_one_seat_taken(course):
    course.enroll("Lukas")
    assert course.seats_left() == 1
