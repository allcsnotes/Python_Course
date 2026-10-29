# M06-L03 · Exceptions

> Video: Module 6, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- What an exception is, and what "raise" and "catch" mean
- How to read a traceback from the bottom up
- How to survive bad input with `try` and `except`: one type, several types, and `as error`
- What `else` and `finally` are for
- Which habits hide bugs (bare `except`, `pass`, a try block that is too big)
- Three promises from earlier lessons kept: the age program, Ctrl+D in the guessing game, and the expense amount

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- The previous lessons in this module: [M06-L01 · Reading and Writing Files](../m06-l01-reading-and-writing-files/README.md) and [M06-L02 · CSV and JSON](../m06-l02-csv-and-json/README.md).
- Copy the `.py` files of this folder into an empty working folder and run the commands from there. A few steps ask you to create a small data file by hand (`prices.txt`, `best_score.txt`).
- Programs that ask a question show what you type after the prompt, for example `Age: 25`.

## Files in this folder

| File | What it is |
|------|------------|
| `total_prices.py` | The hook: adds four prices, one of them is `abc` |
| `checkout.py` | Three small functions, to practise reading a traceback |
| `age.py` | Age program with `try` and `except ValueError` |
| `split.py` | Split the bill: only `ValueError` is handled, zero still crashes |
| `split2.py` | Two `except` blocks |
| `split3.py` | One `except` with a tuple of types, and `as error` |
| `best.py` | `try` / `except FileNotFoundError` / `else` for the best score |
| `cleanup.py` | `try`, `except` and `finally` closing a file |
| `cleanup2.py` | Only `try` and `finally`: the cleanup still runs before the crash |
| `withcheck.py` | Shows that `with` closes the file even after an error |
| `typo.py` | Bare `except` hides a typo |
| `typo2.py` | `except ValueError` lets the typo crash loudly |
| `bare_c.py` | Bare `except` also catches Ctrl+C |
| `eof0.py` | `input()` with nothing to read: `EOFError` |
| `guesseof.py` | A guessing loop that leaves politely on Ctrl+D |
| `guard.py` | Look before you leap: check the text, then convert |
| `attempt.py` | Ask forgiveness: just try `float`, handle the failure |
| `ask.py` | A function that keeps asking until the amount is a number |
| `quiet.py` | Mistake: `except` with `pass` swallows a bad price silently |
| `loud.py` | The fix: say something |
| `unset.py` | Mistake: using `age` after a failed conversion |
| `unset2.py` | The fix: put the dependent line in `else` |

## Follow along

Run each program with `python <file>`.

### 1. The hook: one bad price

`total_prices.py`:

```python
prices = ["1499", "999", "abc", "499"]
total = 0
for text in prices:
    total = total + int(text)
print("Total:", total)
```

```bash
python total_prices.py
```

```text
Traceback (most recent call last):
  File "total_prices.py", line 4, in <module>
    total = total + int(text)
                    ~~~^^^^^^
ValueError: invalid literal for int() with base 10: 'abc'
```

No total at all. The first two prices were fine, but at `abc` the program stopped, and the last price was never looked at. That red text is a traceback. This lesson explains it and shows how a program can survive one bad price.

Think of a delivery shop. A rider cannot finish a delivery, so the rider writes a note ("nobody home") and hands it back to whoever sent the order. Each person passes the note up unless they have a plan for it. If nobody has a plan, the shop closes with the note on the door and the names of everyone it passed through. If the dispatcher has a plan ("phone the customer"), the note stops there and the shop stays open.

Python works the same way. When a line cannot do its job, Python creates a note about the problem: an object with a type (such as `ValueError`) and a message. Three words to remember:

- An exception is the note: an object that describes what went wrong.
- To raise an exception is to create it and send it up.
- To catch (or handle) it is to stop it on the way and deal with it.

### 2. Five exceptions you have met

Each of these is the last line of the red text you get from one line of code. You can run them yourself with `python -c`:

