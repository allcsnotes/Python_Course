seats = int(input("Seats (1 to 5): "))
while seats < 1 or seats > 5:
    print("Please choose from 1 to 5.")
    seats = int(input("Seats (1 to 5): "))
print("Booked", seats, "seats")
