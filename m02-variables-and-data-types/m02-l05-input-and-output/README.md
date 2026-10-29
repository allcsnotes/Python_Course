# M02-L05 · Input and Output

> Video: Module 2, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- `print` in depth: several pieces, the `sep` and `end` settings, tidy tables with f-strings, and the `file=` setting
- `input()`: ask a question, wait, and get the answer back
- Why `input` always returns a string, and how to convert it with `int()` and `float()`
- What a `ValueError` means, and how to clean what people type with `strip()`, `lower()` and `isdigit()`
- Where input works (REPL, terminal, VS Code), and one small receipt program plus a full enrolment form

## Before you start

- Python 3.14 or newer (`python --version`). Do [M02-L04](../m02-l04-true-false-and-none/) first.
- A terminal opened in this folder. For the programs that use `input()`, the lines marked as typed (the text after each question) are what you type and then press Enter.

## Files in this folder

| File | What it is |
|------|------------|
| `p_multi.py`, `p_sep.py`, `p_end.py` | Several pieces, `sep`, `end` |
| `p_ragged.py`, `p_table.py` | A ragged table, and the tidy f-string version |
| `p_err.py` | `print(..., file=sys.stderr)` |
| `in_hook.py`, `in_fix.py` | The opening mystery (`5` and `3` give `53`) and its fix with `int()` |
| `in_name.py`, `in_nospace.py` | A first `input`, and a question without the final space |
| `in_type.py`, `in_two.py`, `in_float.py` | `input` always gives a string; converting in two steps; `float` |
| `in_err.py` | The `ValueError` when the text is not a number |
| `in_clean.py` | `strip()` on what people type |
| `receipt.py` | A receipt maker (course, price, seats) |
| `enrol1.py`, `enrol.py` | The enrolment form: the first step, and the complete program |
| `pit_forgot.py`, `pit_add.py`, `pit_comma.py`, `pit_comma_fix.py`, `pit_space.py` | The pitfalls |

## Follow along

### 1. The mystery

A program asks for two numbers and adds them. The person types `5` and `3`:

**`in_hook.py`**

```python
first = input("First number: ")
second = input("Second number: ")
print(first + second)
```

```text
$ python in_hook.py
First number: 5
Second number: 3
53
```

Fifty-three, not eight. Python did exactly what it was told. By the end of the lesson you will know why.

### 2. print: several pieces, sep and end

`print` reads out each piece with a space in between, and turns a number into text for you:

**`p_multi.py`**

```python
print("Lukas", "enrolled in", 3, "courses")
```

```text
$ python p_multi.py
Lukas enrolled in 3 courses
```

The space between pieces is the separator, `sep`. Change it with a named setting:

**`p_sep.py`**

```python
print("22", "10", "2026", sep="/")
print("asha", "allcsvideos.com", sep="@")
print("Python", "Basics", sep="")
```

```text
$ python p_sep.py
22/10/2026
asha@allcsvideos.com
PythonBasics
```

When `print` finishes it adds a new line. That is the `end` setting, and you can change it too:

**`p_end.py`**

```python
print("Loading", end="... ")
print("done")
print(1, end=" ")
print(2, end=" ")
print(3)
print("Next")
```

```text
$ python p_end.py
Loading... done
1 2 3
Next
```

`sep` is what goes between the pieces, `end` is what goes after the last piece.

### 3. Tidy output

Printed the quick way, columns do not line up:

**`p_ragged.py`**

```python
print("Lesson", "Min")
print("Variables", 14)
print("Numbers", 18)
```

```text
$ python p_ragged.py
Lesson Min
Variables 14
Numbers 18
```

You know the cure from [M02-L03](../m02-l03-text-and-strings/): an f-string with a width. `<14` left-aligns in 14 places, `>6` right-aligns in 6, and `"-" * 20` makes a line:

**`p_table.py`**

```python
print("Lesson           Min")
print("-" * 20)
lesson, minutes = "Variables", 14
print(f"{lesson:<14}{minutes:>6}")
lesson, minutes = "Numbers", 18
print(f"{lesson:<14}{minutes:>6}")
print()
print("Keep going!")
```

```text
$ python p_table.py
Lesson           Min
--------------------
Variables         14
Numbers           18

Keep going!
```

Two more things. Special characters such as `\n` and `\t` work inside any `print`. And a program has two channels, one for normal output and one for errors. `print(..., file=sys.stderr)` uses the error channel. Both lines look the same on screen, the difference matters later when output is saved to a file:

**`p_err.py`**

```python
import sys

print("Saving report")
print("Disk almost full", file=sys.stderr)
```

```text
$ python p_err.py
Saving report
Disk almost full
```

### 4. input: ask and wait

`input("question")` shows the question, waits for the person to type and press Enter, and gives back what they typed. Put the answer in a label. The lines after each `:` below are typed by the person.

**`in_name.py`**

```python
name = input("Your name: ")
print("Welcome,", name)
```

