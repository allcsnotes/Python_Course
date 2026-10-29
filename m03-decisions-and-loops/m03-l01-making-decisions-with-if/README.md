# M03-L01 · Making Decisions with if

> Video: Module 3, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- A condition is a question with a True/False answer, and `if` runs a block only when it is True
- Indentation (four spaces) is how Python knows which lines belong to the block
- `else` for plan B, and `elif` for more than two choices (the first True question wins)
- Nested decisions (an `if` inside an `if`), and an `if` that reads a quiz score with `input`
- The five classic mistakes and the messages they give

## Before you start

- Python 3.14 or newer (`python --version`). Module 2 is needed, especially [M02-L04](../../m02-variables-and-data-types/m02-l04-true-false-and-none/) (booleans, comparisons) and [M02-L05](../../m02-variables-and-data-types/m02-l05-input-and-output/) (`input`).
- A terminal opened in this folder.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The opening problem: a check that welcomes everybody |
| `gate.py`, `gate_paid.py` | The first `if`, with `has_paid` False, then True |
| `budget_hi.py`, `budget_lo.py` | An `if` with a comparison, budget 500 then 300 |
| `block_hi.py`, `block_lo.py`, `block_bug.py` | A two-line block, and the same code with one line outdented |
| `else_hi.py`, `else_lo.py` | `if` with `else`, budget 500 then 300 |
| `disc1.py`, `disc3.py`, `disc7.py`, `disc10.py`, `disc12.py` | The seat discount with `elif`, run for 1, 3, 7, 10 and 12 seats |
| `disc_bad.py`, `ifs.py` | Questions in the wrong order, and three separate `if`s |
| `nested.py` | An `if` inside an `if` |
| `quiz.py` | A quiz score with `if`, `elif`, `else` |
| `colon.py`, `noindent.py`, `elseonly.py`, `assign.py`, `strcmp.py` | The five mistakes, on purpose |

## Follow along

### 1. The problem

Lukas has not paid, yet this program welcomes him. Guess the output:

**`hook.py`**

```python
has_paid = False
print("Checking access...")
print("Welcome! Enjoy the video.")
```

```text
$ python hook.py
Checking access...
Welcome! Enjoy the video.
```

Python never looked at `has_paid`. It ran every line from top to bottom. Real programs need to choose.

### 2. The first if

A decision is a condition (a question Python can answer with True or False) and a choice. Python builds it from `if`, `elif` and `else`. An `if` line has four parts: the word `if`, the condition, a colon `:` at the end, and an indented block underneath. If the condition is True the block runs, if it is False the whole block is skipped.

**`gate.py`**

```python
has_paid = False
print("Checking access...")
if has_paid:
    print("Welcome! Enjoy the video.")
print("Done.")
```

```text
$ python gate.py
Checking access...
Done.
```

The welcome line was skipped, and `Done.` still ran because it is not indented, so it is outside the block. Lukas pays (`has_paid = True`):

**`gate_paid.py`**

```python
has_paid = True
print("Checking access...")
if has_paid:
    print("Welcome! Enjoy the video.")
print("Done.")
```

```text
$ python gate_paid.py
Checking access...
Welcome! Enjoy the video.
Done.
```

Most conditions are comparisons:

**`budget_hi.py`**

```python
price = 499
budget = 500
if price <= budget:
    print("Lukas can afford this course.")
print("Thanks for visiting allcsvideos.")
```

```text
$ python budget_hi.py
Lukas can afford this course.
Thanks for visiting allcsvideos.
```

**`budget_lo.py`**

```python
price = 499
budget = 300
if price <= budget:
    print("Lukas can afford this course.")
print("Thanks for visiting allcsvideos.")
```

```text
$ python budget_lo.py
Thanks for visiting allcsvideos.
```

### 3. Indentation is the structure

Indentation is the empty space at the start of a line. Python has no curly brackets: lines pushed in by the same amount directly under an `if` are inside it. The standard is four spaces (in VS Code the Tab key gives four). With two indented lines, both are skipped when the condition is False:

**`block_hi.py`**

```python
price = 499
budget = 500
if price <= budget:
    print("Lukas can afford this course.")
    print("Adding it to his cart.")
print("Thanks for visiting allcsvideos.")
```

```text
$ python block_hi.py
Lukas can afford this course.
Adding it to his cart.
Thanks for visiting allcsvideos.
```

**`block_lo.py`**

```python
price = 499
budget = 300
if price <= budget:
    print("Lukas can afford this course.")
    print("Adding it to his cart.")
print("Thanks for visiting allcsvideos.")
```

```text
$ python block_lo.py
Thanks for visiting allcsvideos.
```

Now move the second line back to the left edge. Nothing else changes, but that line is no longer in the block, so it runs even though Lukas cannot afford the course:

**`block_bug.py`**

```python
price = 499
budget = 300
if price <= budget:
    print("Lukas can afford this course.")
print("Adding it to his cart.")
print("Thanks for visiting allcsvideos.")
```

```text
$ python block_bug.py
Adding it to his cart.
Thanks for visiting allcsvideos.
```

### 4. else: plan B

`else` sits at the same left edge as its `if` and means "in every other case". Exactly one of the two blocks runs, never both, never none.

**`else_lo.py`**

```python
price = 499
budget = 300
if price <= budget:
    print("Lukas can afford this course.")
else:
    print("Too expensive. Try the free lessons.")
print("Thanks for visiting allcsvideos.")
```

```text
$ python else_lo.py
Too expensive. Try the free lessons.
Thanks for visiting allcsvideos.
```

**`else_hi.py`**

```python
price = 499
budget = 500
if price <= budget:
    print("Lukas can afford this course.")
else:
    print("Too expensive. Try the free lessons.")
print("Thanks for visiting allcsvideos.")
```

