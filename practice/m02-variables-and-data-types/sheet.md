# Module 02 · Practice Sheet: 20 Beginner Python Exercises

Write each program yourself before you open the answer. Every exercise is a small Python file you can run in the terminal, and nothing here needs more than Module 2.

**How to work:**
- Use **Python 3.14** (check with `python --version`; on Mac or Linux the command may be `python3`).
- Put each program in its own file, `Ex01.py` to `Ex20.py`. Run it with **`python Ex01.py`**.
- The exercises use the allcsvideos platform and its cast: Asha, Lukas, Priya, Meera and Rahul. Money is written as **Rs**.
- They go from easy to harder, **about four per lesson**. Some are **predict the output** (guess on paper first, then run), some are **fix the broken code** (read the error, then repair it), and some build a small program.
- Each answer has a hint, a full solution, and the **real output** from running it with Python 3.14. Open the hint first, and only then the solution.
- All 20 solutions are in the folder **`solutions/`** next to this sheet. Run them with `python Ex07.py` from inside that folder.
- Exercises 19 and 20 use `input()`. Each one shows a sample session, and a way to test it without typing: pipe the answers in with `printf '5\n3\n' | python Ex19.py`.

---

## M02 · L01 Variables as Labels on Boxes

### 1 · Four labels, five lines
Asha is building the student card for allcsvideos. In one file, create **four labels** (variables):

| label | value |
|---|---|
| `student_name` | the text `Asha` |
| `course_name` | the text `Python Basics` |
| `lessons_completed` | the number `12` |
| `price` | the number `1499` |

Then write **five** `print` lines, using the labels (no quotes around a label):

1. the heading `Student:` followed by the student name
2. the heading `Course:` and the course name
3. the heading `Lessons done:` and the number of lessons
4. the heading `Price: Rs` and the price
5. a sentence made from the labels: `Asha is learning Python Basics`

**Expected output:**

```text
Student: Asha
Course: Python Basics
Lessons done: 12
Price: Rs 1499
Asha is learning Python Basics
```

Now change **only line 1** so the student is `Lukas`, save and run again. Two of the five output lines should change. Which two?

### 2 · Predict the output (reassigning)
**Do not run it yet.** Read this file and write down, on paper, what each of the five `print` lines shows. Then run it and compare.

```python
lessons_completed = 12
lessons_completed = lessons_completed + 1
lessons_completed = lessons_completed + 1
print(lessons_completed)

lessons_backup = lessons_completed
lessons_completed = 20
print(lessons_backup, lessons_completed)

quizzes_passed = quizzes_failed = 0
quizzes_passed = 5
print(quizzes_passed, quizzes_failed)

lessons_done, lessons_total = 12, 104
print(lessons_done, "of", lessons_total)
print(type(lessons_done), type(lessons_done / lessons_total))
```

Save it as `Ex02.py` and run it. The last line uses a result from Module 2 lesson 2 (what does `/` give?).

### 3 · Fix the broken names
Meera sent you five tiny files. **Each one crashes.** For each, read the error, find the rule that was broken, and fix it. Then put the five fixed versions together in one file and check that it prints what is shown below.

```python
# file a
2nd_course = "Python"
print(2nd_course)
```
```python
# file b
course name = "Spring Boot"
print(course name)
```
```python
# file c
class = "A"
print(class)
```
```python
# file d
Price = 1499
print(price)
```
```python
# file e
print = "Lukas"
print("Hello")
```

What Python says (last lines only):

```text
a: SyntaxError: invalid decimal literal
b: SyntaxError: invalid syntax            (the ^^^^ marks "name")
c: SyntaxError: invalid syntax            (the ^ marks the =)
d: NameError: name 'price' is not defined. Did you mean: 'Price'?
e: TypeError: 'str' object is not callable
```

**Expected output of your repaired file:**

```text
Python
Spring Boot
A
1499
Hello Lukas
```

### 4 · Swap two labels
Asha sits in seat label `first` and Lukas in `second`, and they must swap. This broken swap loses a value:

```python
first = "Asha"
second = "Lukas"
first = second
second = first
print(first, second)
```

It prints `Lukas Lukas`. Fix it **two ways** in one file, printing after each swap:

1. with a third helper label called `temp`
2. with the one-line trick `a, b = b, a` (swap them back)

**Expected output:**

```text
After helper swap: Lukas Asha
After one-line swap: Asha Lukas
```

## M02 · L02 Numbers

