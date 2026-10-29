# M06-L04 · Raising and Designing Errors

> Video: Module 6, Lesson 4. Watch it first, then follow along here.

## What you'll learn
- Raise your own error with `raise`, a built-in kind such as `ValueError`, and a clear message.
- Who raises and who catches: raise where you detect the problem, catch where you can decide what to do.
- Re-raise an error with a bare `raise`, and chain a clearer error with `raise ... from error`.
- Make a brand new kind of error in two lines (`UnknownCourseError`, `PaymentError`).
- Fail early and loudly instead of returning `None`, and when to use `assert` instead of `raise`.

## Before you start
- Python 3.14 or newer. Check with `python --version`.
- No packages and no Docker. You only need the files in this folder.
- Helpful: Lesson M06-L03 (Exceptions), where you caught errors with `try` and `except`.
- Run every command from inside this folder.
- In the "you should see" blocks below, the traceback file paths are shortened to the file name. Your own traceback shows the full path to the file, which is fine.

## Files in this folder
| File | What it is |
| --- | --- |
| `hook.py` | `enrol` returns `('Lukas', None)` quietly (the hook) |
| `raise1.py` | `make_expense` raises `ValueError` for a negative amount |
| `stops.py` | `raise` stops the function on the spot |
| `catch1.py` | `save_expense` catches the error and prints a friendly message |
| `reraise.py` | a bare `raise` passes the same error on |
| `chain.py` | `raise ... from error` links a clearer error to the original |
| `payment.py` | your first custom error, `PaymentError` |
| `enrol_custom.py` | `UnknownCourseError` and a caller that catches it |
| `by_type.py` | catching by kind: a real bug is not hidden |
| `quiet.py` | failing quietly: the crash shows up far from the cause |
| `loud.py` | failing loudly: the crash points at the cause |
| `assert1.py` | `assert` as a check on your own code |
| `rawstr.py` | pitfall 1: raising plain text |
| `vague.py` | pitfall 2: raising with no message |
| `clear.py` | the clear version, with the bad value in the message |
| `outside.py` | pitfall 3: a bare `raise` outside `except` |
| `tryit.py` | the "try it yourself" answer: `set_percent` |

## Follow along

### 1. The hook: a quiet failure
Asha is checking enrolments on allcsvideos.com. Lukas signs up for course `C103`, but the school only has `C101` and `C102`. `enrol` looks the course up with `get`, which gives `None` for a missing key.

`hook.py`:
```python
courses = {"C101": "Python", "C102": "SQL"}


def enrol(student, course_id):
    return (student, courses.get(course_id))


print(enrol("Lukas", "C103"))
```
```bash
python hook.py
```
You should see:
```
('Lukas', None)
```
No error, no warning. Lukas is enrolled in nothing and the program is happy. The rest of the lesson makes functions shout when something is wrong.

### 2. Raise your own error
`raise`, then the kind of error, then a message in round brackets. `ValueError` means: the right kind of thing, but a value that is not acceptable. (Its cousin `TypeError` means the wrong kind of thing, like adding text to a number.)

`raise1.py`:
```python
def make_expense(amount, category):
    if amount <= 0:
        raise ValueError("amount must be positive")
    return {"amount": amount, "category": category}


print(make_expense(250, "food"))
print(make_expense(-50, "food"))
```
```bash
python raise1.py
```
You should see:
```
{'amount': 250, 'category': 'food'}
Traceback (most recent call last):
  File "raise1.py", line 8, in <module>
    print(make_expense(-50, "food"))
          ~~~~~~~~~~~~^^^^^^^^^^^^^
  File "raise1.py", line 3, in make_expense
    raise ValueError("amount must be positive")
ValueError: amount must be positive
```
Read the traceback from the bottom: `ValueError: amount must be positive` is your own message. Above it is the trail: line 3 (the `raise`) and line 8 (the call that led there).

### 3. Raise stops the function
`raise` works like `return` in one way: the rest of the function is skipped. The difference: `return` hands back a value, `raise` hands back a problem.

`stops.py`:
```python
def check(amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    print("amount is fine")


check(50)
check(-50)
```
```bash
python stops.py
```
You should see:
```
amount is fine
Traceback (most recent call last):
  File "stops.py", line 8, in <module>
    check(-50)
    ~~~~~^^^^^
  File "stops.py", line 3, in check
    raise ValueError("amount must be positive")
ValueError: amount must be positive
```
`amount is fine` appears once. For `-50`, the print line never ran.

### 4. Who catches? The caller
`make_expense` does not know who calls it (a terminal program, a website, a night script). The caller knows more, so the caller catches. The rule: raise where you detect the problem, catch where you can decide what to do. If you cannot decide, do not catch: let the error travel up.

