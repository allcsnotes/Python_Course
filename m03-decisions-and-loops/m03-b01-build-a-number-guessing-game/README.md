# M03-B01 · Build a Number Guessing Game

> Video: Module 3, Build 1. Watch it first, then follow along here.

The computer thinks of a secret number and you try to find it. Asha builds it for the break room of allcsvideos.com, so a student who finishes a lesson can play a quick round. We build it from an empty file in seven small steps, and every step uses something from Module 3: decisions, comparisons and loops.

## What you'll learn

- How to plan a program on paper (requirements, then a flow picture) and build it in small steps, running after each one
- How to pick a random number with `import random` and `random.randint(a, b)` (both ends included)
- How `if`/`elif`/`else`, `while`, `break`, `continue`, a counter and a flag fit together
- How to guard input with `isdigit()` before `int()`, and how `match` picks a level
- How to wrap a whole round in an outer loop (play again) with a best score

## Before you start

- Python 3.14 or newer (`python --version`). Modules 1 to 3 (especially [M03-L05](../m03-l05-nested-loops-and-match/)) are needed.
- A terminal opened in this folder (`m03-b01-build-a-number-guessing-game`).

## Files in this folder

| File | What it is |
|------|------------|
| `guess.py` | The finished game (the project as at the end of the video) |
| `steps/step1/dice.py` | Step 1: roll a random number |
| `steps/step2/guess.py` | Step 2: judge one guess (secret fixed at 42) |
| `steps/step3/guess.py` | Step 3: keep asking in a loop, count the tries |
| `steps/step4/guess.py` | Step 4: limit the tries |
| `steps/step5/guess.py` | Step 5: guard the input |
| `steps/step6/guess.py` | Step 6: levels and a random secret |

## Run it

The finished game:

```bash
python guess.py
```

Type a level, then your guesses. The secret is random, so your numbers differ. To get exactly the numbers shown below, there is a small trick: a fixed seed (a starting number for the random generator). For example, this recorded run uses seed 5:

```text
$ python -c "import random, runpy; random.seed(5); runpy.run_path('guess.py', run_name='__main__')"
=== Number Guessing Game ===
Level (easy, medium, hard): hard
I am thinking of a number from 1 to 100.
Guess 1 of 7: 70
Too low!
Guess 2 of 7: 85
Too high!
Guess 3 of 7: 80
Correct! You needed 3 tries.
New best score!
Best so far: 3
Play again? (y/n): y
I am thinking of a number from 1 to 100.
Guess 1 of 7: 50
Too high!
Guess 2 of 7: 25
Too low!
Guess 3 of 7: 37
Too high!
Guess 4 of 7: 31
Too low!
Guess 5 of 7: 33
Correct! You needed 5 tries.
Best so far: 3
Play again? (y/n): n
Thanks for playing!
```

The first round: level `hard` (1 to 100, 7 tries), guesses 70, 85, 80, and it was correct in 3 tries, a new best score. Then `y` to play again, and 50, 25, 37, 31, 33 won in 5 tries, which is not a new best, so the best stays 3.

A lost round on `easy` (seed 24, so the secret is 7 and you only get 4 tries; four wrong guesses lose):

```text
$ python -c "import random, runpy; random.seed(24); runpy.run_path('guess.py', run_name='__main__')"
=== Number Guessing Game ===
Level (easy, medium, hard): easy
I am thinking of a number from 1 to 10.
Guess 1 of 4: 1
Too low!
Guess 2 of 4: 2
Too low!
Guess 3 of 4: 3
Too low!
Guess 4 of 4: 4
Too low!
Out of tries! The number was 7.
Play again? (y/n): n
Thanks for playing!
```

## Build it step by step

### 0. Plan on paper

A builder never lays bricks without a drawing first. The requirements:

1. The computer picks a secret number.
2. The player types a guess.
3. The computer answers too low, too high or correct.
4. The player can guess again, until correct or out of tries.
5. The game survives careless input (letters, numbers out of range).
6. There are levels, and the player can play again and see a best score.

We do not build it all at once: the smallest working piece first, run it, then add one feature. As a picture: pick the secret, ask for a guess, compare, if right the player wins, if not go back and ask again. That arrow going back up is a loop, the heart of the game. The seven steps: the secret, one guess, the loop, the limit, safe input, levels, play again.

### 1. The secret number

