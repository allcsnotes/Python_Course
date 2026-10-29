def countdown(n):
    if n == 0:
        print("Go!")
    else:
        print(n)
        countdown(n - 1)


countdown(3)
