from domain import Course, Level

for price in [-500, 499.5, 0]:
    try:
        Course("Taster", price, Level.BEGINNER)
        print("accepted:", price)
    except ValueError as err:
        print("refused:", err)
