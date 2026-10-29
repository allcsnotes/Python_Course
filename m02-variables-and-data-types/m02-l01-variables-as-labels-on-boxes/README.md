# M02-L01 · Variables as Labels on Boxes

> Video: Module 2, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- A variable is a name (label) attached to a value, made with one equals sign, read from right to left
- How to reassign a variable, count with `x = x + 1`, and why the old value is forgotten
- The four naming rules, the 35 keywords, and the style advice (snake case, meaningful names)
- Multiple assignment and how to swap two variables correctly
- Types belong to values, not labels (`type()`), constants by convention, and `del`
- Three traps: a typo in a name, `=` does not link two names, reusing the name `print`

## Before you start

- Python 3.14 or newer (`python --version`). Do Module 1 first, you should be able to run a file.
- A terminal opened in this folder.

## Files in this folder

| File | What it is |
|------|------------|
| `welcome.py`, `welcome_priya.py` | Four variables and five `print` lines for allcsvideos.com; the second has the name changed |
| `progress.py`, `counter.py` | Reassigning, and counting with `lessons_completed = lessons_completed + 1` |
| `quiz_names.py` | Checks the eight names from the "which are valid?" quiz |
| `bad_digit.py`, `bad_space.py`, `bad_keyword.py`, `bad_dash.py`, `case_bug.py` | One broken name each, to see the real error |
| `kw.py` | Lists Python's keywords |
| `style_bad.py`, `style_good.py`, `styles_ok.py` | Meaningful names versus one-letter names, and three naming styles |
| `multi.py` | Multiple assignment |
| `swap_bug.py`, `swap_temp.py`, `swap_py.py` | The swap that loses a value, and two ways to fix it |
| `dynamic.py`, `kinds.py`, `kinds_err.py`, `quotes.py` | A label can move between types; `type()`; the type error you can cause |
| `constants.py`, `delete.py` | Capital-letter constants (a promise, not a lock), and `del` |
| `typo.py`, `alias.py`, `shadow.py` | The three pitfalls |

## Follow along

### 1. The mystery swap

Five lines that try to swap `a` and `b`. Guess what they print, then run them:

**`swap_bug.py`**

```python
a = 1
b = 2
a = b
b = a
print(a, b)
```

```text
$ python swap_bug.py
2 2
```

Both labels show `2`, and the `1` has vanished. Steps 7 and 8 explain it.

### 2. Make a variable in the REPL

A variable is a label stuck on a value. To create one, write the label, one equals sign, then the value. This is called an assignment. In maths `=` says two things are the same, in Python it means "store". Read the line from right to left: first the value, then the label is stuck onto it.

Start the REPL with `python`:

```text
>>> student_name = "Lukas"
>>> student_name
'Lukas'
>>> print(student_name)
Lukas
>>> course_name = "Python"
>>> print(student_name, "is learning", course_name)
Lukas is learning Python
>>> exit()
```

An assignment is silent. To read the value back, write the label on its own with no quotes (the REPL shows `'Lukas'` with quotes because it is text). Labels never have quotes, text always does.

### 3. A variable in a file

Text goes in quotes, numbers do not. Each `print` looks up the labels it needs.

**`welcome.py`**

```python
student_name = "Lukas"
course_name = "Python"
lessons_completed = 12
price = 499
print("Student:", student_name)
print("Course:", course_name)
print("Lessons done:", lessons_completed)
print("Price:", price)
print(student_name, "completed", lessons_completed)
```

```text
$ python welcome.py
Student: Lukas
Course: Python
Lessons done: 12
Price: 499
Lukas completed 12
```

Change `"Lukas"` to `"Priya"` (this is `welcome_priya.py`) and run again. The first and last lines change, because both used the label:

**`welcome_priya.py`**

```python
student_name = "Priya"
course_name = "Python"
lessons_completed = 12
price = 499
print("Student:", student_name)
print("Course:", course_name)
print("Lessons done:", lessons_completed)
print("Price:", price)
print(student_name, "completed", lessons_completed)
```

```text
$ python welcome_priya.py
Student: Priya
Course: Python
Lessons done: 12
Price: 499
Priya completed 12
```

### 4. Reassigning and counting

A variable can vary: move the label to a new value. Python always uses what is true at that moment.

**`progress.py`**

