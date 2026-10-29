def count_seats():
    seats = 0

    def add():
        nonlocal seats
        seats += 1

    add()
    add()
    print(seats)

count_seats()
