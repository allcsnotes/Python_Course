while True:
    print("1 Courses   2 Fees   3 Quit")
    choice = input("Choose: ")
    match choice:
        case "1":
            print("Python Basics, 20 lessons")
        case "2":
            print("Fee: Rs 1499")
        case "3" | "q":
            print("Bye!")
            break
        case _:
            print("Please type 1, 2 or 3")
print("Session closed")