```python
lessons_completed = 12
print(lessons_completed)
lessons_completed = 13
print(lessons_completed)
```

```text
$ python progress.py
12
13
```

The old `12` has no label any more, so it is forgotten. A pattern you will use in almost every program is counting. Python works out the right side first, then sticks the label on the result:

**`counter.py`**

```python
lessons_completed = 12
lessons_completed = lessons_completed + 1
lessons_completed = lessons_completed + 1
print(lessons_completed)
```

```text
$ python counter.py
14
```

### 5. The four naming rules

1. Use only letters, digits and the underscore.
2. A name cannot start with a digit.
3. Names are case sensitive: `Price` and `price` are different.
4. A name cannot be a keyword (a word Python keeps for itself).

`quiz_names.py` tests the eight names from the video. `True` means Python accepts the name:

**`quiz_names.py`**

```python
import keyword
for n in ["student_name","total_price","price2","Price","2nd_course","course name","price-2","class"]:
    print(n, n.isidentifier() and not keyword.iskeyword(n))
```

```text
$ python quiz_names.py
student_name True
total_price True
price2 True
Price True
2nd_course False
course name False
price-2 False
class False
```

Now the real errors:

**`bad_digit.py`**

```python
2nd_course = "Python"
```

```text
$ python bad_digit.py
  File "bad_digit.py", line 1
    2nd_course = "Python"
    ^
SyntaxError: invalid decimal literal
```

**`bad_space.py`**

```python
course name = "Python"
```

```text
$ python bad_space.py
  File "bad_space.py", line 1
    course name = "Python"
           ^^^^
SyntaxError: invalid syntax
```

**`bad_keyword.py`**

```python
class = "Python"
```

```text
$ python bad_keyword.py
  File "bad_keyword.py", line 1
    class = "Python"
          ^
SyntaxError: invalid syntax
```

**`bad_dash.py`**

```python
price-2 = 499
```

```text
$ python bad_dash.py
  File "bad_dash.py", line 1
    price-2 = 499
    ^^^^^^^
SyntaxError: cannot assign to expression here. Maybe you meant '==' instead of '='?
```

**`case_bug.py`**

```python
Price = 499
print(price)
```

```text
$ python case_bug.py
Traceback (most recent call last):
  File "case_bug.py", line 2, in <module>
    print(price)
          ^^^^^
NameError: name 'price' is not defined. Did you mean: 'Price'?
```

Python lists its keywords for you:

**`kw.py`**

```python
import keyword
print(keyword.kwlist)
print(len(keyword.kwlist))
```

```text
$ python kw.py
['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
35
```

There are 35 keywords in this version. You do not need to memorise them.

### 6. Style, and several names at once

PEP 8, the official style guide, says: write names in lower case with words joined by underscores (snake case: `lessons_completed`). Other styles are valid names, but not the Python way:

**`styles_ok.py`**

```python
lessons_completed = 12
lessonsCompleted = 12
LessonsCompleted = 12
print("all three are valid names")
```

```text
$ python styles_ok.py
all three are valid names
```

Use meaningful names. These two files print the same thing, but only one tells you what the values mean:

**`style_bad.py`**

```python
x = "Lukas"
n = 12
p = 499
print(x, n, p)
```

```text
$ python style_bad.py
Lukas 12 499
```

**`style_good.py`**

```python
student_name = "Lukas"
lessons_completed = 12
price = 499
print(student_name, lessons_completed, price)
```

```text
$ python style_good.py
Lukas 12 499
```

Multiple assignment puts two labels on the same value, or gives two labels two values in one line. Use it with care, one variable per line is easier to read:

**`multi.py`**

```python
quizzes_passed = quizzes_failed = 0
lessons_completed, lessons_total = 12, 104
print(quizzes_passed, quizzes_failed)
print(lessons_completed, lessons_total)
```

```text
$ python multi.py
0 0
12 104
```

### 7. Why the swap failed

`a = b` moves the label `a` onto the value `2`. Now both labels are on `2`, and the `1` has no label. `b = a` changes nothing. The fix needs a third label to hold on to the value:

**`swap_temp.py`**

```python
a = 1
b = 2
temp = a
a = b
b = temp
print(a, b)
```

```text
$ python swap_temp.py
2 1
```

Python also has a one-line swap. The right side is worked out first, then both labels move at the same time:

