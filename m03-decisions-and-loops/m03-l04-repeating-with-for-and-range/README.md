# M03-L04 · Repeating with for and range

> Video: Module 3, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- The `for` loop: "for each item in a group, do this" (letters of a text, numbers from `range`)
- `range(stop)`, `range(start, stop)` and `range(start, stop, step)`: starts at 0, stops before the stop, steps can be negative
- Common jobs: repeat N times, a price list, adding up (accumulator), counting letters, looping over positions
- `break` (leave the loop), `continue` (skip one trip) and `else` on a loop (runs when there was no `break`)
- Choosing `for` or `while`, and five common mistakes

## Before you start

- Python 3.14 or newer (`python --version`). Do [M03-L03](../m03-l03-repeating-with-while/) first.
- A terminal opened in this folder.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py`, `range_print.py` | `range(5)` printed in a loop, and `range(5)` printed itself |
| `while_letters.py`, `letters.py`, `letters_up.py`, `while_hello.py` | The same jobs with `while` and with `for` |
| `count_s.py` | Counting the letter `s` in `allcsvideos` |
| `nl_a.py` to `nl_h.py`, `iv_a.py` | Eight `range` forms, each printing its numbers on one line |
| `repeat.py`, `seats.py`, `total.py`, `inside_total.py`, `total100.py`, `positions.py` | Repeat a fixed number of times, a price list, adding up, positions |
| `break_seats.py`, `continue_lessons.py` | `break` and `continue` |
| `pw_ok.py`, `pw_bad.py` | `for ... else`: a password needs a digit |
| `off_zero.py`, `off_four.py`, `off_fix.py` | The off-by-one mistake and its fix |
| `float_err.py`, `down_bad.py`, `down_ok.py`, `no_colon.py` | More mistakes: a decimal in `range`, counting down without a step, a missing colon |

## Follow along

### 1. The opening puzzle

Guess what `range(5)` gives:

**`hook.py`**

```python
for i in range(5):
    print(i)
```

```text
$ python hook.py
0
1
2
3
4
```

Five numbers, starting at zero, and the last one is four. We never wrote a counter, a condition or a `+= 1`: the loop did all that for us.

### 2. for versus while

A `for` loop is for when you know what you are going through, like a teacher handing a certificate to every student in a line: "for each item in a group, do this". One trip around a loop is an iteration. Print every letter of a word, first with `while` (you need a position counter, a condition and an update), then with `for`:

**`while_letters.py`**

```python
word = "Python"
i = 0
while i < len(word):
    print(word[i])
    i += 1
```

```text
$ python while_letters.py
P
y
t
h
o
n
```

**`letters.py`**

```python
word = "Python"
for letter in word:
    print(letter)
```

```text
$ python letters.py
P
y
t
h
o
n
```

Same result, far less to forget.

### 3. Reading a for loop

The `for` line has four parts: the word `for`, the loop variable (`letter`, holds the current item, you choose the name), the word `in`, the group to walk through, and a colon. The indented body runs once for every item. Trip one: `letter` is `P`. Trip two: `y`. And so on, six letters, six trips, six lines. The loop ends by itself when there are no more items.

The body can do anything you like:

**`letters_up.py`**

```python
word = "Python"
for letter in word:
    print(letter.upper())
```

```text
$ python letters_up.py
P
Y
T
H
O
N
```

Counting how many times the letter `s` appears in `allcsvideos`, with a tally:

**`count_s.py`**

```python
word = "allcsvideos"
count = 0
for letter in word:
    if letter == "s":
        count += 1
print("s appears", count, "times")
```

```text
$ python count_s.py
s appears 2 times
```

The last `print` is not indented, so it runs once, after the loop.

### 4. range

`range` produces a run of numbers, like the numbered tickets on a roll.

- `range(stop)`: starts at 0, stops before the stop number.
- `range(start, stop)`: starts at `start`, stops before `stop`. The stop is the first number you do not get. `stop - start` is how many numbers.
- `range(start, stop, step)`: add `step` each time. A negative step counts down.

Each file prints its numbers on one line (`end=" "`):

**`nl_a.py`**

```python
for n in range(5):
    print(n, end=" ")
```

```text
$ python nl_a.py
0 1 2 3 4 
```

**`nl_b.py`**

```python
for n in range(1, 6):
    print(n, end=" ")
