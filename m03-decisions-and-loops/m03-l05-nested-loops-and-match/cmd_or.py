command = "quit"

match command:
    case "q" | "quit" | "exit":
        print("Goodbye!")
    case "help" | "h":
        print("Showing help")
    case _:
        print("Unknown command")
