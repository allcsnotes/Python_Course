secret = 42
guess = int(input("Your guess: "))

if guess < secret:
    print("Too low!")
elif guess > secret:
    print("Too high!")
else:
    print("Correct!")