`catch1.py`:
```python
def make_expense(amount, category):
    if amount <= 0:
        raise ValueError("amount must be positive")
    return {"amount": amount, "category": category}


def save_expense(text):
    try:
        expense = make_expense(float(text), "food")
        print("Saved:", expense["amount"])
    except ValueError as error:
        print("Could not save:", error)


save_expense("250")
save_expense("-50")
save_expense("abc")
```
```bash
python catch1.py
```
You should see:
```
Saved: 250.0
Could not save: amount must be positive
Could not save: could not convert string to float: 'abc'
```
One `except` caught two different problems because `float("abc")` is also a `ValueError`. The second message is your own, the third is Python's own.

### 5. Re-raise with a bare raise
Sometimes you want to look at an error and still pass it on, for example write a note in a log. A single `raise` with nothing after it, inside `except`, sends the same error up again.

`reraise.py`:
```python
def read_amount(text):
    try:
        return float(text)
    except ValueError:
        print("Log: bad amount", text)
        raise


print(read_amount("abc"))
```
```bash
python reraise.py
```
You should see:
```
Log: bad amount abc
Traceback (most recent call last):
  File "reraise.py", line 9, in <module>
    print(read_amount("abc"))
          ~~~~~~~~~~~^^^^^^^
  File "reraise.py", line 3, in read_amount
    return float(text)
ValueError: could not convert string to float: 'abc'
```
Nothing was lost: it is the same original error, passed on after you took a look.

### 6. Chain a clearer error with from error
"Could not convert string to float" talks about floats, not about what the person was doing. Raise a new, clearer error, and add `from error` to link the original as its cause.

`chain.py`:
```python
def read_amount(text):
    try:
        return float(text)
    except ValueError as error:
        raise ValueError("not a number") from error


print(read_amount("abc"))
```
```bash
python chain.py
```
You should see:
```
Traceback (most recent call last):
  File "chain.py", line 3, in read_amount
    return float(text)
ValueError: could not convert string to float: 'abc'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "chain.py", line 8, in <module>
    print(read_amount("abc"))
          ~~~~~~~~~~~^^^^^^^
  File "chain.py", line 5, in read_amount
    raise ValueError("not a number") from error
ValueError: not a number
```
Read it as a story: first the cause, then the error you chose to show.

### 7. Make your own kind of error
`ValueError` is broad. A new kind of error means exactly one thing. Two lines: `class`, a name ending in `Error` with capital letters, `Exception` in brackets, then `pass`. (A class is a recipe Python lets you copy. Classes get their own module, module 8. For now, copy the pattern and change the name.)

`payment.py`:
```python
class PaymentError(Exception):
    pass


raise PaymentError("card was declined")
```
```bash
python payment.py
```
You should see:
```
Traceback (most recent call last):
  File "payment.py", line 5, in <module>
    raise PaymentError("card was declined")
PaymentError: card was declined
```

### 8. Fix Lukas's typo with UnknownCourseError
`enrol` now checks at the start. After the check, it can use square brackets, because the key must be there.

`enrol_custom.py`:
```python
courses = {"C101": "Python", "C102": "SQL"}


class UnknownCourseError(Exception):
    pass


def enrol(student, course_id):
    if course_id not in courses:
        raise UnknownCourseError(f"no course {course_id}")
    return (student, courses[course_id])


try:
    print(enrol("Priya", "C102"))
    print(enrol("Lukas", "C103"))
except UnknownCourseError as error:
    print("Sorry:", error)
```
```bash
python enrol_custom.py
```
You should see:
```
('Priya', 'SQL')
Sorry: no course C103
```
The typo no longer slips through.

### 9. Why not just ValueError? Real bugs stay loud
`except UnknownCourseError` catches only this one problem. In `by_type.py` the call forgets an argument (a real bug).

`by_type.py` (the last line is the only difference):
```python
try:
    enrol("Lukas")
except UnknownCourseError as error:
    print("Sorry:", error)
```
```bash
python by_type.py
```
You should see:
```
Traceback (most recent call last):
  File "by_type.py", line 15, in <module>
    enrol("Lukas")
    ~~~~~^^^^^^^^^
TypeError: enrol() missing 1 required positional argument: 'course_id'
```
Our `except` did not touch it, and that is what we want: we handled the problem we planned for, and a real bug stays visible.

### 10. Fail early and loudly: the quiet version
`find_course` returns `courses.get(...)`, which is `None` for an unknown id. The crash happens later, somewhere else.

`quiet.py`:
```bash
python quiet.py
```
You should see:
```
Traceback (most recent call last):
  File "quiet.py", line 9, in <module>
    print("Welcome to " + title.upper())
                          ^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'upper'
```
Python points at the print line, but the real problem is an unknown course id back in `find_course`. In a big program that could be hundreds of lines, or several files, away.