```bash
python -c 'int("abc")'
python -c '10 / 0'
python -c '{"python": 1499}["java"]'
python -c 'open("missing.txt")'
python -c 'input()' < /dev/null
```

The last line of each traceback:

```text
ValueError: invalid literal for int() with base 10: 'abc'
ZeroDivisionError: division by zero
KeyError: 'java'
FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'
EOFError: EOF when reading a line
```

(On Windows, use double quotes outside and single inside, and drop the `< /dev/null`; for the last one, press Ctrl+Z then Enter.) Each problem has its own type name. That name is what we use to catch exactly the problem we expect. `ValueError` means the kind of value is right but the content is wrong; `EOFError` (end of file) means `input` had nothing more to read.

### 3. Read a traceback

`checkout.py`:

```python
def convert_price(text):
    return int(text)


def add_price(total, text):
    return total + convert_price(text)


def checkout(prices):
    total = 0
    for text in prices:
        total = add_price(total, text)
    return total


print(checkout(["1499", "999", "abc"]))
```

```bash
python checkout.py
```

```text
Traceback (most recent call last):
  File "checkout.py", line 16, in <module>
    print(checkout(["1499", "999", "abc"]))
          ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
  File "checkout.py", line 12, in checkout
    total = add_price(total, text)
  File "checkout.py", line 6, in add_price
    return total + convert_price(text)
                   ~~~~~~~~~~~~~^^^^^^
  File "checkout.py", line 2, in convert_price
    return int(text)
ValueError: invalid literal for int() with base 10: 'abc'
```

The recipe, starting at the bottom:

1. Read the last line: the type (`ValueError`) and the message (`invalid literal for int() with base 10: 'abc'`).
2. Find the last `File` line: `line 2, in convert_price`, `return int(text)`. That is where the exception was raised. The little marks point at the exact part of the line.
3. Climb the `File` lines to see who called whom: `convert_price` was called by `add_price` (line 6), which was called by `checkout` (line 12), which was called from `<module>` (line 16). `<module>` means the main part of the file, outside any function.

A traceback is a call chain: the oldest call is first, the newest is last (that is why the header says "most recent call last"). Python blames `convert_price`, where `int` failed, but the real culprit is higher up: the text `abc` was sent in from the list on the last line.

### 4. try and except

The safety net has two parts: `try:` starts a block of code you want to attempt, and `except` followed by one type of problem starts the plan for that problem. This keeps the promise from the input and output lesson: the age program should not crash on words.

`age.py`:

```python
text = input("Age: ")
try:
    age = int(text)
    print("Next year:", age + 1)
except ValueError:
    print("Please type digits only.")
print("Thanks!")
```

Run it twice. First type `25`, then run it again and type `twenty five`:

```bash
python age.py
```

```text
Age: 25
Next year: 26
Thanks!
```

```bash
python age.py
```

```text
Age: twenty five
Please type digits only.
Thanks!
```

In slow motion: Python runs the `try` block line by line. With `25`, nothing goes wrong, so the `except` block is skipped. With words, `int(text)` raises a `ValueError`, Python jumps out of the `try` block straight to the `except` line, and the `print` line inside `try` is never run. The type matches, so the plan runs, and then the program carries on with the next line (`Thanks!`).

### 5. A different type passes through

`split.py`:

```python
text = input("People: ")
try:
    people = int(text)
    print("Each pays:", 1000 / people)
except ValueError:
    print("Please type digits only.")
```

Type `0`:

```bash
python split.py
```

```text
People: 0
Traceback (most recent call last):
  File "split.py", line 4, in <module>
    print("Each pays:", 1000 / people)
                        ~~~~~^~~~~~~~
ZeroDivisionError: division by zero
```

The `except` only catches `ValueError`, so a `ZeroDivisionError` passes straight through. That is good: we named one problem, so every other surprise still crashes loudly.

Add a second `except` block (`split2.py`). Python checks them from the top and runs the first that matches:

```python
text = input("People: ")
try:
    people = int(text)
    print("Each pays:", 1000 / people)
except ValueError:
    print("Please type digits only.")
except ZeroDivisionError:
    print("Nobody to share with.")
```

Run it three times, typing `4`, then `abc`, then `0`:

```text
People: 4
Each pays: 250.0
```

```text
People: abc
Please type digits only.
```

```text
People: 0
Nobody to share with.
```

When two problems get the same plan, put both names in round brackets in one `except` line (a tuple, from Module 5). Add `as error` to get the exception object, and print it to see Python's message. `split3.py`:

```python
text = input("People: ")
try:
    people = int(text)
    print("Each pays:", 1000 / people)
except (ValueError, ZeroDivisionError) as error:
    print("Problem:", error)
```

Type `abc`, then run again and type `0`:

```text
People: abc
Problem: invalid literal for int() with base 10: 'abc'
```

```text
People: 0
Problem: division by zero
```

The name after `as` is your choice, but `error` is clear. Use the message to tell the person what happened, or (later in the course) to write it to a log.

### 6. else: the happy path

In the files lesson, `load_best` asked `path.exists()` before reading (look before you leap). Now the other way: just try to open the file, and handle the missing file. The first time the game runs, that file does not exist. `best.py`:

```python
try:
    file = open("best_score.txt")
except FileNotFoundError:
    best = 0
else:
    best = int(file.read())
    file.close()
print("Best so far:", best)
```

Run it twice. First with no `best_score.txt` in the folder, then after you create `best_score.txt` containing just `5`:

```bash
python best.py
```

```text
Best so far: 0
```

```text
Best so far: 5
```

`else` runs only when the `try` block finished with no error. Only the line that can fail (`open`) sits inside `try`. The code that depends on it working goes in `else`, so if that code has a bug, this net does not hide it. A small `try` block, and the rest in `else`.

### 7. finally: always runs

Think of baking a cake: you try to bake it; if it burns, you throw it away (except); if it worked, you serve it (else); and finally, whatever happened, you switch the oven off.

Create a file `prices.txt` with one line: `1499 999 499`. `cleanup.py` opens the file by hand, without `with`, so you can see what `finally` does:

```python
total = 0
file = open("prices.txt")
try:
    for word in file.read().split():
        total = total + int(word)
    print("Total:", total)
except ValueError:
    print("A price is not a number.")
finally:
    file.close()
    print("File closed.")
```

```bash
python cleanup.py
```

```text
Total: 2997
File closed.
```

Now change `prices.txt` to `1499 abc 499` and run it again:

```text
A price is not a number.
File closed.
```

Either way, the file is closed. Now `cleanup2.py` has no `except`, only `try` and `finally`:

```python
total = 0
file = open("prices.txt")
try:
    for word in file.read().split():
        total = total + int(word)
    print("Total:", total)
finally:
    file.close()
    print("File closed.")
```

With the same bad `prices.txt`:

```bash
python cleanup2.py
```

```text
File closed.
Traceback (most recent call last):
  File "cleanup2.py", line 5, in <module>
    total = total + int(word)
                    ~~~^^^^^^
ValueError: invalid literal for int() with base 10: 'abc'
```

`File closed.` comes first: `finally` ran while the problem was on its way up, even though the program was about to crash. This job is so common that Python has a shortcut, the `with` statement from the files lesson. `withcheck.py` proves `with` closes the file even after an error:

```python
try:
    with open("prices.txt") as file:
        int("abc")
except ValueError:
    print("caught")
print(file.closed)
```

```bash
python withcheck.py
```

```text
caught
True
```

Use `with` for files. `finally` is the general tool, for any cleanup.

The whole family on one card:

- No error: `try`, then `else`, then `finally`.
- A handled problem: `try` up to the error, then the matching `except`, then `finally`.
- A problem nobody handles: `try` up to the error, then `finally`, and then the crash.

### 8. Mistake: the bare except

