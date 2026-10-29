# M04-L01 · Functions as Recipes

> Video: Module 4, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- Why copy and paste is a trap, and how a function (a named recipe) fixes it
- Defining a function with `def`, and calling it with round brackets (two separate actions)
- How Python jumps into a function and back (the order lines run in)
- Parameters (the blank on the card) and arguments (the value you hand over)
- `print` versus `return`: the most important idea of the lesson
- Making the first cut in the guessing game, and five common mistakes

## Before you start

- Python 3.14 or newer (`python --version`). Modules 1 to 3 are needed, especially [M03-B01](../../m03-decisions-and-loops/m03-b01-build-a-number-guessing-game/).
- A terminal opened in this folder. Each demo sits in its own sub-folder (because several use the same file name). Run them from this folder as shown, for example `python welcome/welcome.py`.

## Files in this folder

| File | What it is |
|------|------------|
| `copy_v1/pages.py`, `copy_v2/pages.py` | The welcome message pasted three times, and the edit that forgot one copy |
| `def_only/welcome.py`, `welcome/welcome.py` | A function that is only defined, and defined plus called |
| `trace/trace.py` | A function with `print` lines around the call, to trace the order |
| `welcome_back/welcome.py` | Asha's fix: one function, called three times |
| `greet/greet.py` | A parameter and two different arguments |
| `show_fee/fee.py`, `fee/fee.py`, `after_return/fee.py` | `print` versus `return`, and a line after `return` |
| `game_bits/game_bits.py` | The first two functions cut out of the guessing game |
| `err_colon/`, `err_indent/`, `err_order/`, `err_brackets/`, `err_none/` | The five mistakes, each in its own folder |

## Follow along

### 1. The problem with copy and paste

Asha wants the same welcome message in three places of the allcsvideos.com app: the login page, the home page and the lesson page. The same two lines, three times:

**`copy_v1/pages.py`**

```python
# login page
print("Welcome to allcsvideos.com!")
print("Pick a course and start learning.")
# home page
print("Welcome to allcsvideos.com!")
print("Pick a course and start learning.")
# lesson page
print("Welcome to allcsvideos.com!")
print("Pick a course and start learning.")
```

```text
$ python copy_v1/pages.py
Welcome to allcsvideos.com!
Pick a course and start learning.
Welcome to allcsvideos.com!
Pick a course and start learning.
Welcome to allcsvideos.com!
Pick a course and start learning.
```

The team asks for a change: the first line should say "Welcome back". Asha edits the copies, in a hurry, and forgets one:

**`copy_v2/pages.py`**

```python
# login page
print("Welcome back to allcsvideos.com!")
print("Pick a course and start learning.")
# home page
print("Welcome back to allcsvideos.com!")
print("Pick a course and start learning.")
# lesson page
print("Welcome to allcsvideos.com!")
print("Pick a course and start learning.")
```

```text
$ python copy_v2/pages.py
Welcome back to allcsvideos.com!
Pick a course and start learning.
Welcome back to allcsvideos.com!
Pick a course and start learning.
Welcome to allcsvideos.com!
Pick a course and start learning.
```

Two pages say "Welcome back", one still says the old words, and Python shows no error. That is the trap of copy and paste: every copy is one more place to forget. The cure is to write the lines once and give them a name.

### 2. A function is a recipe card

A recipe card for masala chai has a name and a list of steps. The cook writes it once and uses it for every order. A function is exactly that: a group of steps, written once, with a name, that you can use as often as you like. You already use functions: `print` is one, and you call it with round brackets.

There are two separate actions. Writing the card is defining the function. Using it is calling the function.

### 3. Define a function

`def` (short for define) tells Python you are writing a recipe card. Then the name (the same rules as a variable name: lower case, words joined with underscores), round brackets (empty for now) and a colon. The body is indented by four spaces, like an `if` block.

**`def_only/welcome.py`**

```python
def welcome():
    print("Welcome to allcsvideos.com!")
    print("Pick a course and start learning.")
```

```text
$ python def_only/welcome.py
```

Nothing is shown and there is no error. Python only remembered the card. To cook from it, add a call at the bottom, back at the left edge:

**`welcome/welcome.py`**

```python
def welcome():
    print("Welcome to allcsvideos.com!")
    print("Pick a course and start learning.")

welcome()
```

```text
$ python welcome/welcome.py
Welcome to allcsvideos.com!
Pick a course and start learning.
```

The `def` line writes the card. The name with round brackets cooks from it.

### 4. Follow the order

Here is a slightly shorter card with a line before and a line after the call. Guess the output:

**`trace/trace.py`**

```python
def welcome():
    print("Welcome!")
    print("Let's learn.")

print("Start")
welcome()
print("Done")
```

```text
$ python trace/trace.py
Start
Welcome!
Let's learn.
Done
```

Python starts at the top. The `def` is only remembered, the body is not run. `print("Start")` is the first thing on the screen. Then the call `welcome()`: Python puts its finger on the card, jumps up to its first line, runs both lines, and then jumps back to the exact place of the call and carries on with `print("Done")`. A call is a little trip: jump into the function, run it, come back.

### 5. Asha's fix

She writes the two lines once, inside `welcome`, and calls it from each page:

**`welcome_back/welcome.py`**

```python
def welcome():
    print("Welcome back to allcsvideos.com!")
    print("Pick a course and start learning.")

# login page
welcome()
# home page
welcome()
# lesson page
welcome()
```

```text
$ python welcome_back/welcome.py
Welcome back to allcsvideos.com!
Pick a course and start learning.
Welcome back to allcsvideos.com!
Pick a course and start learning.
Welcome back to allcsvideos.com!
Pick a course and start learning.
```