The game must pick a different number every time. A fixed `secret = 42` would be the same every game. Python can pick by chance, but not with a helper we have used so far: this one lives in a separate drawer called `random`. `import random` opens the drawer, and `random.randint(1, 6)` picks a whole number from 1 to 6, and both 1 and 6 are allowed.

```python
import random

number = random.randint(1, 6)
print("The dice shows", number)
```

Run it three times. The numbers are chosen by chance, so you get different numbers and a repeat is possible. (Imports get their own lesson in Module 7. For now remember: `import random` at the top, then `random.randint(a, b)`.) Recorded with seeds 5, 1 and 3 so you can reproduce them:

```text
$ python -c "import random, runpy; random.seed(5); runpy.run_path('dice.py', run_name='__main__')"
The dice shows 5
```

```text
$ python -c "import random, runpy; random.seed(1); runpy.run_path('dice.py', run_name='__main__')"
The dice shows 2
```

```text
$ python -c "import random, runpy; random.seed(3); runpy.run_path('dice.py', run_name='__main__')"
The dice shows 2
```

### 2. Judge one guess

While building, a random secret is annoying because you never know the answer when you test. So for now the secret is fixed at 42. The guess comes from `input`, which gives back text, so `int` turns it into a number. We never test for "equal": if the guess is not lower and not higher, only one possibility is left, so `else` catches it.

```python
secret = 42
guess = int(input("Your guess: "))

if guess < secret:
    print("Too low!")
elif guess > secret:
    print("Too high!")
else:
    print("Correct!")
```

Try 30, 60 and 42, so all three paths run:

```text
$ python guess.py
Your guess: 30
Too low!
```

```text
$ python guess.py
Your guess: 60
Too high!
```

```text
$ python guess.py
Your guess: 42
Correct!
```

The game judges one guess, but asks only once. A real game must ask again and again.

### 3. The loop

`while True` is always true, so the loop only ends when we say so with `break`. Everything moves inside the loop (four more spaces of indentation), `break` goes in the correct branch, and a counter `tries` starts at 0 and gets `tries += 1` every round.

```python
secret = 42
tries = 0

while True:
    guess = int(input("Your guess: "))
    tries += 1
    if guess < secret:
        print("Too low!")
    elif guess > secret:
        print("Too high!")
    else:
        print("Correct! Tries:", tries)
        break
```

The secret is 42. Type 50, 30, 45, 42:

```text
$ python guess.py
Your guess: 50
Too high!
Your guess: 30
Too low!
Your guess: 45
Too high!
Your guess: 42
Correct! Tries: 4
```

The loop stopped exactly when `break` ran. But a game you can never lose is not much of a game.

### 4. Limited tries

`max_tries = 5`, and the loop becomes `while tries < max_tries`. When the loop is over, how do we know why it ended? A flag, `won`, starts as `False`. The correct branch sets `won = True` and breaks, and after the loop an `if won:` prints the winning message, else the "Out of tries" message. The question is friendlier too: an f-string shows "Guess 1 of 5".

```python
secret = 42
max_tries = 5
tries = 0
won = False

while tries < max_tries:
    guess = int(input(f"Guess {tries + 1} of {max_tries}: "))
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
```

Play badly on purpose: 10, 20, 30, 40, 50:

```text
$ python guess.py
Guess 1 of 5: 10
Too low!
Guess 2 of 5: 20
Too low!
Guess 3 of 5: 30
Too low!
Guess 4 of 5: 40
Too low!
Guess 5 of 5: 50
Too high!
Out of tries! The number was 42.
```

A good round: 60, 20, 42:

```text
$ python guess.py
Guess 1 of 5: 60
Too high!
Guess 2 of 5: 20
Too low!
Guess 3 of 5: 42
Correct! You needed 3 tries.
```

### 5. Safe input

People type strange things. What if the player types the letters `abc`? The whole game crashes:

```text
$ python guess.py
Guess 1 of 5: abc
Traceback (most recent call last):
  File "guess.py", line 7, in <module>
    guess = int(input(f"Guess {tries + 1} of {max_tries}: "))
ValueError: invalid literal for int() with base 10: 'abc'
```

`ValueError: invalid literal for int()`, as you met in Module 2. The fix is a guard at the door: before calling `int`, ask the text whether it is made only of digits (`isdigit()`). If not, print a friendly message and `continue` (skip the rest of this round and ask again). A second guard checks the range. The counter goes after the checks, so a typo does not cost a try.

```python
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
```

