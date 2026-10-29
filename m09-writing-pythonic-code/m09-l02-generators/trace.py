def numbers():
    for n in [1, 2, 3]:
        print("  numbers makes", n)
        yield n


def doubled(items):
    for n in items:
        print("  doubled gets", n)
        yield n * 2


for x in doubled(numbers()):
    print("main got", x)
