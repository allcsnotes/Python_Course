def three_numbers():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")
    yield 3


for number in three_numbers():
    print("got", number)
