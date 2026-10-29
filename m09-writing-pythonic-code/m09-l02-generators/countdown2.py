def countdown(start):
    while start > 0:
        yield start
        start -= 1


timer = countdown(3)
for number in timer:
    print(number)
print("--- again ---")
for number in timer:
    print(number)
