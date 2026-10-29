total = 0
file = open("prices.txt")
try:
    for word in file.read().split():
        total = total + int(word)
    print("Total:", total)
finally:
    file.close()
    print("File closed.")
