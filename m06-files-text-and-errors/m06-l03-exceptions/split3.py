text = input("People: ")
try:
    people = int(text)
    print("Each pays:", 1000 / people)
except (ValueError, ZeroDivisionError) as error:
    print("Problem:", error)
