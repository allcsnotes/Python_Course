total = 0
file = open("prices.txt")
try:
    for word in file.read().split():
        total = total + int(word)
    print("Total:", total)
except ValueError:
    print("A price is not a number.")
finally:
    file.close()
    print("File closed.")
