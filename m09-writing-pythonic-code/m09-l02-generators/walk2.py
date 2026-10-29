def three_numbers():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")
    yield 3


gen = three_numbers()
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