**`swap_py.py`**

```python
a = 1
b = 2
a, b = b, a
print(a, b)
```

```text
$ python swap_py.py
2 1
```

You will see `a, b = b, a` all the time in real code.

### 8. Types belong to values

Python has a word for the kind of a value: its type. A label has no fixed type, it can be stuck on a number now and on text later:

**`dynamic.py`**

```python
lessons_completed = 12
print(lessons_completed)
lessons_completed = "twelve"
print(lessons_completed)
```

```text
$ python dynamic.py
12
twelve
```

Ask for the type with `type()`:

**`kinds.py`**

```python
lessons_completed = 12
print(type(lessons_completed))
lessons_completed = "twelve"
print(type(lessons_completed))
```

```text
$ python kinds.py
<class 'int'>
<class 'str'>
```

`int` is a whole number, `str` is text (a string). The quotes change the type:

**`quotes.py`**

```python
print(type(12))
print(type("12"))
```

```text
$ python quotes.py
<class 'int'>
<class 'str'>
```

The freedom has a cost. Adding a number to text is an error:

**`kinds_err.py`**

```python
lessons_completed = "twelve"
lessons_completed = lessons_completed + 1
```

```text
$ python kinds_err.py
Traceback (most recent call last):
  File "kinds_err.py", line 2, in <module>
    lessons_completed = lessons_completed + 1
                        ~~~~~~~~~~~~~~~~~~^~~
TypeError: can only concatenate str (not "int") to str
```

### 9. Constants and `del`

Some values should never change, such as a maximum number of attempts. Python cannot lock a value. By convention, all capitals mean "please do not change this". It is a promise between humans, not a rule for the machine:

**`constants.py`**

```python
MAX_QUIZ_ATTEMPTS = 3
print(MAX_QUIZ_ATTEMPTS)
MAX_QUIZ_ATTEMPTS = 5
print(MAX_QUIZ_ATTEMPTS)
```

```text
$ python constants.py
3
5
```

`del` removes the label itself. Afterwards the name does not exist. You will rarely need it:

**`delete.py`**

```python
price = 499
print(price)
del price
print(price)
```

```text
$ python delete.py
499
Traceback (most recent call last):
  File "delete.py", line 4, in <module>
    print(price)
          ^^^^^
NameError: name 'price' is not defined. Did you mean: 'print'?
```

### 10. The three pitfalls

A typo in a label (the most common error you will ever see; read the hint):

**`typo.py`**

```python
student_name = "Lukas"
print(student_nme)
```

```text
$ python typo.py
Traceback (most recent call last):
  File "typo.py", line 2, in <module>
    print(student_nme)
          ^^^^^^^^^^^
NameError: name 'student_nme' is not defined. Did you mean: 'student_name'?
```

`=` does not link two names. `lessons_backup` took the value the label had at that moment. Moving the other label does not drag it along:

**`alias.py`**

```python
lessons_completed = 12
lessons_backup = lessons_completed
lessons_completed = 13
print(lessons_completed, lessons_backup)
```

```text
$ python alias.py
13 12
```

Reusing the name of a built-in helper. `print` is also just a label, the label of the helper that prints:

**`shadow.py`**

```python
print = "Lukas"
print("Hello")
```

```text
$ python shadow.py
Traceback (most recent call last):
  File "shadow.py", line 2, in <module>
    print("Hello")
    ~~~~~^^^^^^^^^
TypeError: 'str' object is not callable
```

Python tried to call the text `"Lukas"` as if it were the helper. Never reuse names like `print`.

## Interview tip

Rahul, our senior developer, asks: what is a variable in Python? A strong one-sentence answer: a variable in Python is a name that refers to a value. Assignment attaches the name to the value, it does not copy a box, and the type belongs to the value, not the name.

## Common mistakes

- Typing a name differently from where you created it (`student_nme`). Read the "Did you mean" hint.
- Starting a name with a digit, using a space or a dash, or using a keyword like `class`.
- Mixing capitals: `Price` and `price` are two different names.
- Thinking `=` makes two names stay linked, or that `a = b; b = a` swaps two values.
- Assigning to a built-in name such as `print`.

## Clean up

Nothing to clean up.

## Next

[M02-L02 · Numbers](../m02-l02-numbers/)