```

```text
$ python nl_b.py
1 2 3 4 5 
```

**`nl_c.py`**

```python
for n in range(3, 8):
    print(n, end=" ")
```

```text
$ python nl_c.py
3 4 5 6 7 
```

**`nl_d.py`**

```python
for n in range(0, 10, 2):
    print(n, end=" ")
```

```text
$ python nl_d.py
0 2 4 6 8 
```

**`nl_e.py`**

```python
for n in range(5, 0, -1):
    print(n, end=" ")
```

```text
$ python nl_e.py
5 4 3 2 1 
```

**`nl_f.py`**

```python
for n in range(10, 0, -3):
    print(n, end=" ")
```

```text
$ python nl_f.py
10 7 4 1 
```

**`nl_g.py`**

```python
for n in range(2, 10, 3):
    print(n, end=" ")
```

```text
$ python nl_g.py
2 5 8 
```

**`nl_h.py`**

```python
for n in range(1, 11):
    print(n, end=" ")
```

```text
$ python nl_h.py
1 2 3 4 5 6 7 8 9 10 
```

`range(10, 0, -3)` gives 10, 7, 4, 1 and then stops, because the next number (-2) would pass zero. Why start at zero? Because the first letter of a text sits at index 0 (the same idea as in [M02-L03](../../m02-variables-and-data-types/m02-l03-text-and-strings/)). Printing `range(5)` itself does not show the numbers:

**`range_print.py`**

```python
print(range(5))
```

```text
$ python range_print.py
range(0, 5)
```

`iv_a.py` is the one-line version of the first loop (`for n in range(5): print(n, end=" ")`):

```text
$ python iv_a.py
0 1 2 3 4 
```

### 5. Jobs with range

Repeat a fixed number of times. We do not need the number itself, so by habit the loop variable is called `_`. To get 100 messages, change one number:

**`repeat.py`**

```python
for _ in range(3):
    print("Welcome to allcsvideos!")
```

```text
$ python repeat.py
Welcome to allcsvideos!
Welcome to allcsvideos!
Welcome to allcsvideos!
```

A price list. One seat costs 499 rupees:

**`seats.py`**

```python
for seats in range(1, 6):
    print(f"{seats} x 499 = {seats * 499}")
```

```text
$ python seats.py
1 x 499 = 499
2 x 499 = 998
3 x 499 = 1497
4 x 499 = 1996
5 x 499 = 2495
```

Adding up. This is the accumulator from last lesson. Trip one: `n` is 1 and `total` becomes 1. Trip two: 3. And so on, 15 at the end. The final `print` is not indented, so it runs once:

**`total.py`**

```python
total = 0
for n in range(1, 6):
    total += n
print(total)
```

```text
$ python total.py
15
```

To see the total grow, put the `print` inside the loop (indented):

**`inside_total.py`**

```python
total = 0
for n in range(1, 6):
    total += n
    print(total)
```

```text
$ python inside_total.py
1
3
6
10
15
```

Change one number, `range(1, 101)`, and the loop makes 100 trips:

**`total100.py`**

```python
total = 0
for n in range(1, 101):
    total += n
print(total)
```

```text
$ python total100.py
5050
```

When you need the position of each letter, loop over `range(len(word))` and pick the letter with `word[i]`:

**`positions.py`**

```python
word = "Python"
for i in range(len(word)):
    print(i, word[i])
```

```text
$ python positions.py
0 P
1 y
2 t
3 h
4 o
5 n
```

For comparison, the `while` version of a repeat-three-times loop:

**`while_hello.py`**

```python
count = 0
while count < 3:
    print("Welcome")
    count += 1
```

```text
$ python while_hello.py
Welcome
Welcome
Welcome
```

### 6. break

`break` leaves the loop immediately. Each seat costs 499. At what seat count does the total pass 2000? `break` sits inside an `if`, which is almost always how it is used:

**`break_seats.py`**

```python
for seats in range(1, 100):
    total = seats * 499
    if total > 2000:
        print(seats, "seats cost", total)
        break
print("Done")
```

```text
$ python break_seats.py
5 seats cost 2495
Done
```

The loop stopped after five trips. The other 94 trips never happened. Python jumped to the line after the loop.

### 7. continue

`continue` stops this trip right now, jumps back to the top and takes the next item. Lukas has already seen lesson 3, so he skips it:

**`continue_lessons.py`**

```python
for lesson in range(1, 6):
    if lesson == 3:
        continue
    print("Watching lesson", lesson)
