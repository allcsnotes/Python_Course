secret = 42
max_tries = 5
tries = 0
won = False

while tries < max_tries:
    text = input(f"Guess {tries + 1} of {max_tries}: ")
    if not text.isdigit():
        print("Please type a whole number.")
        continue
    guess = int(text)
    if guess < 1 or guess > 100:
        print("Stay between 1 and 100.")
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
