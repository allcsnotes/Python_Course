import dis


def add_all(numbers):
    total = 0
    for n in numbers:
        total += n
    return total


dis.dis(add_all)
