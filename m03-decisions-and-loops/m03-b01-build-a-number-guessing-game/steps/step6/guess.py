import random

level = input("Level (easy, medium, hard): ").strip().lower()

match level:
    case "easy":
        high = 10
        max_tries = 4
    case "hard":
        high = 100
        max_tries = 7
    case _:
        high = 50
        max_tries = 6

secret = random.randint(1, high)
print(f"I am thinking of a number from 1 to {high}.")
tries = 0
won = False

while tries < max_tries:
    text = input(f"Guess {tries + 1} of {max_tries}: ")
    if not text.isdigit():
        print("Please type a whole number.")
        continue
    guess = int(text)
    if guess < 1 or guess > high:
        print(f"Stay between 1 and {high}.")
        continue
    tries += 1
    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")
    else:
        won = True
        break

if won:
    print(f"Correct! You needed {tries} tries.")
else:
    print(f"Out of tries! The number was {secret}.")
