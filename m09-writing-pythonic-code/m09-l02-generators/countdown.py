def countdown(start):
    while start > 0:
        yield start
        start -= 1


for number in countdown(3):
    print(number)
print("Class starts!")