### 5 · Predict the output (operators)
**Do not run it first.** Write down what each line prints, in order. There are 12 `print` lines, and some print more than one value.

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
print(10 / 2)
print(7 / 2)
print(17 // 5)
print(17 % 5)
print(2 ** 10)
print(10 % 2, 7 % 2)
print(round(2.5), round(3.5), round(3.14159, 2))
print(int(3.99))
print(divmod(17, 5))
print(type(5), type(5.0))
```

Save it as `Ex05.py`, run it and mark your wrong guesses. For each wrong guess, say which lesson idea you forgot.

### 6 · GST in whole paise, and pages
The Python course costs Rs 1,999, which is **199900 paise**. Never keep money in a float, so do all the work in whole paise.

1. Work out the 18 percent GST in paise (use `*` and `//`), the total in paise, and then use `divmod` to split the total into rupees and paise.
2. The site shows 10 lessons per page and the course has 47 lessons. Use `import math` and `math.ceil` to find how many pages are needed.

**Expected output:**

```text
Tax: 35982 paise
Total: 235882 paise
That is Rs 2358 and 82 paise
Pages needed: 5
```

### 7 · Priya's shopping cart
Priya fills her cart on allcsvideos. Start a label `cart` at 0 and use the **shortcut operators** (`+=`, `-=`, `*=`) for every change. Print the cart after each step.

1. Start: 0
2. Add the Python course, 1999
3. Add the Spring Boot course, 1499
4. A coupon takes off 300
5. A friend buys the same cart, so double it

Finish with three helper calls: the cheapest and priciest of the prices 1999, 1499, 2999 (`min`, `max`), and the size of a refund of -250 (`abs`).

**Expected output:**

```text
Start: 0
After Python course: 1999
After Spring Boot course: 3498
After coupon: 3198
After doubling: 6396
Cheapest: 1499
Priciest: 2999
Refund size: 250
```

### 8 · The famous decimal surprise
Run `0.1 + 0.2` in a file and print the result. It is **not** `0.3`. Write a file that:

1. prints the sum
2. prints the answer to the question "is the sum exactly `0.3`?" (`==`)
3. prints the answer when you ask with `math.isclose`
4. prints the sum using `Decimal("0.1") + Decimal("0.2")` (use `from decimal import Decimal`, and give it **text**)
5. prints `10 + 20` as the same sum in whole paise

**Expected output:**

```text
Sum: 0.30000000000000004
Exactly 0.3? False
Close to 0.3? True
Decimal sum: 0.3
Paise sum: 30 paise
```

## M02 · L03 Text and Strings

### 9 · Predict the output (indexing and slicing)
**Write your guesses first.** Here the label `name` holds the text `Python`. Predict each of the 11 lines.

```python
name = "Python"
print(name[0])
print(name[-1])
print(name[2:5])
print(name[:3])
print(name[2:])
print(name[::2])
print(name[::-1])
print(name[0:100])
print(len(name))
print(len("a b"))
print(len(""))
```

Run it. Draw the beads P y t h o n with the numbers 0 to 5 under them and the "lines" 0 to 6 between them if you get stuck.

### 10 · Fix the broken string code
Five more broken programs. Run each, read the problem, and fix it. The first, third and fourth ones **crash**; the second and fifth have a different problem, so read the output carefully.

```python
# file a
name = "Python"
name[0] = "J"
print(name)
```
```python
# file b
title = "python basics"
title.upper()
print(title)
```
```python
# file c
student = "Asha"
print("Hello, {student}")
```
```python
# file d
total = 1768.82
print("Total: " + total)
```
```python
# file e
name = "Python"
print(name[len(name)])
```

What Python says:

```text
a: TypeError: 'str' object does not support item assignment
b: (no error) prints   python basics   - still small letters
c: (no error) prints   Hello, {student}
d: TypeError: can only concatenate str (not "float") to str
e: IndexError: string index out of range
```

**Goal after fixing all five** (put the repaired versions in one file, in the same order):

```text
Jython
PYTHON BASICS
Hello, Asha
Total: 1768.82
n
```

### 11 · A receipt for Priya
Priya bought **Python Basics** for Rs 1499, and 18 percent tax is added. Print this receipt using **f-strings** with alignment and number formats. The whole receipt is 30 characters wide.

**Expected output:**

```text
==============================
           RECEIPT            
==============================
Student: Priya
Python Basics         1,499.00
GST 18%                 269.82
Total                 1,768.82
==============================
```

Rules: the border is `"=" * 30`. `RECEIPT` is centred in width 30. The label columns are left-aligned in width 20, the amounts right-aligned in width 10, with a thousands comma and two decimals.

### 12 · Clean what people type
Lukas typed three things in a hurry:

```python
raw_name = "   lUKAS     wEBER  "
raw_email = "  Lukas@Mail.COM "
raw_title = "  Python   FOR  Absolute   Beginners "
```

Use only string methods to produce these results. Do **not** type the answers by hand.

- `name`: single spaces, Title Case
- `email`: no outer spaces, all small letters
- print whether the email contains an `@`, and whether it ends with `mail.com`
- `slug`: the title in small letters, words joined by dashes
- a page address built with an f-string, and the length of the slug

**Expected output:**

```text
Name: Lukas Weber
Email: lukas@mail.com
Has an @: True
Ends with mail.com: True
Slug: python-for-absolute-beginners
Address: allcsvideos.com/courses/python-for-absolute-beginners
Slug length: 29
```

## M02 · L04 True, False and None

### 13 · Predict the output (comparisons)
**Guess first.** There are 14 values printed. Write `True` or `False` for each.

```python
price = 499
budget = 500
print(price == 499)
print(price != 499)
print(price < budget)
print(price >= budget)
print("Python" == "python")
print(5 == 5.0)
print(5 == "5")
print("apple" < "banana")
print("ten" < "nine")
rating = 4
print(1 <= rating <= 5)
rating = 7
print(1 <= rating <= 5)
is_enrolled = True
has_paid = False
print(is_enrolled and has_paid, is_enrolled or has_paid, not has_paid)
```

### 14 · Truthy or falsy?
For each line, say whether Python prints `True` or `False` **before** you run it. Then run it.

```python
print(bool(0))
print(bool(7))
print(bool(-3))
print(bool(0.0))
print(bool(""))
print(bool("hi"))
print(bool(" "))
print(bool("False"))
print(bool([]))
print(bool([1, 2, 3]))
print(bool(None))
print(True + True)
print(int(False))
```

Then finish this sentence in your own words: "Python counts these as no: ______. Everything else counts as yes."

### 15 · Fix the broken yes/no code
Four problems. Run them, read the message, and fix them.

```python
# file a
is_enrolled = true
print(is_enrolled)
```
```python
# file b
499 = price
```
```python
# file c   (answer is typed text, like input() would give)
answer = "False"
print(bool(answer))
```
```python
# file d
seats = None
print(seats + 1)
```

What Python says:

```text
a: NameError: name 'true' is not defined. Did you mean: 'True'?
b: SyntaxError: cannot assign to literal here. Maybe you meant '==' instead of '='?
c: (no error) prints   True   - but the student answered False!
d: TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

Your fixed file should print:

```text
Price is 499? True
False
1
```

### 16 · Nothing here yet
Lukas has just enrolled, so his certificate does not exist yet. Write a file that:

1. sets `certificate` to `None` and prints it and its type
2. prints whether `certificate is None`
3. prints whether `certificate == 0` and whether `certificate == ""` (two answers on one line)
4. prints `bool(certificate)`
5. sets `certificate` to the text `CERT-0042` and prints `certificate is None`, then `certificate is not None`
6. stores the result of `print("Welcome, Lukas")` in `result` and prints `result`

**Expected output:**

```text
None
<class 'NoneType'>
True
False False
False
False
True
Welcome, Lukas
None
```

## M02 · L05 Input and Output

### 17 · sep and end
`print` has two hidden settings: `sep` (what goes between pieces, default a space) and `end` (what goes after the last piece, default a new line). Write a file whose output is exactly:

```text
Lukas enrolled in 3 courses
22/10/2026
asha@allcsvideos.com
PythonBasics
Loading... done
1 2 3
Next
```

Use these rules: the first line passes four pieces (one of them is the **number** 3). The date uses `sep="/"` with three numbers. The email uses `sep="@"`. `PythonBasics` is two pieces with an empty separator. `Loading... done` is two `print` calls, the first with `end="... "`. The `1 2 3` line is three calls, the first two with `end=" "`.

### 18 · A tidy table
Print this table of lesson lengths. No `input` is needed. The name column is **14 wide, left-aligned**; the minutes column is **6 wide, right-aligned**; the dash line is 20 dashes; the blank line is an empty `print()`; the total is calculated by Python (do not type 54 by hand).

```text
Lesson           Min
--------------------
Variables         12
Numbers           15
Text              18
Booleans           9

Total             54
```

### 19 · The 53 mystery, fixed
This program has an old problem. It is meant to add two numbers:

```python
first = input("First number: ")
second = input("Second number: ")
print(first + second)
```

**Sample session** (what you see in the terminal; `5` and `3` are typed by the person):

```text
First number: 5
Second number: 3
53
```

It prints `53`, not `8`. Write `Ex19.py` so that it prints `Total: 8` for those inputs. Then add a third question, `Hours per week: `, read with `float`, and print `In four weeks:` followed by the hours times 4. (Typing `2.5` should give `10.0`.)

**Expected session:**

```text
First number: 5
Second number: 3
Total: 8
Hours per week: 2.5
In four weeks: 10.0
```

**How to test without typing.** Pipe the answers in, one per line:

```bash
printf '5\n3\n2.5\n' | python Ex19.py
```

Because the answers are not typed on the screen, the questions appear side by side on one line. That is normal. In a real session, run `python Ex19.py` and type the answers yourself. Also try typing `twenty five` for the first number. What error do you get, and what does the last line say?

### 20 · The allcsvideos enrolment form
Build the finale: a complete enrolment form. The program asks **six questions** and prints a confirmation. Requirements:

1. `Full name: ` read as text; squeeze extra spaces and use Title Case.
2. `Email: ` stripped and in small letters.
3. `Age: ` read as text and stripped; print `Age is a number:` with the answer of `.isdigit()`, then convert to `int`.
4. `Course: ` stripped.
5. `Fee in Rs: ` read as text, commas removed with `replace`, converted to `int`.
6. `Hours per week: ` converted with `float`.
7. GST is 18 percent of the fee, **in whole rupees** (floor division). Total = fee + GST.
8. Print `Saving` with `end="... "`, then `done`, then a line of 30 dashes, the labelled details (labels padded to 8 characters so the colons line up; amounts right-aligned in 8 places with commas), and a closing line of dashes.

**Sample session** (answers typed by the person are after each question):

```text
ALLCSVIDEOS ENROLMENT
Full name:   lukas   weber  
Email:   Lukas@Mail.COM 
Age: 24 
Course: Python Basics
Fee in Rs: 1,499
Hours per week: 2.5
Age is a number: True
Saving... done
------------------------------
Name    : Lukas Weber
Email   : lukas@mail.com
Age     : 24 (next year 25)
Course  : Python Basics
Hours   : 2.5 per week
Fee     : Rs    1,499
GST     : Rs      269
Total   : Rs    1,768
------------------------------
```

**Test it with piped input** (`printf` sends each `\n`-separated answer to one `input`):

```bash
printf '  lukas   weber  \n  Lukas@Mail.COM \n24 \nPython Basics\n1,499\n2.5\n' | python Ex20.py
```

In the piped output the questions appear side by side, because the answers are not echoed to the screen.

---

## Answers

Click an exercise to open its solution. Your code does not have to match line for line; it should produce the same output.

<details>
<summary><b>1 · Four labels, five lines</b></summary>

**Hint.** Text goes in quotes, numbers do not, and labels never have quotes. `print("Student:", student_name)` prints the heading, then looks up the label. `print` puts one space between the pieces for you.

A variable is a label stuck on a value. One `=` means "store". Every `print` line that uses `student_name` follows the change, which is the whole point of a variable. After changing line 1 to `Lukas`, lines 1 and 5 change (`Student: Lukas` and `Lukas is learning Python Basics`).

`solutions/Ex01.py`, run with `python Ex01.py`:

```python
# Exercise 01 - Four labels, five lines
student_name = "Asha"
course_name = "Python Basics"
lessons_completed = 12
price = 1499

print("Student:", student_name)
print("Course:", course_name)
print("Lessons done:", lessons_completed)
print("Price: Rs", price)
print(student_name, "is learning", course_name)
```

Output (Python 3.14):

```text
Student: Asha
Course: Python Basics
Lessons done: 12
Price: Rs 1499
Asha is learning Python Basics
```

</details>

<details>
<summary><b>2 · Predict the output (reassigning)</b></summary>

**Hint.** Python always works out the **right side first**, then moves the label. `lessons_backup = lessons_completed` copies the value the label has at that moment; it does not link the two labels together. Moving one label later does not drag the other one.

Line by line: 12, then 13, then 14, so the first print shows `14`. The backup took the value 14, so after `lessons_completed` moves to 20 the backup still says 14. `quizzes_passed = quizzes_failed = 0` put two labels on one zero, but moving `quizzes_passed` to 5 leaves `quizzes_failed` on 0. The last line shows that `12` is an `int` and that `/` always gives a `float`.

`solutions/Ex02.py`, run with `python Ex02.py`:

```python
# Exercise 02 - Predict the output
lessons_completed = 12
lessons_completed = lessons_completed + 1
lessons_completed = lessons_completed + 1
print(lessons_completed)

lessons_backup = lessons_completed
lessons_completed = 20
print(lessons_backup, lessons_completed)

quizzes_passed = quizzes_failed = 0
quizzes_passed = 5
print(quizzes_passed, quizzes_failed)

lessons_done, lessons_total = 12, 104
print(lessons_done, "of", lessons_total)
print(type(lessons_done), type(lessons_done / lessons_total))
```

Output (Python 3.14):

```text
14
14 20
5 0
12 of 104
<class 'int'> <class 'float'>
```

</details>

<details>
<summary><b>3 · Fix the broken names</b></summary>

**Hint.** There are four naming rules: only letters, digits and underscores; cannot start with a digit; case matters; cannot be a keyword. File e breaks no naming rule at all: it peels the label `print` off the helper that prints. Pick a different label for the text `Lukas`.

Fixes: `2nd_course` becomes `first_course` (rule 2), `course name` becomes `course_name` (rule 1, join with an underscore), `class` becomes `class_name` (rule 4, keyword), `Price`/`price` made the same (rule 3, case), and in file e the text goes into a new label `greeting` so that `print` stays the helper. Your labels may be named differently from mine; what matters is that the output matches.

`solutions/Ex03.py`, run with `python Ex03.py`:

```python
# Exercise 03 - Fix the broken names (all five repaired)
first_course = "Python"       # was: 2nd_course  (cannot start with a digit)
course_name = "Spring Boot"   # was: course name (no spaces)
class_name = "A"              # was: class       (a keyword)
price = 1499                  # was: Price assigned, price printed (case matters)
greeting = "Lukas"            # was: print = "Lukas" (hid the print helper)

print(first_course)
print(course_name)
print(class_name)
print(price)
print("Hello", greeting)
```

Output (Python 3.14):

```text
Python
Spring Boot
A
1499
Hello Lukas
```

</details>

<details>
<summary><b>4 · Swap two labels</b></summary>

**Hint.** Think of two cups, coffee and tea: you need a third, empty cup. Save the first value in `temp` before you overwrite it. For the one-liner, the right side is worked out first, then both labels move at the same time.

In the broken version `first = second` moves the label `first` onto "Lukas" and nobody holds "Asha" any more, so it is lost. The helper label `temp` keeps it safe. The one-line swap `first, second = second, first` works because Python builds the pair on the right before moving any label.

`solutions/Ex04.py`, run with `python Ex04.py`:

```python
# Exercise 04 - Swap two labels without losing a value
first = "Asha"
second = "Lukas"

# Way 1: a helper label
temp = first
first = second
second = temp
print("After helper swap:", first, second)

# Way 2: the one-line swap
first, second = second, first
print("After one-line swap:", first, second)
```

Output (Python 3.14):

```text
After helper swap: Lukas Asha
After one-line swap: Asha Lukas
```

</details>

<details>
<summary><b>5 · Predict the output (operators)</b></summary>

**Hint.** Remember: `*` before `+`; `/` always gives a float; `//` is "how many whole sweets each", `%` is "how many left over"; `int` chops, it does not round; `round` of an exact half picks the **even** neighbour (banker's rounding).

`2 + 3 * 4` is 14 (star first), but with brackets it is 20. `10 / 2` is `5.0` (a float). `17 // 5` is 3 and `17 % 5` is 2: seventeen sweets among five children. `10 % 2` is 0 (even) and `7 % 2` is 1 (odd). `round(2.5)` is 2 and `round(3.5)` is 4, because exact halves go to the even number. `int(3.99)` is 3. `divmod` gives both sweets answers in one pair.

`solutions/Ex05.py`, run with `python Ex05.py`:

```python
# Exercise 05 - Predict the numbers
print(2 + 3 * 4)
print((2 + 3) * 4)
print(10 / 2)
print(7 / 2)
print(17 // 5)
print(17 % 5)
print(2 ** 10)
print(10 % 2, 7 % 2)
print(round(2.5), round(3.5), round(3.14159, 2))
print(int(3.99))
print(divmod(17, 5))
print(type(5), type(5.0))
```

Output (Python 3.14):

```text
14
20
5.0
3.5
3
2
1024
0 1
2 4 3.14
3
(3, 2)
<class 'int'> <class 'float'>
```

</details>

<details>
<summary><b>6 · GST in whole paise, and pages</b></summary>

**Hint.** `tax = price * 18 // 100`, `total = price + tax`, `rupees, paise = divmod(total, 100)`. For pages: 47 / 10 is 4.7, and you must round **up**. Print with commas: `print("Tax:", tax, "paise")`.

Floor division keeps whole paise and never creates a float, so every step is exact. `divmod(235882, 100)` answers "how many whole rupees" and "how many paise left over" in one go. `math.ceil(4.7)` is 5, because four pages would hide seven lessons.

`solutions/Ex06.py`, run with `python Ex06.py`:

```python
# Exercise 06 - GST in whole paise, and pages
import math

price_paise = 199900                      # Rs 1,999
tax_paise = price_paise * 18 // 100       # whole paise, no float
total_paise = price_paise + tax_paise
rupees, paise = divmod(total_paise, 100)

print("Tax:", tax_paise, "paise")
print("Total:", total_paise, "paise")
print("That is Rs", rupees, "and", paise, "paise")

lessons = 47
per_page = 10
pages = math.ceil(lessons / per_page)
print("Pages needed:", pages)
```

Output (Python 3.14):

```text
Tax: 35982 paise
Total: 235882 paise
That is Rs 2358 and 82 paise
Pages needed: 5
```

</details>

<details>
<summary><b>7 · Priya's shopping cart</b></summary>

**Hint.** `cart += 1999` means exactly `cart = cart + 1999`: work out the right side with the current value, then move the label to the answer.

Each shortcut reads the current value of `cart`, computes the result, and puts the answer back into the same label. 0, 1999, 3498, 3198, 6396. `min` and `max` take any number of values, and `abs` removes the minus sign.

`solutions/Ex07.py`, run with `python Ex07.py`:

```python
# Exercise 07 - Priya's shopping cart
cart = 0
print("Start:", cart)

cart += 1999        # Python course
print("After Python course:", cart)

cart += 1499        # Spring Boot course
print("After Spring Boot course:", cart)

cart -= 300         # coupon
print("After coupon:", cart)

cart *= 2           # a friend buys the same cart
print("After doubling:", cart)

print("Cheapest:", min(1999, 1499, 2999))
print("Priciest:", max(1999, 1499, 2999))
print("Refund size:", abs(-250))
```

Output (Python 3.14):

```text
Start: 0
After Python course: 1999
After Spring Boot course: 3498
After coupon: 3198
After doubling: 6396
Cheapest: 1499
Priciest: 2999
Refund size: 250
```

</details>

<details>
<summary><b>8 · The famous decimal surprise</b></summary>

**Hint.** Floats are stored in binary, and one tenth has no exact binary form, so there is a tiny error. Fix 1: ask "close enough?" with `math.isclose(a, b)`. Fix 2: `decimal` stores digits as we write them, so hand it text in quotes. Fix 3: store money as whole paise.

This is not a Python bug: Java, JavaScript and C give the same answer. The `==` check is `False` because of the tiny error, `math.isclose` forgives it, `Decimal` is exact (but slower), and whole numbers in paise are always exact. The professional rule: never store money in a float.

`solutions/Ex08.py`, run with `python Ex08.py`:

```python
# Exercise 08 - The famous decimal surprise
import math
from decimal import Decimal

total = 0.1 + 0.2
print("Sum:", total)
print("Exactly 0.3?", total == 0.3)                    # the broken check
print("Close to 0.3?", math.isclose(total, 0.3))       # fix 1
print("Decimal sum:", Decimal("0.1") + Decimal("0.2")) # fix 2
print("Paise sum:", 10 + 20, "paise")                  # fix 3: whole numbers
```

Output (Python 3.14):

```text
Sum: 0.30000000000000004
Exactly 0.3? False
Close to 0.3? True
Decimal sum: 0.3
Paise sum: 30 paise
```

</details>

<details>
<summary><b>9 · Predict the output (indexing and slicing)</b></summary>

**Hint.** The first character is index 0. A slice `[start:stop]` cuts at two lines and **leaves out** the stop. A missing start means the beginning, a missing stop the end, and `[::-1]` walks backwards. A space is a character, and the empty string has no characters.

`name[2:5]` starts at line 2 and stops at line 5, so it keeps `t`, `h`, `o` (stop minus start is the length, 3). `name[::2]` jumps by two: P, t, o. `name[::-1]` reverses the string. A slice never causes an index error, so `name[0:100]` simply gives all of Python. `len("a b")` is 3 because the space is a bead too, and the empty string has length 0.

`solutions/Ex09.py`, run with `python Ex09.py`:

```python
# Exercise 09 - Predict: indexing and slicing
name = "Python"
print(name[0])
print(name[-1])
print(name[2:5])
print(name[:3])
print(name[2:])
print(name[::2])
print(name[::-1])
print(name[0:100])
print(len(name))
print(len("a b"))
print(len(""))
```

Output (Python 3.14):

```text
P
n
tho
Pyt
thon
Pto
nohtyP
Python
6
3
0
```

</details>

<details>
<summary><b>10 · Fix the broken string code</b></summary>

**Hint.** a: strings cannot be changed, so build a new one from pieces (`"J"` plus a slice). b: string methods return a **new** string; keep it with a label. c: one letter is missing before the opening quote. d: use a comma in `print`, or an f-string. e: the last index is `len(name) - 1`, or simply `-1`.

a: a string is immutable, so `"J" + name[1:]` builds a new string and puts a label on it. b: `title.upper()` made capitals, but nobody kept them, so assign `title = title.upper()`. c: without the `f` there is no filling-in, and curly braces print as plain text. d: Python refuses to guess whether `+` should add or join. e: `len` is 6 but the last index is 5, a classic off-by-one.

`solutions/Ex10.py`, run with `python Ex10.py`:

```python
# Exercise 10 - Fix the broken string code (all five repaired)
name = "Python"
new_name = "J" + name[1:]          # strings cannot be changed, build a new one
print(new_name)

title = "python basics"
title = title.upper()              # keep the result with a label
print(title)

student = "Asha"
print(f"Hello, {student}")         # the f was missing

total = 1768.82
print("Total:", total)             # or: print(f"Total: {total}")

print(name[len(name) - 1])         # last index is len - 1 (or just name[-1])
```

Output (Python 3.14):

```text
Jython
PYTHON BASICS
Hello, Asha
Total: 1768.82
n
```

</details>

<details>
<summary><b>11 · A receipt for Priya</b></summary>

**Hint.** Format rules go after a colon inside the braces: `^30` centres in 30 places, `<20` left-aligns in 20, `>10` right-aligns in 10, and `,.2f` means thousands comma plus two decimals. For a fixed word inside the braces, put it in the *other* kind of quotes: `{'RECEIPT':^30}`.

Compute `tax = price * 0.18` and `total = price + tax` first, then each row is one f-string. The right edges line up because every amount uses the same width. (The line `RECEIPT` has trailing spaces, because centring pads on both sides.)

`solutions/Ex11.py`, run with `python Ex11.py`:

```python
# Exercise 11 - A receipt for Priya
student = "Priya"
course = "Python Basics"
price = 1499
tax = price * 0.18
total = price + tax

print("=" * 30)
print(f"{'RECEIPT':^30}")
print("=" * 30)
print(f"Student: {student}")
print(f"{course:<20}{price:>10,.2f}")
print(f"{'GST 18%':<20}{tax:>10,.2f}")
print(f"{'Total':<20}{total:>10,.2f}")
print("=" * 30)
```

Output (Python 3.14):

```text
==============================
           RECEIPT            
==============================
Student: Priya
Python Basics         1,499.00
GST 18%                 269.82
Total                 1,768.82
==============================
```

</details>

<details>
<summary><b>12 · Clean what people type</b></summary>

**Hint.** `split()` with no argument cuts at every run of spaces and drops the empty pieces. `" ".join(pieces)` glues them back with one space (the string in front is the glue). For the email: `strip()` then `lower()`. For the slug: `lower()`, `split()`, then `"-".join(...)`.

Methods return new strings, so chaining reads left to right: `raw_email.strip().lower()`. `split` plus `join` is the standard way to squeeze extra spaces. Words in quotes `in` a string, and `startswith`/`endswith`, answer yes or no with `True` or `False`.

`solutions/Ex12.py`, run with `python Ex12.py`:

```python
# Exercise 12 - Clean what people type
raw_name = "   lUKAS     wEBER  "
raw_email = "  Lukas@Mail.COM "
raw_title = "  Python   FOR  Absolute   Beginners "

name = " ".join(raw_name.split()).title()
email = raw_email.strip().lower()
slug = "-".join(raw_title.lower().split())

print("Name:", name)
print("Email:", email)
print("Has an @:", "@" in email)
print("Ends with mail.com:", email.endswith("mail.com"))
print("Slug:", slug)
print(f"Address: allcsvideos.com/courses/{slug}")
print("Slug length:", len(slug))
```

Output (Python 3.14):

```text
Name: Lukas Weber
Email: lukas@mail.com
Has an @: True
Ends with mail.com: True
Slug: python-for-absolute-beginners
Address: allcsvideos.com/courses/python-for-absolute-beginners
Slug length: 29
```

</details>

<details>
<summary><b>13 · Predict the output (comparisons)</b></summary>

**Hint.** Text is compared one character at a time from the left, and capitals are different letters from small ones. A number and the text of that number are never equal. `and` needs both, `or` needs one, `not` flips.


`5 == 5.0` is `True` (the same amount), but `5 == "5"` is `False` (quotes make it text). `"apple" < "banana"` is `True` because `a` comes before `b`. `"ten" < "nine"` is `False`: Python compares one character at a time, and `t` comes after `n`. (With the text `"10"` against `"9"` the answer would be `True`, because the character `1` comes before `9`. Text is ordered by characters, not by size.) `1 <= rating <= 5` reads like maths. The last line prints three answers: `False True True`.


`solutions/Ex13.py`, run with `python Ex13.py`:

```python
# Exercise 13 - Predict: comparisons
price = 499
budget = 500
print(price == 499)
print(price != 499)
print(price < budget)
print(price >= budget)
print("Python" == "python")
print(5 == 5.0)
print(5 == "5")
print("apple" < "banana")
print("ten" < "nine")
rating = 4
print(1 <= rating <= 5)
rating = 7
print(1 <= rating <= 5)
is_enrolled = True
has_paid = False
print(is_enrolled and has_paid, is_enrolled or has_paid, not has_paid)
```

Output (Python 3.14):

```text
True
False
True
False
False
True
False
True
False
True
False
False True True
```

</details>

<details>
<summary><b>14 · Truthy or falsy?</b></summary>

**Hint.** Zero, empty things and `None` count as no. A negative number is still something. A single space is a character, so it is not empty. The text `False` has five letters in it.

Falsy values: `0`, `0.0`, `""`, `[]`, `None` (and `False` itself). Everything else is truthy, including `-3`, a single space and the text `"False"`. The last two lines show that underneath, `True` is 1 and `False` is 0.

`solutions/Ex14.py`, run with `python Ex14.py`:

```python
# Exercise 14 - Truthy or falsy?
print(bool(0))
print(bool(7))
print(bool(-3))
print(bool(0.0))
print(bool(""))
print(bool("hi"))
print(bool(" "))
print(bool("False"))
print(bool([]))
print(bool([1, 2, 3]))
print(bool(None))
print(True + True)
print(int(False))
```

Output (Python 3.14):

```text
False
True
True
False
False
True
True
True
False
True
False
2
0
```

</details>

<details>
<summary><b>15 · Fix the broken yes/no code</b></summary>

**Hint.** a: only capital `True` and `False` mean yes and no. b: one `=` stores, two `==` ask; also, the label goes on the left. c: any text with something in it is truthy, so turn the text into a real boolean with a comparison: `answer == "True"`. d: you cannot do maths on nothing; give the label a real starting value.

Fixes: `True` with a capital T; `price = 499` and then `price == 499` to ask; `has_certificate = answer == "True"` makes a real boolean from typed text (the comparison produces `False` here); and `seats = 0` so that `seats + 1` works. Whenever you see `NoneType` in an error, a box that you expected to hold a value is empty.

`solutions/Ex15.py`, run with `python Ex15.py`:

```python
# Exercise 15 - Fix the broken yes/no code (all four repaired)
is_enrolled = True            # was: true
has_paid = False

price = 499                   # was: 499 = price
print("Price is 499?", price == 499)

answer = "False"              # typed text, as input() would give it
has_certificate = answer == "True"   # a comparison makes a real boolean
print(has_certificate)

seats = 0                     # was: None, then seats + 1
print(seats + 1)
```

Output (Python 3.14):

```text
Price is 499? True
False
1
```

</details>

<details>
<summary><b>16 · Nothing here yet</b></summary>

**Hint.** `None` is its own kind of value: not zero, not empty text. Check for it with the two words `is None` (or `is not None`). The `print` function shows a message but gives nothing back.

`None` is falsy, but it is not equal to `0` or `""`: three different ideas (a zero, an empty text, and no value at all). The last two lines show where `None` often comes from: a function that has nothing to give back. The `print` call showed its message, then `result` held `None`.

`solutions/Ex16.py`, run with `python Ex16.py`:

```python
# Exercise 16 - Nothing here yet
certificate = None
print(certificate)
print(type(certificate))
print(certificate is None)
print(certificate == 0, certificate == "")
print(bool(certificate))

certificate = "CERT-0042"
print(certificate is None)
print(certificate is not None)

result = print("Welcome, Lukas")
print(result)
```

Output (Python 3.14):

```text
None
<class 'NoneType'>
True
False False
False
False
True
Welcome, Lukas
None
```

</details>

<details>
<summary><b>17 · sep and end</b></summary>

**Hint.** `sep` and `end` are written at the end of the brackets, as `name=value`. An empty separator is two quotes with nothing between them: `sep=""`.

`print` turns numbers into text by itself, so it never complains about a number among its pieces. By default `end` is the new-line character `\n`; replacing it keeps the next print on the same line.

`solutions/Ex17.py`, run with `python Ex17.py`:

```python
# Exercise 17 - sep and end
print("Lukas", "enrolled in", 3, "courses")
print(22, 10, 2026, sep="/")
print("asha", "allcsvideos.com", sep="@")
print("Python", "Basics", sep="")
print("Loading", end="... ")
print("done")
print(1, end=" ")
print(2, end=" ")
print(3)
print("Next")
```

Output (Python 3.14):

```text
Lukas enrolled in 3 courses
22/10/2026
asha@allcsvideos.com
PythonBasics
Loading... done
1 2 3
Next
```

</details>

<details>
<summary><b>18 · A tidy table</b></summary>

**Hint.** Each row is one f-string such as `f"{'Numbers':<14}{15:>6}"`. The dashes are `"-" * 20`. For the total, put the sum inside the braces: `{12 + 15 + 18 + 9:>6}`.

Anything that produces a value can go inside the braces, including a sum. Because every row uses the same widths, the right edges line up under `Min`.

`solutions/Ex18.py`, run with `python Ex18.py`:

```python
# Exercise 18 - A tidy table
print(f"{'Lesson':<14}{'Min':>6}")
print("-" * 20)
print(f"{'Variables':<14}{12:>6}")
print(f"{'Numbers':<14}{15:>6}")
print(f"{'Text':<14}{18:>6}")
print(f"{'Booleans':<14}{9:>6}")
print()
print(f"{'Total':<14}{12 + 15 + 18 + 9:>6}")
```

Output (Python 3.14):

```text
Lesson           Min
--------------------
Variables         12
Numbers           15
Text              18
Booleans           9

Total             54
```

</details>

<details>
<summary><b>19 · The 53 mystery, fixed</b></summary>

**Hint.** `input` **always** returns a string, so `"5" + "3"` joins into `"53"`. Wrap the call with `int(...)` for whole numbers, or `float(...)` for decimals. Read it from the inside out: `input` runs first, then `int` converts.

Python did not forget how to add: it joined two pieces of text. `int(input(...))` fixes it. `float` is for numbers that can have a decimal part, such as hours. If the person types `twenty five`, `int` stops with `ValueError: invalid literal for int() with base 10: 'twenty five'`. A `ValueError` means the kind of value is right (text) but its content is wrong.

`solutions/Ex19.py`, run with `printf '5\n3\n2.5\n' | python Ex19.py`:

```python
# Exercise 19 - The 53 mystery, fixed
first = int(input("First number: "))
second = int(input("Second number: "))
print("Total:", first + second)

hours = float(input("Hours per week: "))
print("In four weeks:", hours * 4)
```

Output (Python 3.14):

```text
First number: Second number: Total: 8
Hours per week: In four weeks: 10.0
```

Because the answers are piped in, they do not appear on the screen, so the questions run together. In a real session each answer appears after its question, as in the sample session above.

</details>

<details>
<summary><b>20 · The allcsvideos enrolment form</b></summary>

**Hint.** Build it in the same order as the lesson: questions first, then conversions, then the maths, then the printing. For the commas in the fee: `input(...).replace(",", "")` before `int(...)`. For a padded label inside an f-string: `{'Name':<8}`. For the money columns: `{fee:>8,}`.

This uses every idea from Module 2: labels, `int` and `float`, `//`, string methods (`strip`, `lower`, `split`, `join`, `title`, `replace`, `isdigit`), f-strings with widths, and `print` with `end`. GST of Rs 1,499 is 269.82, and floor division keeps whole rupees: 269. The program can still crash if the person types a bad number (try typing `abc` as the fee). Handling that is Module 6; deciding what to do is Module 3.

`solutions/Ex20.py`, run with `printf '  lukas   weber  \n  Lukas@Mail.COM \n24 \nPython Basics\n1,499\n2.5\n' | python Ex20.py`:

```python
# Exercise 20 - Enrolment form for allcsvideos
print("ALLCSVIDEOS ENROLMENT")
name = " ".join(input("Full name: ").split()).title()
email = input("Email: ").strip().lower()
age_text = input("Age: ").strip()
course = input("Course: ").strip()
fee = int(input("Fee in Rs: ").replace(",", ""))
hours = float(input("Hours per week: "))

print("Age is a number:", age_text.isdigit())
age = int(age_text)
gst = fee * 18 // 100
total = fee + gst

print("Saving", end="... ")
print("done")
print("-" * 30)
print(f"{'Name':<8}: {name}")
print(f"{'Email':<8}: {email}")
print(f"{'Age':<8}: {age} (next year {age + 1})")
print(f"{'Course':<8}: {course}")
print(f"{'Hours':<8}: {hours} per week")
print(f"{'Fee':<8}: Rs {fee:>8,}")
print(f"{'GST':<8}: Rs {gst:>8,}")
print(f"{'Total':<8}: Rs {total:>8,}")
print("-" * 30)
```

Output (Python 3.14):

```text
ALLCSVIDEOS ENROLMENT
Full name: Email: Age: Course: Fee in Rs: Hours per week: Age is a number: True
Saving... done
------------------------------
Name    : Lukas Weber
Email   : lukas@mail.com
Age     : 24 (next year 25)
Course  : Python Basics
Hours   : 2.5 per week
Fee     : Rs    1,499
GST     : Rs      269
Total   : Rs    1,768
------------------------------
```

Because the answers are piped in, they do not appear on the screen, so the questions run together. In a real session each answer appears after its question, as in the sample session above.

</details>

---

**Score yourself:** 16-20 working programs means you are ready for Module 03. Under 12, rewatch the lesson named above the exercises you missed. Exercises 3, 10 and 15 (reading error messages) are the best practice for every module that follows.

## What next

In **Module 03 · Decisions and Loops** your programs stop running every line in a fixed order. With `if`, `elif` and `else` they will choose, with `and`, `or` and `not` they will combine yes and no answers, and with `while` and `for` they will repeat work. That is exactly what Exercises 14, 19 and 20 were missing: reacting to a bad answer, asking again, and doing the same step for many students.
