def total_seats(halls):
    return sum(halls)


halls = [500, 500]
if total_seats(halls) is 1000:
    print("sold out")
else:
    print("seats left")
