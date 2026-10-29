try:
    with open("prices.txt") as file:
        int("abc")
except ValueError:
    print("caught")
print(file.closed)
