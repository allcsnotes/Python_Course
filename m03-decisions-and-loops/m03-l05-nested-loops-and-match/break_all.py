found = False
for row in range(1, 4):
    for seat in range(1, 6):
        print(f"R{row}S{seat}", end=" ")
        if row == 2 and seat == 3:
            found = True
            break
    print()
    if found:
        break
print("Seat found!")
