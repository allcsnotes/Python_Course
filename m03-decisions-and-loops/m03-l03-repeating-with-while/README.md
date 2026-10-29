# M03-L03 · Repeating with while

> Video: Module 3, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- How a `while` loop repeats its body while a condition is True, and checks the condition before every round
- The three parts of a counting loop: start, test, update (and counting down)
- Infinite loops: the three usual causes, and how to escape with Ctrl + C
- Sentinel loops (stop at a special value), accumulators (running totals) and "ask until valid" loops
- A loop with two stopping reasons (a login with three tries), and the two common syntax mistakes

## Before you start

- Python 3.14 or newer (`python --version`). Do [M03-L02](../m03-l02-comparing-and-combining/) first.
- A terminal opened in this folder.
- Some programs here never stop on purpose. Press Ctrl + C (hold Control, press C) to stop them. Their output below is shortened.

## Files in this folder

| File | What it is |
|------|------------|
| `welcome.py`, `welcome_loop.py` | Three copied lines, then 1000 welcome messages from a four-line loop |
| `count_up.py` | The first loop: a counter from 1 to 3 with `<=` |
| `rounds_less.py`, `rounds.py` | Two experiments: `<` instead of `<=`, and a counter that starts at 5 |
| `countdown.py` | Counting down: 3, 2, 1, Go! |
| `forever.py`, `skip.py`, `indent.py` | The three infinite loops: no update, an update that skips the target, an unindented update |
| `students.py` | A sentinel loop: stop at the word `done` |
| `cart.py` | An accumulator: adding up prices until `0` |
| `seats.py` | Ask until the answer is valid |
| `login.py` | A loop with two stopping reasons: right code or three tries |
| `colon.py`, `equals.py` | The two syntax mistakes |

## Follow along

### 1. The problem

Asha wants every new student to see a welcome message. For three students you can copy the line three times:

**`welcome.py`**

```python
print("Welcome, student!")
print("Welcome, student!")
print("Welcome, student!")
```

```text
$ python welcome.py
Welcome, student!
Welcome, student!
Welcome, student!
```

But for 1000 students? Here are four lines that do it. The output is shortened here, run it to see all 1000 lines:

```python
count = 1
while count <= 1000:
    print("Welcome, student", count)
    count += 1
```

```text
$ python welcome_loop.py
Welcome, student 1
Welcome, student 2
Welcome, student 3
...
Welcome, student 999
Welcome, student 1000
```

### 2. How a while loop works

It works like washing dishes: check whether there are dirty dishes, wash one, check again, and stop when the sink is empty. In Python the check is the condition, and the steps you repeat are the body (indented four spaces). The last line is not indented, so it runs once, after the loop is over. Guess how many times `Round` is printed, then run it:

**`count_up.py`**

```python
count = 1
while count <= 3:
    print("Round", count)
    count += 1
print("Done")
```

```text
$ python count_up.py
Round 1
Round 2
Round 3
Done
```

Walk through it the way Python does: `count` is 1, is `1 <= 3`? True, print round 1, `count` becomes 2. The same for 2 and 3. Now `count` is 4: is `4 <= 3`? False. The loop is over, Python skips the body and runs the line after it.

### 3. Start, test, update

Almost every counting loop has three parts: the start (give the counter its first value), the test (the condition after `while`), and the update (change the counter so the loop moves towards the end).

What if the condition is `count < 3`, without the equals part? There is no round 3, because `<` stops as soon as the counter reaches 3 (`rounds_less.py`):

```text
$ python rounds_less.py
Round 1
Round 2
Done
```

Mixing these up is the classic off-by-one mistake: one round too many or one too few. What if the counter starts at 5 instead (`rounds.py`)? At the very first check `5 <= 3` is False, so the body never runs at all:

```text
$ python rounds.py
Done
```

Counters can count down. Here the update subtracts one:

**`countdown.py`**

```python
seconds = 3
while seconds > 0:
    print(seconds)
    seconds -= 1
print("Go!")
```

```text
$ python countdown.py
3
2
1
Go!
```

### 4. Infinite loops

What if you forget the update? Here `count` stays 1 forever:

```python
count = 1
while count <= 3:
    print("Round", count)
print("Done")
```

```text
$ python forever.py
Round 1
Round 1
Round 1
Round 1
...
^C
```

The lines fly past and the program never stops. To escape, hold Control and press C (`^C`). Your terminal comes back and nothing is damaged. An infinite loop only wastes time and power.

The second cause: an update that never hits the target. `skip.py` counts 0, 3, 6, 9, 12, ... and jumps right over 10, so `count != 10` is always True:

```python
count = 0
while count != 10:
    print(count)
    count += 3
print("Done")
```

