tries = 0
while tries < 3:
    try:
        text = input("Guess: ")
    except EOFError:
        print()
        print("Input closed. Goodbye!")
        break
    if not text.isdigit():
        print("Please type a whole number.")
        continue
    tries = tries + 1
    print("You guessed", text)
print("Game over")
