for seats in range(1, 100):
    total = seats * 499
    if total > 2000:
        print(seats, "seats cost", total)
        break
print("Done")