```

```text
$ python continue_lessons.py
Watching lesson 1
Watching lesson 2
Watching lesson 4
Watching lesson 5
```

Lesson 3 is missing, but the loop did not stop. `break` leaves the loop, `continue` only skips the rest of this trip.

### 8. for ... else

A sign-up form needs a password with at least one digit. Check the characters one by one. If you find a digit, you are done (`break`). If you get to the end without finding one, show a message. That second case is what loop `else` is for: the `else` block runs when the loop finishes normally, that is, without a `break`. Read it as "if we did not break".

**`pw_ok.py`**

```python
password = "lukas2024"
for ch in password:
    if ch.isdigit():
        print("Good: it has a digit")
        break
else:
    print("Add at least one digit")
```

```text
$ python pw_ok.py
Good: it has a digit
```

**`pw_bad.py`**

```python
password = "lukaspass"
for ch in password:
    if ch.isdigit():
        print("Good: it has a digit")
        break
else:
    print("Add at least one digit")
```

```text
$ python pw_bad.py
Add at least one digit
```

### 9. for or while?

Use `for` when you know what you are going through: a number of repeats or the letters of a text. Use `while` when you repeat until something happens. Ask: do I know in advance what I am going through? Printing 1 to 10: `for`. Keep asking for a password until it is right: `while`. Checking every letter of a name: `for`. Waiting until a download is finished: `while`.

### 10. Five mistakes

Mistake 1, off by one. Asha wants lessons 1 to 5:

**`off_zero.py`**

```python
for lesson in range(5):
    print("Lesson", lesson)
```

```text
$ python off_zero.py
Lesson 0
Lesson 1
Lesson 2
Lesson 3
Lesson 4
```

Lesson 0 should not exist and there is no lesson 5. Try `range(1, 5)`:

**`off_four.py`**

```python
for lesson in range(1, 5):
    print("Lesson", lesson)
```

```text
$ python off_four.py
Lesson 1
Lesson 2
Lesson 3
Lesson 4
```

It starts well but stops at lesson 4, because the stop is never included. The stop must be one more than the last number you want:

**`off_fix.py`**

```python
for lesson in range(1, 6):
    print("Lesson", lesson)
```

```text
$ python off_fix.py
Lesson 1
Lesson 2
Lesson 3
Lesson 4
Lesson 5
```

Mistake 2, a number with a decimal point. `range` accepts only whole numbers:

**`float_err.py`**

```python
for i in range(2.5):
    print(i)
```

```text
$ python float_err.py
Traceback (most recent call last):
  File "float_err.py", line 1, in <module>
    for i in range(2.5):
             ~~~~~^^^^^
TypeError: 'float' object cannot be interpreted as an integer
```

Mistake 3, counting down without a negative step. `range(5, 0)` starts at 5 and the step is +1, so there is nothing to go through:

**`down_bad.py`**

```python
for n in range(5, 0):
    print(n)
print("Liftoff!")
```

```text
$ python down_bad.py
Liftoff!
```

Add a step of `-1`:

**`down_ok.py`**

```python
for n in range(5, 0, -1):
    print(n)
print("Liftoff!")
```

```text
$ python down_ok.py
5
4
3
2
1
Liftoff!
```

Mistake 4: a line in the wrong place. If the total `print` is indented, it belongs to the loop and prints every trip (see `inside_total.py` above).

Mistake 5, the colon:

**`no_colon.py`**

```python
for i in range(3)
    print(i)
```

```text
$ python no_colon.py
  File "no_colon.py", line 1
    for i in range(3)
                     ^
SyntaxError: expected ':'
```

When a loop gives a surprising result, ask three questions: where does it start, where does it stop, and what is the step?

## Interview tip

"What does `range(2, 10, 3)` produce?" It gives 2, 5, 8. It starts at 2, adds 3 each time, and stops before 10.

## Common mistakes

- `range(5)` starts at 0 and stops at 4. For 1 to 5 write `range(1, 6)`.
- `range` only takes whole numbers.
- Counting down needs a negative step (`range(5, 0, -1)`).
- Putting the final `print` inside the loop (indented) when you want it once.
- Forgetting the colon on the `for` line.

## Clean up

Nothing to clean up.

## Next

[M03-L05 · Nested Loops and match](../m03-l05-nested-loops-and-match/)