No page can be forgotten, because there is only one copy. The next time somebody wants other words, she changes one place: the body of the function. Recap: a function is a named recipe, the `def` line writes it, and the name with round brackets calls it.

### 6. Parameters and arguments

This welcome is the same for everybody. A friendlier one says the student's name: a recipe with a blank to fill in. The blank goes inside the round brackets of the `def` line, and is called a parameter (`name`). Inside the body it works like a variable, a label on a box that starts empty. To fill it, put a value inside the round brackets of the call: that value is the argument.

**`greet/greet.py`**

```python
def greet(name):
    print(f"Hello, {name}!")

greet("Lukas")
greet("Priya")
```

```text
$ python greet/greet.py
Hello, Lukas!
Hello, Priya!
```

One card, two different arguments, two different results. Keep the words apart: the parameter is the blank on the card (in the `def` line), the argument is the value you hand over (in the call).

### 7. print versus return

The most important idea of this lesson, and the one that confuses almost every beginner. Two helpers each work out 3 courses at 1499 rupees. The first reads the answer out loud, the second writes it on a slip of paper and hands it to you, so you can add to it. The first is `print`: it shows a value on the screen, for a person. The second is `return`: it hands a value back to the program.

The first helper, with `print` inside the function:

**`show_fee/fee.py`**

```python
def show_fee(courses):
    print(courses * 1499)

total = show_fee(3)
print(total)
```

```text
$ python show_fee/fee.py
4497
None
```

First 4497 is printed from inside the function. Then the program prints `total`, and it is `None` (the value that means nothing, from [M02-L04](../../m02-variables-and-data-types/m02-l04-true-false-and-none/)): `show_fee` printed the number but handed nothing back. Now the second helper, one change, `return` instead of `print`:

**`fee/fee.py`**

```python
def fee(courses):
    return courses * 1499

total = fee(3)
print(total)
print(total + 100)
```

```text
$ python fee/fee.py
4497
4597
```

This time `total` really holds the number, so you can add 100 to it. When Python meets a call like `fee(3)`, it runs the function, and the call is replaced by the returned value. One more rule: `return` also ends the function on the spot. Any line below it is never reached:

**`after_return/fee.py`**

```python
def fee(courses):
    return courses * 1499
    print("Fee calculated")

print(fee(3))
```

```text
$ python after_return/fee.py
4497
```

Only the number. The `print` below the `return` never ran. Rule of thumb: `print` is for people (it shows), `return` is for the program (it hands over).

### 8. The first cut in the guessing game

Remember the last question of the game, "play again, y or n", and the title banner at the top. Each is a small job. `show_banner` only prints, so it has no `return`. `ask_again` asks the question, cleans the answer and returns it. The call is `again = ask_again()`, with empty round brackets. Type a capital `Y`:

**`game_bits/game_bits.py`**

```python
def show_banner():
    print("=== Number Guessing Game ===")

def ask_again():
    return input("Play again? (y/n): ").strip().lower()

show_banner()
again = ask_again()
print(f"You chose: {again}")
```

```text
$ python game_bits/game_bits.py
=== Number Guessing Game ===
Play again? (y/n): Y
You chose: y
```

There are two kinds of function: one that does something (shows a banner) and one that answers something (returns a value).

### 9. Five mistakes

Mistake 1, no colon on the `def` line:

**`err_colon/welcome.py`**

```python
def welcome()
    print("Welcome!")

welcome()
```

```text
$ python err_colon/welcome.py
  File "welcome.py", line 1
    def welcome()
                 ^
SyntaxError: expected ':'
```

Mistake 2, forgetting to push the body in:

**`err_indent/welcome.py`**

```python
def welcome():
print("Welcome!")

welcome()
```

```text
$ python err_indent/welcome.py
  File "welcome.py", line 2
    print("Welcome!")
    ^^^^^
IndentationError: expected an indented block after function definition on line 1
```

Mistake 3, calling the function before defining it. Python reads from the top, so on line 1 it has not met the `def` yet:

**`err_order/welcome.py`**

```python
welcome()

def welcome():
    print("Welcome!")
```

```text
$ python err_order/welcome.py
Traceback (most recent call last):
  File "welcome.py", line 1, in <module>
    welcome()
    ^^^^^^^
NameError: name 'welcome' is not defined
```

Mistake 4, no round brackets in the call. The last line is just the word `welcome`. Nothing happens, and there is no error, because you only mentioned the name of the card:

**`err_brackets/welcome.py`**

```python
def welcome():
    print("Welcome!")

welcome
```

```text
$ python err_brackets/welcome.py
```

Mistake 5, the sneaky one: printing inside the function and then using the result. `show_fee` printed 4497, but gave back `None`, so `total + 100` fails:

**`err_none/fee.py`**

```python
def show_fee(courses):
    print(courses * 1499)

total = show_fee(3)
print(total + 100)
```

```text
$ python err_none/fee.py
4497
Traceback (most recent call last):
  File "fee.py", line 5, in <module>
    print(total + 100)
          ~~~~~~^~~~~
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

## Interview tip

"What is the difference between `print` and `return` in a function?" `print` shows a value on the screen and gives back `None`. `return` hands a value back to the caller, so the program can use it, and ends the function.

## Your turn

Write a function called `square` that takes a number and returns the number times itself. Call it with 5 and print the result.

## Common mistakes

- A missing colon or indent after `def`.
- Calling a function before it is defined.
- Forgetting the round brackets in a call.
- Printing inside a function when you need to `return` the value.
- Writing code after a `return` (it never runs).

## Clean up

Nothing to clean up.

## Next

[M04-L02 · Parameters and Arguments](../m04-l02-parameters-and-arguments/)
