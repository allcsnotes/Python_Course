choice = "2"

match choice:
    case "1":
        print("Show courses")
    case "2":
        print("Show my fees")
    case "3":
        print("Contact support")
    case _:
        print("Unknown option")
