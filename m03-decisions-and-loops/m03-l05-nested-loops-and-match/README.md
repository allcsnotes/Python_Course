# M03-L05 · Nested Loops and match

> Video: Module 3, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- A nested loop is a loop inside a loop: the inner loop runs completely for every step of the outer loop
- Drawing a rectangle and a staircase, and printing a multiplication table
- `break` only leaves the innermost loop, and how to stop both loops with a flag
- `match` and `case` for choosing between many values: `_` (wildcard), `|` (or), and a menu inside `while True`
- The classic mistakes (same loop variable twice, text versus number in a `case`)

## Before you start

- Python 3.14 or newer (`python --version`; `match` needs 3.10 or newer). Do [M03-L04](../m03-l04-repeating-with-for-and-range/) first.
- A terminal opened in this folder.

## Files in this folder

| File | What it is |
|------|------------|
| `seats.py` | The live-class hall: 3 rows of 5 seats |
| `trace.py` | A small nested loop to trace step by step |
| `stars.py`, `stars_one.py`, `stars_col.py`, `stars_bad.py` | A star rectangle, and three ways to break it |
| `stairs.py`, `times.py` | A staircase, and a multiplication table |
| `break_one.py`, `break_all.py` | `break` in a nested loop, and stopping everything |
| `same_name.py` | The same loop variable used twice |
| `menu_if.py`, `menu_match.py`, `menu_9.py`, `menu_nodef.py` | A menu with `if`/`elif` and with `match`, an unknown choice, and no `_` case |
| `cmd_or.py`, `day.py` | `|` (or) in a pattern |
| `pit_type.py`, `pit_fix.py` | The text-versus-number trap with `input` |
| `menu.py` | The help-desk menu: `while True` plus `match` plus `break` |

## Follow along

### 1. The live-class hall

Asha sets up a live class with 3 rows of 5 seats. A loop inside a loop:

**`seats.py`**

```python
for row in range(1, 4):
    for seat in range(1, 6):
        print(f"R{row}S{seat}", end=" ")
    print()
```

```text
$ python seats.py
R1S1 R1S2 R1S3 R1S4 R1S5 
R2S1 R2S2 R2S3 R2S4 R2S5 
R3S1 R3S2 R3S3 R3S4 R3S5 
```

Fifteen seat labels in three neat rows. A loop inside a loop is a nested loop, and it is how programs handle grids, tables and patterns.

### 2. Slow hand and fast hand

Think of a clock. The minute hand goes all the way round while the hour hand barely moves. The slow hand is the outer loop, the fast hand is the inner loop. The rule: for every single step of the outer loop, the inner loop runs completely, from its start to its end. In the hall, the row is the slow hand and the seat is the fast hand.

### 3. Trace it

Guess how many lines this prints and what the first two are:

**`trace.py`**

```python
for hour in range(1, 4):
    for minute in range(1, 3):
        print(hour, minute)
```

```text
$ python trace.py
1 1
1 2
2 1
2 2
3 1
3 2
```

`hour` is 1, then the inner loop runs completely (`1 1`, `1 2`). Only when it has run out of numbers does Python go back to the outer loop for `hour` 2. The outer loop runs 3 times and the inner loop runs 2 times each, so 3 x 2 = 6 lines.

### 4. Draw a rectangle

Three rows, five stars each. The key line is the empty `print()`: it is indented one level only, so it belongs to the outer loop and runs once per row, to start a new line.

**`stars.py`**

```python
for row in range(3):
    for col in range(5):
        print("*", end="")
    print()
```

```text
$ python stars.py
*****
*****
*****
```

Experiment: delete that last `print()`. Nothing tells Python to start a new line:

**`stars_one.py`**

```python
for row in range(3):
    for col in range(5):
        print("*", end="")
```

```text
$ python stars_one.py
***************
```

Or keep the `print()` but push it one level deeper, so it belongs to the inner loop. Now there is a new line after every single star:

**`stars_col.py`**

```python
for row in range(3):
    for col in range(5):
        print("*", end="")
        print()
```

```text
$ python stars_col.py
*
*
*
*
*
*
*
*
*
*
*
*
*
*
*
```

Indentation decides which loop a line belongs to. Indented under the inner loop, it runs for every star. Indented under the outer loop only, it runs once per row.

### 5. A staircase

One star in the first row, two in the second, and so on. The number of stars in a row is the row number, so the inner loop can use the outer variable: `range(row)`.

**`stairs.py`**

```python
for row in range(1, 6):
    for col in range(row):
        print("*", end="")
    print()
```

```text
$ python stairs.py
*
**
***
****
*****
```

This is the pattern for patterns: the outer loop chooses the row, the inner loop draws what that row needs.

### 6. A multiplication table

`{row * col:>4}` right-aligns each product in 4 places, so the columns line up:

**`times.py`**

```python
for row in range(1, 6):
    for col in range(1, 6):
        print(f"{row * col:>4}", end="")
    print()
```

```text
$ python times.py
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
   4   8  12  16  20
   5  10  15  20  25
```

### 7. break in a nested loop

`break` only leaves the loop it is directly inside, the innermost one. Show only the first two seats of every row:

**`break_one.py`**

```python
for row in range(1, 4):
    for seat in range(1, 6):
        if seat == 3:
            break
        print(f"R{row}S{seat}", end=" ")
    print()
```

```text
$ python break_one.py
R1S1 R1S2 
R2S1 R2S2 
R3S1 R3S2 
```

The outer loop carried on with the next row. To stop everything, Lukas looks for seat R2S3. When he finds it, set a flag (`found = True`) and `break` the inner loop, then ask at the outer level `if found: break`:

**`break_all.py`**