```text
$ python skip.py
0
3
6
9
12
15
...
^C
```

The fix: use `count < 10`. The test becomes False as soon as the counter passes the limit, even if it skips over it.

The third cause is sneaky: the update line is there, but it is not indented, so it is outside the loop:

```python
count = 1
while count <= 3:
    print("Round", count)
count += 1
print("Done")
```

```text
$ python indent.py
Round 1
Round 1
Round 1
...
^C
```

Whenever a loop does not end, check three things: a missing update, an update that skips the target, or an update that is not indented.

### 5. A sentinel loop

Often you do not know how many rounds you want. A cashier scans items until a special button ends the order. In `students.py` the sentinel is the word `done`. We ask once before the loop (so the first check has something to compare) and once at the end of every round. Here the person types `Lukas`, `Priya`, `done`:

**`students.py`**

```python
name = input("Student name (or done): ")
while name != "done":
    print("Welcome,", name)
    name = input("Student name (or done): ")
print("All students welcomed.")
```

```text
$ python students.py
Student name (or done): Lukas
Welcome, Lukas
Student name (or done): Priya
Welcome, Priya
Student name (or done): done
All students welcomed.
```

There is no welcome for `done`. A good sentinel is a value that real answers can never be. The word `done` works for names. For prices, zero works.

### 6. An accumulator

Priya adds up the prices in her cart without knowing how many courses there will be. `total` starts at zero (an empty cart) and grows. A variable that collects a running sum is called an accumulator. She types 1499, 999, then 0 to finish:

**`cart.py`**

```python
total = 0
price = int(input("Course price (0 to finish): "))
while price != 0:
    total += price
    price = int(input("Course price (0 to finish): "))
print("Cart total:", total)
```

```text
$ python cart.py
Course price (0 to finish): 1499
Course price (0 to finish): 999
Course price (0 to finish): 0
Cart total: 2498
```

### 7. Ask until valid

Lukas books seats for a live session, one to five. The condition describes what is wrong (fewer than 1 or more than 5), so the loop keeps asking while the answer is bad. He types 0, then 9, then 2:

**`seats.py`**

```python
seats = int(input("Seats (1 to 5): "))
while seats < 1 or seats > 5:
    print("Please choose from 1 to 5.")
    seats = int(input("Seats (1 to 5): "))
print("Booked", seats, "seats")
```

```text
$ python seats.py
Seats (1 to 5): 0
Please choose from 1 to 5.
Seats (1 to 5): 9
Please choose from 1 to 5.
Seats (1 to 5): 2
Booked 2 seats
```

### 8. Two ways to stop

Many sites lock you out after three wrong tries. The condition has two parts joined by `and`, so one False part is enough to end the loop. After the loop, an `if` finds out which reason it was. Lukas types 1234, then 4821:

**`login.py`**

```python
attempts = 0
code = ""
while code != "4821" and attempts < 3:
    code = input("Course code: ")
    attempts += 1
if code == "4821":
    print("Welcome in!")
else:
    print("Too many tries.")
```

```text
$ python login.py
Course code: 1234
Course code: 4821
Welcome in!
```

A different person types three wrong codes:

```text
$ python login.py
Course code: 1234
Course code: 0000
Course code: 1111
Too many tries.
```

### 9. Two common mistakes

Forgetting the colon:

**`colon.py`**

```python
count = 1
while count <= 3
    print("Round", count)
    count += 1
```

```text
$ python colon.py
  File "colon.py", line 2
    while count <= 3
                    ^
SyntaxError: expected ':'
```

A single `=` inside the condition (one stores, two ask):

**`equals.py`**

```python
count = 1
while count = 3:
    print("Round", count)
    count += 1
```

```text
$ python equals.py
  File "equals.py", line 2
    while count = 3:
          ^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

Fix the sign and run again. And if you ever see a loop that never ends, remember the three suspects: a missing update, an update that skips the target, or an update that is not indented.

## Interview tip

"What is a `while` loop, and what is an infinite loop?" A `while` loop repeats its body as long as its condition is true, and checks the condition before every round. An infinite loop is one whose condition never becomes false, usually because the update is missing, skips the target or is outside the loop.

## Common mistakes

- Forgetting the update (`count += 1`), or putting it outside the loop.
- A test that the counter can jump over (`!=` instead of `<`).
- `<` versus `<=`: off by one round.
- A missing colon, or `=` instead of `==` in the condition.
- Forgetting to ask a second time at the end of a sentinel loop.

## Clean up

Nothing to clean up. If a loop is still running in your terminal, press Ctrl + C.

## Next

[M03-L04 · Repeating with for and range](../m03-l04-repeating-with-for-and-range/)