It is tempting to write `except` with no type (or `except Exception`) so that nothing can ever crash. `typo.py` has a typo on the print line (`agee`, with two e's):

```python
text = input("Age: ")
try:
    age = int(text)
    print("Next year:", agee + 1)
except:
    print("Please type digits only.")
```

```bash
python typo.py
```

```text
Age: 25
Please type digits only.
```

You typed digits, but the program says otherwise. The real problem is the typo, a `NameError`. The bare `except` caught it, told the wrong story, and hid the bug. Now name the type (`typo2.py` has `except ValueError`):

```bash
python typo2.py
```

```text
Age: 25
Traceback (most recent call last):
  File "typo2.py", line 4, in <module>
    print("Next year:", agee + 1)
                        ^^^^
NameError: name 'agee' is not defined. Did you mean: 'age'?
```

A loud crash like this is a gift: it shows exactly what to fix.

A bare `except` also catches Ctrl+C. `bare_c.py`:

```python
try:
    text = input("Age: ")
except:
    print("Nice try!")
print("Done")
```

Run it and press Ctrl+C at the question:

```text
Age: ^CNice try!
Done
```

The person cannot even stop the program. The rule: catch the narrowest type you expect, around the fewest lines. One fair use for a wide net is at the very edge of a big program, to show a friendly message, record the details, and stop. Never use it to carry on as if nothing happened.

### 9. Promise kept: Ctrl+D in the guessing game

`eof0.py` asks for a name:

```python
name = input("Your name: ")
print("Hello,", name)
```

Run it and press Ctrl+D (on Windows, Ctrl+Z then Enter) instead of typing. Ctrl+D means "no more input, ever":

```text
Your name: ^DTraceback (most recent call last):
  File "eof0.py", line 1, in <module>
    name = input("Your name: ")
EOFError
```

When the input comes from a file, the same error has a message. Try `python eof0.py < /dev/null`:

```text
Your name: Traceback (most recent call last):
  File "eof0.py", line 1, in <module>
    name = input("Your name: ")
EOFError: EOF when reading a line
```

The same type, so the same plan works for both. `guesseof.py` puts a net around only the `input` line and leaves the loop politely:

```python
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
```

Type `abc`, then `7`, then press Ctrl+D:

```text
Guess: abc
Please type a whole number.
Guess: 7
You guessed 7
Guess: ^D
Input closed. Goodbye!
Game over
```

No traceback, and the last line still ran.

### 10. Promise kept: look before you leap, or ask forgiveness

In the expense tracker we protected `float` by asking the text first. `guard.py` is that style (look before you leap). In the expense tracker we removed one dot first, so prices with decimals pass:

```python
text = input("Amount: ").strip()
if text.replace(".", "", 1).isdigit():
    amount = float(text)
    print("Saved", amount)
else:
    print("Please type a number like 250 or 80.5")
```

`attempt.py` is the other style (easier to ask forgiveness than permission): just try it, and handle the failure:

```python
text = input("Amount: ").strip()
try:
    amount = float(text)
except ValueError:
    print("Please type a number like 250 or 80.5")
else:
    print("Saved", amount)
```

Run both with six different amounts (it is easiest to run each program six times). What each one prints:

| You type | `guard.py` | `attempt.py` |
|----------|------------|--------------|
| `250` | Saved 250.0 | Saved 250.0 |
| `80.5` | Saved 80.5 | Saved 80.5 |
| `-5` | Please type a number like 250 or 80.5 | Saved -5.0 |
| `1e3` | Please type a number like 250 or 80.5 | Saved 1000.0 |
| `1,500` | Please type a number like 250 or 80.5 | Please type a number like 250 or 80.5 |
| `abc` | Please type a number like 250 or 80.5 | Please type a number like 250 or 80.5 |

`1e3` is how computers write one thousand. The guard is our own guess about what `float` accepts, and it was wrong in two places. The try version asks `float` itself. Rules of our own, like "the amount must be above zero", we add on purpose (next lesson).

Now the amount question as a function with a loop. `ask.py`:

```python
def ask_amount():
    while True:
        text = input("Amount: ").strip()
        try:
            amount = float(text)
        except ValueError:
            print("Please type a number like 250 or 80.5")
        else:
            return amount


print("Saved", ask_amount())
```

Type `abc`, then `80,5`, then `80.5`:

```text
Amount: abc
Please type a number like 250 or 80.5
Amount: 80,5
Please type a number like 250 or 80.5
Amount: 80.5
Saved 80.5
```

One typo no longer throws away every expense.

Which style? Use a quick check when it is simple and obvious (is a key in the dictionary, or use `get`). Use `try` when the check would copy Python's own rules, like numbers, or when the world can change between the check and the action: a file can exist when you check and be gone when you open it. The best-score code in step 6 is a good example: no `exists` check, just open and handle the missing file.

### 11. Mistake: swallowing the problem

`quiet.py` has `pass` (a word that does nothing, because Python needs something inside the block):

```python
total = 0
for text in ["1499", "999", "abc", "499"]:
    try:
        total = total + int(text)
    except ValueError:
        pass
print("Total:", total)
```

```bash
python quiet.py
```

```text
Total: 2997
```

It looks fine, but a bad price was thrown away without a sound. `loud.py` says something:

```python
total = 0
for text in ["1499", "999", "abc", "499"]:
    try:
        total = total + int(text)
    except ValueError:
        print("Skipping bad price:", text)
print("Total:", total)
```

```bash
python loud.py
```

```text
Skipping bad price: abc
Total: 2997
```

Later, a real program writes this to a log.

### 12. Mistake: the variable that was never set

`unset.py` handles the problem, but carries on and uses `age`:

```python
text = input("Age: ")
try:
    age = int(text)
except ValueError:
    print("Please type digits only.")
print("Next year:", age + 1)
```

Type `abc`:

```text
Age: abc
Please type digits only.
Traceback (most recent call last):
  File "unset.py", line 6, in <module>
    print("Next year:", age + 1)
                        ^^^
NameError: name 'age' is not defined
```

The fix (`unset2.py`): put every line that needs `age` in `else`, so it only runs when the conversion worked:

```python
text = input("Age: ")
try:
    age = int(text)
except ValueError:
    print("Please type digits only.")
else:
    print("Next year:", age + 1)
```

Typing `abc` now prints only the hint, and typing `25` works as before:

```text
Age: abc
Please type digits only.
```

```text
Age: 25
Next year: 26
```

A third mistake needs no file: a `try` block that is too big. If you put twenty lines inside `try`, any `ValueError` from any of them gets the same plan and you cannot tell which line failed. Keep `try` small: only the line that can fail. The rest goes in `else` or after.

## Common mistakes

- A bare `except` (or `except Exception`) that hides bugs, such as a typo, and catches Ctrl+C.
- `except ... : pass`, which swallows a problem silently. Say something instead.
- Using a variable after a failed `try`. Put the lines that need it in `else`.
- A `try` block that is too big: keep only the line that can fail inside it.
- Guarding with your own rules for things only Python can judge (like what `float` accepts). Try it and handle the failure.
- Reading a traceback from the top. Start at the bottom: type and message, then the `File` lines going up.

Interview tip. What is the difference between `except Exception` and `except ValueError`, and what do `else` and `finally` do? `except ValueError` catches only that one problem. `except Exception` catches almost everything, which hides bugs such as a typo, so I catch the narrowest type I expect, around the fewest lines. `else` runs when the `try` block had no error. `finally` always runs, so it is the place for cleanup, such as closing a file.

Before you go on, try it yourself: write a loop that asks for a number of tickets and keeps asking until the person types digits. Use `try`, `except` and `else`.

## Clean up

Delete the files you created by hand in your working folder: `prices.txt` and `best_score.txt`.

## Next

[M06-L04 · Raising and Designing Errors](../m06-l04-raising-and-designing-errors/README.md)