### 11. The loud version
`loud.py` checks at the door and raises `UnknownCourseError` with the id in the message.
```bash
python loud.py
```
You should see:
```
Traceback (most recent call last):
  File "loud.py", line 14, in <module>
    title = find_course("C103")
  File "loud.py", line 10, in find_course
    raise UnknownCourseError(f"no course {course_id}")
UnknownCourseError: no course C103
```
The last frame is `find_course`, the exact place that noticed the problem. The Zen of Python says it: errors should never pass silently.

Three habits:
1. Check inputs at the top of a function, before doing any work.
2. Put the bad value in the message.
3. Do not return `None`, or a special number like `-1`, to mean failed. The exception is when a missing answer is normal: square brackets when missing is a bug, `get` when missing is fine.

### 12. assert: a check for yourself
`assert condition, message`. If the condition is `True`, nothing happens. If it is `False`, Python raises `AssertionError` with your message.

`assert1.py`:
```python
def apply_discount(price, percent):
    final = price - price * percent / 100
    assert 0 <= final <= price, "bad final price"
    return final


print(apply_discount(1000, 20))
print(apply_discount(1000, 150))
```
```bash
python assert1.py
```
You should see:
```
800.0
Traceback (most recent call last):
  File "assert1.py", line 8, in <module>
    print(apply_discount(1000, 150))
          ~~~~~~~~~~~~~~^^^^^^^^^^^
  File "assert1.py", line 3, in apply_discount
    assert 0 <= final <= price, "bad final price"
           ^^^^^^^^^^^^^^^^^^^
AssertionError: bad final price
```
Which one to use? If the bad value can come from outside (a person typing, a file, a website), use `raise` with a proper error. `assert` is for something that can never happen unless your own code has a bug.

Why: asserts can be switched off. Run with `-O`:
```bash
python -O assert1.py
```
You should see:
```
800.0
-500.0
```
No error at all. A check that can disappear must never guard real user input.

### 13. Three pitfalls
**Pitfall 1: raising plain text.** `rawstr.py` does `raise "amount must be positive"`.
```bash
python rawstr.py
```
You should see:
```
Traceback (most recent call last):
  File "rawstr.py", line 3, in <module>
    raise "amount must be positive"
TypeError: exceptions must derive from BaseException
```
You can only raise errors, not plain text. Put the text inside an error kind: `ValueError("...")`.

**Pitfall 2: no message.** `vague.py` does `raise ValueError` with nothing after it.
```bash
python vague.py
```
You should see:
```
Traceback (most recent call last):
  File "vague.py", line 3, in <module>
    raise ValueError
ValueError
```
Which value? What is wrong? Compare `clear.py`, which puts the message and the value in:
```bash
python clear.py
```
```
Traceback (most recent call last):
  File "clear.py", line 3, in <module>
    raise ValueError(f"amount must be positive, got {amount}")
ValueError: amount must be positive, got -50
```

**Pitfall 3: a bare raise outside except.** `outside.py` does a bare `raise` with no error being handled.
```bash
python outside.py
```
You should see:
```
Traceback (most recent call last):
  File "outside.py", line 3, in <module>
    raise
RuntimeError: No active exception to reraise
```
A bare `raise` means "send the current error again", so it only works inside `except`.

### 14. Try it yourself
Write `set_percent` that raises `ValueError` if the number is below 0 or above 100, with the number in the message. Loop over 40 and 150, call it inside `try` and `except`, and print a friendly message. The answer is `tryit.py`:
```python
def set_percent(value):
    if value < 0 or value > 100:
        raise ValueError(f"percent must be 0 to 100, got {value}")
    return value


for value in [40, 150]:
    try:
        print("Saved", set_percent(value))
    except ValueError as error:
        print("Could not save:", error)
```
```bash
python tryit.py
```
You should see:
```
Saved 40
Could not save: percent must be 0 to 100, got 150
```

## Common mistakes
- Raising plain text: `raise "message"` is a `TypeError`. Raise an error kind.
- Raising with no message, so the next person has to guess what went wrong. Put the bad value in the message.
- Using a bare `raise` outside an `except` block (`RuntimeError`).
- Returning `None` or `-1` to mean "failed". The caller can ignore it and the bug shows up later, somewhere else.
- Using `assert` to check what users type. Asserts vanish with `python -O`.
- Catching too broadly. Catch by the exact kind so real bugs stay loud.

## Clean up
Nothing to clean up. These scripts create no files.

## Next
[M06-L05 · Dates, Times and the Standard Library Tour](../m06-l05-dates-times-and-the-standard-library-tour/)