Type `abc`, then 500, then 0, then 60, then 42. Which cost a try? None of the first three:

```text
$ python guess.py
Guess 1 of 5: abc
Please type a whole number.
Guess 1 of 5: 500
Stay between 1 and 100.
Guess 1 of 5: 0
Stay between 1 and 100.
Guess 1 of 5: 60
Too high!
Guess 2 of 5: 42
Correct! You needed 2 tries.
```

The game is solid now, but the secret is stuck at 42.

### 6. Levels and a random secret

Each level needs its own settings: `high` (the top of the range) and `max_tries`. The level word is cleaned with `strip()` and `lower()`, then a `match` sets the numbers: `easy` is 1 to 10 with 4 tries, `hard` is 1 to 100 with 7 tries, and `case _` (anything else) is the medium level, 1 to 50 with 6 tries. Why 7 tries for 100 numbers? A good guess in the middle cuts the choices in half: 100, 50, 25, 12, 6, 3, 1. Then the dice comes back: `secret = random.randint(1, high)`.

```python
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
```

Level `" Easy "` (a capital and spaces, cleaned for us), seed 24 so the secret is 7:

```text
$ python -c "import random, runpy; random.seed(24); runpy.run_path('guess.py', run_name='__main__')"
Level (easy, medium, hard):  Easy 
I am thinking of a number from 1 to 10.
Guess 1 of 4: 5
Too low!
Guess 2 of 4: 8
Too high!
Guess 3 of 4: 7
Correct! You needed 3 tries.
```

Type `banana` and no complaint: the catch-all case gives the medium level, 1 to 50 and 6 tries:

```text
$ python -c "import random, runpy; random.seed(24); runpy.run_path('guess.py', run_name='__main__')"
Level (easy, medium, hard): banana
I am thinking of a number from 1 to 50.
Guess 1 of 6: 25
Too low!
Guess 2 of 6: 46
Correct! You needed 2 tries.
```

### 7. Play again and a best score

The whole round goes inside an outer loop. Before it we create `best = 0` (no score yet) and `again = "y"` (so the first round runs). Inside the outer loop: a new secret each round, a fresh `tries` counter, a fresh `won` flag, then the guess loop. At the end of every round we ask "Play again?" and clean the answer. When the player wins we compare: if `best` is 0 (no score yet) or `tries` is less than `best`, this is a new best. Here is `guess.py`, the finished game:

```python
import random

print("=== Number Guessing Game ===")
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

best = 0
again = "y"

while again == "y":
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
        if best == 0 or tries < best:
            best = tries
            print("New best score!")
        print(f"Best so far: {best}")
    else:
        print(f"Out of tries! The number was {secret}.")

    again = input("Play again? (y/n): ").strip().lower()

print("Thanks for playing!")
```

Part one is the setup (the import, the level, the `match`, and `best` and `again`), part two is one round (secret, counters and the guess loop with its guards, hints and `break`), part three is after the loop (win or lose, best score, play again?). The runs are in the "Run it" section above. A lost round on `easy` ends like this: `Out of tries! The number was 7.`

## What can still break

- The best score lives only in memory. Close the program and it is gone (Module 6 saves it to a file).
- If the player closes the input with Ctrl + D at the first question, Python raises an `EOFError` (end of file):

```text
$ python guess.py
=== Number Guessing Game ===
Level (easy, medium, hard): ^DTraceback (most recent call last):
  File "guess.py", line 4, in <module>
    level = input("Level (easy, medium, hard): ").strip().lower()
            ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
EOFError
```

- `random` is perfect for games but predictable on purpose. Never use it for passwords or secret tokens (Python has a separate `secrets` module for that).
- All the lines sit in one long block. It works, but is hard to read next month. Module 4 teaches functions to cut it into small pieces.

## Try these upgrades yourself

- Hot and cold hints: tell the player how far away the guess was.
- Let the player choose the range.
- Save the best score (after Module 6).
- Add a daily secret number.

## Common mistakes

- Calling `int()` on text that is not digits (guard it with `isdigit()`).
- Putting `tries += 1` before the checks, so typos cost a try.
- Forgetting the `won` flag, so you cannot tell why the loop ended.
- Not resetting `tries` and `won` inside the outer loop.

## Clean up

Nothing to clean up.

## Next

You have finished Module 3. [M04-L01 · Functions as Recipes](../../m04-functions/m04-l01-functions-as-recipes/)