```text
$ python in_name.py
Your name: Lukas
Welcome, Lukas
```

Notice the space at the end of the question (inside the quotes). Without it, the answer sticks to the colon:

**`in_nospace.py`**

```python
name = input("Your name:")
print("Welcome,", name)
```

```text
$ python in_nospace.py
Your name:Lukas
Welcome, Lukas
```

While `input` waits, your program is completely stopped. To quit without answering, press Ctrl + C. Python stops the program and shows a `KeyboardInterrupt`:

```text
$ python in_name.py
Your name: ^C
Traceback (most recent call last):
  File "in_name.py", line 1, in <module>
    name = input("Your name: ")
KeyboardInterrupt
```

`input` needs a person at the keyboard. A program on a server with nobody to type would fail with an `EOFError` instead.

### 5. input always returns a string

Find out what you really get back:

**`in_type.py`**

```python
age = input("Age: ")
print(type(age))
print(age * 2)
```

```text
$ python in_type.py
Age: 25
<class 'str'>
2525
```

Always a string, whatever the person types, like ink on a paper form: the form holds the characters `25`, not a number. So in the mystery, `first` held the text `"5"` and `second` the text `"3"`, and `+` joined them.

### 6. Convert with int and float

`int(...)` turns text into a whole number, `float(...)` into a number with a decimal part. Put it around `input`:

**`in_fix.py`**

```python
first = int(input("First number: "))
second = int(input("Second number: "))
print(first + second)
```

```text
$ python in_fix.py
First number: 5
Second number: 3
8
```

If the double brackets are hard to read, use two steps:

**`in_two.py`**

```python
text = input("Age: ")
age = int(text)
print(age + 1)
```

```text
$ python in_two.py
Age: 24
25
```

For numbers that can have a decimal part, use `float`:

**`in_float.py`**

```python
hours = float(input("Hours per week: "))
print(hours * 4)
```

```text
$ python in_float.py
Hours per week: 2.5
10.0
```

Pick with a question: can this number ever have a decimal part? An age, a number of seats or a price in whole rupees is an `int`. Hours or a weight is a `float`.

### 7. When the text is not a number

**`in_err.py`**

```python
age = int(input("Age: "))
print("Next year you will be", age + 1)
print("Thanks!")
```

```text
$ python in_err.py
Age: twenty five
Traceback (most recent call last):
  File "in_err.py", line 1, in <module>
    age = int(input("Age: "))
ValueError: invalid literal for int() with base 10: 'twenty five'
```

The program stopped and the last two lines never ran. Read the last line first: `ValueError` means the kind of thing you gave (text) is right, but its content is wrong, because `int` cannot make a whole number from `'twenty five'` (a literal is a value written in code). The lines above show where.

`int` and `float` are strict: they accept only text that already looks like a number. Module 6 shows how to avoid the crash with `try` and `except`.

### 8. Clean what people type

People type extra spaces and odd capitals. `strip()` removes spaces at both ends. The brackets in this output show the spaces:

**`in_clean.py`**

```python
raw = input("Name: ")
name = raw.strip()
print(f"[{raw}]")
print(f"[{name}]")
```

```text
$ python in_clean.py
Name:    Lukas Weber  
[   Lukas Weber  ]
[Lukas Weber]
```

You can chain it: `input("Name: ").strip()`. A string also has a method `isdigit()`, which says `True` if the text is not empty and made only of digits:

```text
>>> "25".isdigit()
True
>>> "twenty".isdigit()
False
>>> "".isdigit()
False
>>> "3.5".isdigit()
False
>>> "-5".isdigit()
False
```

It is a light check. It works for whole, positive numbers such as an age, and is wrong for `-5` or `3.5`. To act on the answer (for example to ask again) you need `if` and loops, in Module 3.

### 9. Where input works

The rule is the same everywhere: type your answer in the same place the question appears.

- In the REPL: `name = input("Your name: ")`, then type the answer at the prompt.
- In a file, from the terminal: `python in_name.py`, and answer when the question shows.
- In VS Code: press the run button. The terminal panel opens at the bottom, and you must click inside it and type there.

The most common beginner confusion is typing the answer into the editor instead of the terminal.

### 10. A first small program: the receipt

Asha wants a receipt maker for the helpdesk. Line 1 reads the course name, lines 2 and 3 convert price and seats with `int`, then the maths uses `//` for the whole-rupee GST, and the rows are f-strings.

```python
course = input("Course: ")
price = int(input("Price in rupees: "))
seats = int(input("Seats: "))

subtotal = price * seats
gst = subtotal * 18 // 100
total = subtotal + gst

print()
print("RECEIPT")
print("-" * 26)
print(f"{course:<14}{subtotal:>12,}")
print(f"{'GST 18%':<14}{gst:>12,}")
print(f"{'Total':<14}{total:>12,}")
```

The clerk types `Python Basics`, `1499` and `2` seats:

