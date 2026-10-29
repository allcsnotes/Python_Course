for row in range(1, 4):
    for seat in range(1, 6):
        if seat == 3:
            break
        print(f"R{row}S{seat}", end=" ")
    print()