```python
found = False
for row in range(1, 4):
    for seat in range(1, 6):
        print(f"R{row}S{seat}", end=" ")
        if row == 2 and seat == 3:
            found = True
            break
    print()
    if found:
        break
print("Seat found!")
```

```text
$ python break_all.py
R1S1 R1S2 R1S3 R1S4 R1S5 
R2S1 R2S2 R2S3 
Seat found!
```

Row 1 prints in full, row 2 stops at seat 3, and row 3 never even starts.

### 8. match: choosing between many options

The help-desk menu: type 1 for courses, 2 for fees, 3 for support. First with `if` and `elif`. The choice is the text `"2"`:

**`menu_if.py`**

```python
choice = "2"

if choice == "1":
    print("Show courses")
elif choice == "2":
    print("Show my fees")
elif choice == "3":
    print("Contact support")
else:
    print("Unknown option")
```

```text
$ python menu_if.py
Show my fees
```

The comparison `choice ==` is repeated on every branch, and with ten options that gets long. `match` looks at one value and compares it with a list of patterns:

**`menu_match.py`**

```python
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
```

```text
$ python menu_match.py
Show my fees
```

Python goes from top to bottom and runs only the first matching `case`. The last case `_` is a wildcard that matches anything (like `else`). Change the choice to `"9"`:

**`menu_9.py`**

```python
choice = "9"

match choice:
    case "1":
        print("Show courses")
    case "2":
        print("Show my fees")
    case "3":
        print("Contact support")
    case _:
        print("Unknown option")
```

```text
$ python menu_9.py
Unknown option
```

What if there is no `_` case and the choice is `"9"`? Nothing happens, and there is no error. Python just skips the `match` and moves on. A `case _` is your safety net:

**`menu_nodef.py`**

```python
choice = "9"

match choice:
    case "1":
        print("Show courses")
    case "2":
        print("Show my fees")
    case "3":
        print("Contact support")

print("Done")
```

```text
$ python menu_nodef.py
Done
```

### 9. Several values in one case

A vertical bar `|` means "or". Here three commands do the same thing:

**`cmd_or.py`**

```python
command = "quit"

match command:
    case "q" | "quit" | "exit":
        print("Goodbye!")
    case "help" | "h":
        print("Showing help")
    case _:
        print("Unknown command")
```

```text
$ python cmd_or.py
Goodbye!
```

It works with numbers too:

**`day.py`**

```python
day = 6

match day:
    case 6 | 7:
        print("Weekend: live class at 10")
    case _:
        print("Weekday: recorded lessons")
```

```text
$ python day.py
Weekend: live class at 10
```

The parts of `match`: `match` and the value you look at, `case` and a pattern, `|` for several values, and `_` for anything else.

### 10. The text-versus-number trap

`input` always returns text. A pattern `1` (no quotes) is the number one, so the person's text `"1"` never matches:

**`pit_type.py`**

```python
choice = input("Choice: ")

match choice:
    case 1:
        print("Show courses")
    case _:
        print("Unknown option")
```

```text
$ python pit_type.py
Choice: 1
Unknown option
```

To Python the number 1 and the text `"1"` are different things. Put quotes around the pattern (or convert the input with `int`):

**`pit_fix.py`**

```python
choice = input("Choice: ")

match choice:
    case "1":
        print("Show courses")
    case _:
        print("Unknown option")
```

```text
$ python pit_fix.py
Choice: 1
Show courses
```

### 11. The full help-desk menu

`while True` repeats forever, and a `break` ends it. `break` sits inside a `case`, inside the `while`. `match` is not a loop, so `break` leaves the `while`. The person types 1, then 2, then 9, then 3:

**`menu.py`**

```python
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
```

```text
$ python menu.py
1 Courses   2 Fees   3 Quit
Choose: 1
Python Basics, 20 lessons
1 Courses   2 Fees   3 Quit
Choose: 2
Fee: Rs 1499
1 Courses   2 Fees   3 Quit
Choose: 9
Please type 1, 2 or 3
1 Courses   2 Fees   3 Quit
Choose: 3
Bye!
Session closed
```

This shape is very real: a loop that asks, decides and sometimes breaks.

### 12. Common mistakes

Forgetting to indent the inner body (the `print` is not indented under the inner `for`):

**`stars_bad.py`**

```python
for row in range(3):
    for col in range(5):
    print("*", end="")
```

```text
$ python stars_bad.py
  File "stars_bad.py", line 3
    print("*", end="")
    ^^^^^
IndentationError: expected an indented block after 'for' statement on line 2
```

The same variable name for both loops. The outer `i` gets overwritten by the inner loop:

**`same_name.py`**

```python
for i in range(3):
    for i in range(2):
        print(i, end=" ")
    print("outer is", i)
```

```text
$ python same_name.py
0 1 outer is 1
0 1 outer is 1
0 1 outer is 1
```

The outer `i` should have been 0, then 1, then 2, but each time you see the inner loop's last value, 1. Use different names (`row` and `col`). And if stars come out on one long line or one per line, check where your `print()` is indented.

## Interview tip

"You have two nested loops, and each runs 100 times. How many times does the inner body run?" 10,000 times: the inner body runs outer times inner, so nested loops multiply the work. Keep nesting shallow when the numbers get big.

## Common mistakes

- Not indenting the inner loop's body.
- Using the same variable for the outer and inner loop.
- Putting the newline `print()` in the wrong loop.
- Expecting `break` to leave both loops: it leaves only the innermost.
- Quoting (or not) a `case` pattern wrongly: the number `1` is not the text `"1"`.
- No `case _` when you want to handle unexpected values.

## Clean up

Nothing to clean up.

## Next

[M03-B01 · Build a Number Guessing Game](../m03-b01-build-a-number-guessing-game/)
