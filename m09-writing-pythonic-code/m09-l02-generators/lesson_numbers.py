def lesson_numbers():
    number = 1
    while True:
        yield number
        number += 1


gen = lesson_numbers()
print(next(gen), next(gen), next(gen))

for number in lesson_numbers():
    if number > 5:
        break
    print(number)