```text
$ python else_hi.py
Lukas can afford this course.
Thanks for visiting allcsvideos.
```

### 5. elif: more than two choices

allcsvideos gives 25 percent off for 10 or more seats, 15 for 5 or more, 5 for 2 or more, otherwise nothing. `elif` is short for "else if". Python asks the questions from the top, the first True one wins and the rest are skipped.

```python
seats = 7
if seats >= 10:
    discount = 25
elif seats >= 5:
    discount = 15
elif seats >= 2:
    discount = 5
else:
    discount = 0
print("Discount:", discount, "percent")
```

Run for 7 seats (the file `disc7.py`), and the other seat counts:

```text
$ python disc7.py
Discount: 15 percent
```

```text
$ python disc12.py
Discount: 25 percent
```

```text
$ python disc10.py
Discount: 25 percent
```

```text
$ python disc3.py
Discount: 5 percent
```

```text
$ python disc1.py
Discount: 0 percent
```

Order matters. With the questions in the wrong order, 12 seats gets only 5 percent, because `12 >= 2` is True and Python stops there:

**`disc_bad.py`**

```python
seats = 12
if seats >= 2:
    discount = 5
elif seats >= 5:
    discount = 15
elif seats >= 10:
    discount = 25
else:
    discount = 0
print("Discount:", discount, "percent")
```

```text
$ python disc_bad.py
Discount: 5 percent
```

Three separate `if`s are three separate questions, so more than one block can run. With `elif`, only one ever runs:

**`ifs.py`**

```python
seats = 12
if seats >= 10:
    print("25 percent")
if seats >= 5:
    print("15 percent")
if seats >= 2:
    print("5 percent")
```

```text
$ python ifs.py
25 percent
15 percent
5 percent
```

The shape: one `if` first, then as many `elif` as you need, and an optional `else` at the very end.

### 6. Nested decisions

A student must be enrolled first, and only then do we check payment. The inner `if` is pushed in again, so its block is indented by eight spaces:

**`nested.py`**

```python
is_enrolled = True
has_paid = False
if is_enrolled:
    print("Welcome back, Lukas.")
    if has_paid:
        print("Playing the video.")
    else:
        print("Please complete the payment.")
else:
    print("Please enrol first.")
```

```text
$ python nested.py
Welcome back, Lukas.
Please complete the payment.
```

The shape of the code shows the structure: you can see which lines belong to which question just by their left edge.

### 7. A quiz score

The score comes from `input`, which always gives text, so we wrap it in `int`. Eighty or more unlocks the certificate, forty or more passes, otherwise try again. Priya types 85:

**`quiz.py`**

```python
score = int(input("Quiz score out of 100: "))
if score >= 80:
    print("Excellent! Certificate unlocked.")
elif score >= 40:
    print("Passed. Try again for a certificate.")
else:
    print("Not passed yet. Watch the lesson again.")
```

```text
$ python quiz.py
Quiz score out of 100: 85
Excellent! Certificate unlocked.
```

Lukas types 60:

```text
$ python quiz.py
Quiz score out of 100: 60
Passed. Try again for a certificate.
```

A new student types 20:

```text
$ python quiz.py
Quiz score out of 100: 20
Not passed yet. Watch the lesson again.
```

Three runs, three results: that is what a decision does.

### 8. The five mistakes

1. Forgetting the colon:

**`colon.py`**

```python
price = 499
budget = 300
if price <= budget
    print("Lukas can afford this course.")
```

```text
$ python colon.py
  File "colon.py", line 3
    if price <= budget
                      ^
SyntaxError: expected ':'
```

2. Forgetting to indent the block:

**`noindent.py`**

```python
price = 499
budget = 300
if price <= budget:
print("Lukas can afford this course.")
```

```text
$ python noindent.py
  File "noindent.py", line 4
    print("Lukas can afford this course.")
    ^^^^^
IndentationError: expected an indented block after 'if' statement on line 3
```

3. An `else` that is not lined up with its `if`:

**`elseonly.py`**

```python
price = 499
budget = 300
if price <= budget:
    print("Lukas can afford this course.")
  else:
    print("Too expensive.")
```

```text
$ python elseonly.py
  File "elseonly.py", line 5
    else:
         ^
IndentationError: unindent does not match any outer indentation level
```

4. One `=` instead of `==` inside a condition:

**`assign.py`**

```python
score = 80
if score = 80:
    print("Full marks!")
```

```text
$ python assign.py
  File "assign.py", line 2
    if score = 80:
       ^^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

5. Forgetting `int` when the value comes from `input` (Priya types 85):

**`strcmp.py`**

```python
score = input("Quiz score: ")
if score >= 40:
    print("Passed!")
```

```text
$ python strcmp.py
Quiz score: 85
Traceback (most recent call last):
  File "strcmp.py", line 2, in <module>
    if score >= 40:
       ^^^^^^^^^^^
TypeError: '>=' not supported between instances of 'str' and 'int'
```

`str` means string, so the text `'85'` is being compared with the number 40. The first four mistakes are caught before the program starts. This last one only stops when the line runs.

## Interview tip

"How does Python know which lines belong to an `if`?" Python uses indentation instead of curly brackets. The lines pushed in under the colon form the block, and the block ends where the indentation ends.

## Common mistakes

- Missing colon, missing indent, or an `else` not lined up with its `if` (see step 8).
- `=` (store) where you meant `==` (ask).
- Questions in the wrong order in an `elif` chain: put the most specific question first.
- Forgetting `int` around `input` before comparing with a number.

## Clean up

Nothing to clean up.

## Next

[M03-L02 · Comparing and Combining](../m03-l02-comparing-and-combining/)