```text
$ python receipt.py
Course: Python Basics
Price in rupees: 1499
Seats: 2

RECEIPT
--------------------------
Python Basics        2,998
GST 18%                539
Total                3,537
```

### 11. The finale: the enrolment form

A new student sits at the enrolment desk. The program asks, listens, cleans, converts, calculates and answers. First step, the title and two questions (name and email, cleaned with `strip()` and `lower()`):

**`enrol1.py`**

```python
print("=== allcsvideos enrolment ===")
name = input("Full name: ").strip()
email = input("Email: ").strip().lower()
print(name)
print(email)
```

```text
$ python enrol1.py
=== allcsvideos enrolment ===
Full name:    Lukas Weber  
Email: Lukas@Mail.com 
Lukas Weber
lukas@mail.com
```

Now the complete program. Every idea in it came from this module:

```python
print("=== allcsvideos enrolment ===")
name = input("Full name: ").strip()
email = input("Email: ").strip().lower()
age_text = input("Age: ").strip()
course = input("Course: ").strip()
fee = int(input("Fee in rupees: ").replace(",", ""))
hours = float(input("Hours per week: "))

print()
print("Age is a number:", age_text.isdigit())
age = int(age_text)
gst = fee * 18 // 100
total = fee + gst

print("Saving", end="... ")
print("done")
print("-" * 30)
print("Name   :", name)
print("Email  :", email)
print("Age    :", age)
print("Course :", course)
print(f"Fee    : {fee:>8,}")
print(f"GST 18%: {gst:>8,}")
print(f"Total  : {total:>8,}")
print("Weekly :", hours, "hours")
```

A student types a messy name, email, age with a space, the fee with a comma, and hours:

```text
$ python enrol.py
=== allcsvideos enrolment ===
Full name:    Lukas Weber  
Email: Lukas@Mail.com 
Age: 24 
Course: Python Basics
Fee in rupees: 1,499
Hours per week: 2.5

Age is a number: True
Saving... done
------------------------------
Name   : Lukas Weber
Email  : lukas@mail.com
Age    : 24
Course : Python Basics
Fee    :    1,499
GST 18%:      269
Total  :    1,768
Weekly : 2.5 hours
```

The name is clean, the email is lower case, the fee comma was removed, and the GST and total are right. Now a second student types the age in words:

```text
$ python enrol.py
=== allcsvideos enrolment ===
Full name: Lukas Weber
Email: lukas@mail.com
Age: twenty-four
Course: Python Basics
Fee in rupees: 1499
Hours per week: 2.5

Age is a number: False
Traceback (most recent call last):
  File "enrol.py", line 11, in <module>
    age = int(age_text)
ValueError: invalid literal for int() with base 10: 'twenty-four'
```

`Age is a number: False`. Our check noticed, but the program does not act on it, so the next line crashes. Module 3 teaches `if` and loops, which will let the program ask again.

## Interview tip

"What does `input` return, and what do you do with it?" It always returns a string, whatever the user types. I convert it with `int` or `float` when I need a number, and I clean it with `strip()` and `lower()` first.

## Common mistakes

- Forgetting `int`. With text, `*` repeats and `+` joins, so no error appears:

**`pit_forgot.py`**

```python
price = input("Price: ")
seats = 3
print("Total:", price * seats)
```

```text
$ python pit_forgot.py
Price: 499
Total: 499499499
```

- The loud version, `price + 100`:

**`pit_add.py`**

```python
price = input("Price: ")
print(price + 100)
```

```text
$ python pit_add.py
Price: 499
Traceback (most recent call last):
  File "pit_add.py", line 2, in <module>
    print(price + 100)
          ~~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
```

- Commas in a number. `int("1,499")` is a `ValueError`:

**`pit_comma.py`**

```python
fee = int(input("Fee: "))
print(fee)
```

```text
$ python pit_comma.py
Fee: 1,499
Traceback (most recent call last):
  File "pit_comma.py", line 1, in <module>
    fee = int(input("Fee: "))
ValueError: invalid literal for int() with base 10: '1,499'
```

Remove the comma first with `replace`:

**`pit_comma_fix.py`**

```python
fee = int(input("Fee: ").replace(",", ""))
print(fee)
```

```text
$ python pit_comma_fix.py
Fee: 1,499
1499
```

- Extra spaces. `"Lukas "` is not `"Lukas"` until you `strip()`:

**`pit_space.py`**

```python
name = input("Name: ")
print(name == "Lukas")
print(name.strip() == "Lukas")
```

```text
$ python pit_space.py
Name: Lukas 
False
True
```

- Forgetting the space at the end of the question, and thinking a program is frozen when it is just waiting for `input`.

## Clean up

Nothing to clean up.

## Next

You have finished the lessons of Module 2. Practise with the [M02 practice sheet](../../practice/m02-variables-and-data-types/), then continue with [M03-L01 · Making Decisions with if](../../m03-decisions-and-loops/m03-l01-making-decisions-with-if/).
