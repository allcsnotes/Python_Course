# M03-L02 · Comparing and Combining

> Video: Module 3, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- Comparisons inside `if`, and cleaning a typed answer with `strip()` and `lower()` before comparing
- `and`, `or`, `not` with their truth tables, and the order they run in (comparisons, `not`, `and`, `or`)
- Short-circuit evaluation: Python stops as soon as the answer is decided, and hands back that value
- Why `0 or 5` gives `5`, the default-value trick (`nickname or "Student"`), and `if coupon:` for "is there something here"
- Chained comparisons (`18 <= age < 65`) and checking the edges
- Three pitfalls in combined conditions

## Before you start

- Python 3.14 or newer (`python --version`). Do [M03-L01](../m03-l01-making-decisions-with-if/) first.
- A terminal opened in this folder.

## Files in this folder

| File | What it is |
|------|------------|
| `budget.py`, `budget2.py` | A comparison in an `if`, with budget 500 then 400 |
| `confirm.py` | Cleaning a typed yes/no with `strip()` and `lower()` |
| `unlock.py`, `unlock2.py` | `and`: enrolled and paid |
| `watch.py`, `watch2.py` | `or`: free or enrolled |
| `not_paid.py`, `email_check.py` | `not`, and `not in` |
| `rule_bug.py`, `rule_fix.py` | `and` with `or` without brackets, and with brackets |
| `crash.py`, `safe.py` | A division by zero, and the short-circuit fix |
| `default.py` | The default-value trick |
| `coupon.py`, `coupon2.py` | `if coupon:` with an empty and a filled string |
| `age_group.py` | A chained comparison, `18 <= age < 65` |
| `weekend_bug.py`, `weekend_fix.py`, `weekend_in.py` | The `day == "Sat" or "Sun"` bug, the fix, and the `in` list version |
| `ticket.py`, `ticket_fix.py` | A missing name after `and` (error) and the fix |
| `age_check.py`, `age_check_fix.py` | Forgetting `int` around `input`, and the fix |

## Follow along

### 1. The puzzle

In the REPL, `and` and `or` do not always answer True or False:

```text
>>> 0 or 5
5
>>> "" or "guest"
'guest'
>>> "hi" and "bye"
'bye'
```

By the end of the lesson you will know exactly why.

### 2. Comparisons inside an if

The six comparisons from [M02-L04](../../m02-variables-and-data-types/m02-l04-true-false-and-none/) with the price 499 and a budget of 500:

```text
>>> price = 499
>>> budget = 500
>>> price == 499
True
>>> price != 499
False
>>> price < budget
True
>>> price > budget
False
>>> price <= 499
True
>>> price >= budget
False
```

Inside an `if`, the True or False answer is used quietly and then forgotten:

**`budget.py`**

```python
price = 499
budget = 500
if price <= budget:
    print("Lukas can buy it")
else:
    print("Too expensive")
```

```text
$ python budget.py
Lukas can buy it
```

**`budget2.py`**

```python
price = 499
budget = 400
if price <= budget:
    print("Lukas can buy it")
else:
    print("Too expensive")
```

```text
$ python budget2.py
Too expensive
```

A typed answer needs cleaning first. `confirm.py` strips the spaces and makes the letters small, so `" YES "` still counts as yes:

**`confirm.py`**

```python
answer = input("Continue? (yes/no) ")
answer = answer.strip().lower()
if answer == "yes":
    print("Continuing")
else:
    print("Stopping")
```

```text
$ python confirm.py
Continue? (yes/no)  YES 
Continuing
```

```text
$ python confirm.py
Continue? (yes/no) no
Stopping
```

### 3. and

`and` is True only when both sides are True, like needing both a hall ticket and a photo ID:

```text
>>> True and True
True
>>> True and False
False
>>> False and True
False
>>> False and False
False
```

**`unlock.py`**

```python
is_enrolled = True
has_paid = False
if is_enrolled and has_paid:
    print("Video unlocked")
else:
    print("Video locked")
```

```text
$ python unlock.py
Video locked
```

**`unlock2.py`**

```python
is_enrolled = True
has_paid = True
if is_enrolled and has_paid:
    print("Video unlocked")
else:
    print("Video locked")
```

```text
$ python unlock2.py
Video unlocked
```

### 4. or

`or` is False only when both sides are False. One True is enough, like a front door and a back door:

```text
>>> True or True
True
>>> True or False
True
>>> False or True
True
>>> False or False
False
```

**`watch.py`**

```python
is_free = False
is_enrolled = True
if is_free or is_enrolled:
    print("Play the video")
else:
    print("Please enroll first")
```

```text
$ python watch.py
Play the video
```

Priya is not enrolled, and the video is not free (`watch2.py`):

```text
$ python watch2.py
Please enroll first
```

### 5. not

`not` flips one answer. It is great for yes/no flags:

**`not_paid.py`**

```python
has_paid = False
if not has_paid:
    print("Please pay to continue")
```

```text
$ python not_paid.py
Please pay to continue
```

`not in` asks whether some text is NOT inside other text:

**`email_check.py`**

```python
email = "asha.allcsvideos.com"
if "@" not in email:
    print("That email has no @")
```

```text
$ python email_check.py
That email has no @
```

Recap: `and` needs both sides True, `or` needs at least one, `not` flips the answer.

### 6. The order of and, or, not

Python runs comparisons first, then `not`, then `and`, and last `or`. Brackets always go first.

```text
>>> True or False and False
True
>>> (True or False) and False
False
```

The first is `True` because `and` goes first: `False and False` is `False`, leaving `True or False`. This can cause a real bug. Asha wants: the student must be enrolled, and either have paid or the video is free. Priya is not enrolled, but the video is free:

**`rule_bug.py`**

```python
is_enrolled = False
has_paid = False
is_free = True
if is_enrolled and has_paid or is_free:
    print("Video unlocked")
else:
    print("Video locked")
```

```text
$ python rule_bug.py
Video unlocked
```

Priya got in. Python did `is_enrolled and has_paid` first (False), then `False or is_free` (True). The fix is brackets around `has_paid or is_free`:

**`rule_fix.py`**

```python
is_enrolled = False
has_paid = False
is_free = True
if is_enrolled and (has_paid or is_free):
    print("Video unlocked")
else:
    print("Video locked")
```

```text
$ python rule_fix.py
Video locked
```

The habit: whenever one line uses both `and` and `or`, add brackets, even when Python would guess right.

### 7. Short circuit

Python is lazy in a clever way. With `and`, if the left side is False the answer must be False, so Python never looks at the right side. With `or`, if the left side is True the answer must be True. Prove it with a division by zero, which is an error:

```text
>>> False and 1 / 0
False
>>> True or 1 / 0
True
```

No error, because the right side was never run. This matters in real code. Asha wants to know if a course has more than 50 minutes per lesson, but `count` can be zero:

**`crash.py`**

```python
total = 600
count = 0
if total / count > 50:
    print("Popular course")
else:
    print("Not enough data")
```

```text
$ python crash.py
Traceback (most recent call last):
  File "crash.py", line 3, in <module>
    if total / count > 50:
       ~~~~~~^~~~~~~
ZeroDivisionError: division by zero
```

The fix puts the safety check on the left of the `and`. If `count` is zero, the division is never run:

**`safe.py`**

```python
total = 600
count = 0
if count != 0 and total / count > 50:
    print("Popular course")
else:
    print("Not enough data")
```

```text
$ python safe.py
Not enough data
```

Order matters: the safety check goes on the left.

### 8. What and and or really return

When Python stops at one of the two sides, it gives back that side's value. `or` gives the first truthy value it finds (truthy means counts as True), or the last value. `and` gives the first falsy value it finds, or the last value if everything is truthy.

```text
>>> 0 or 5
5
>>> "" or "guest"
'guest'
>>> "Asha" or "guest"
'Asha'
>>> 0 and 5
0
>>> "hi" and "bye"
'bye'
```

A useful trick: a default value. The nickname is optional. The person types `Ria`:

**`default.py`**

```python
nickname = input("Nickname (optional): ")
shown = nickname or "Student"
print("Hello,", shown)
```

```text
$ python default.py
Nickname (optional): Ria
Hello, Ria
```

The person just presses Enter:

```text
$ python default.py
Nickname (optional): 
Hello, Student
```

Warning: this trick treats zero as if it were empty. If zero is a valid answer, such as a discount of zero, use a proper `if` instead.

### 9. if coupon: "is there something here?"

An empty string is falsy, so `if coupon:` means "if there is a coupon", and `if not coupon:` means "if there is none":

**`coupon.py`**

```python
coupon = ""
if coupon:
    print("Coupon applied")
else:
    print("No coupon entered")
```

```text
$ python coupon.py
No coupon entered
```

**`coupon2.py`**

```python
coupon = "SAVE20"
if coupon:
    print("Coupon applied")
else:
    print("No coupon entered")
```

```text
$ python coupon2.py
Coupon applied
```

### 10. Ranges and edges

A standard ticket is for ages 18 up to, but not including, 65. Python lets you chain the comparisons, like in maths:

**`age_group.py`**

```python
age = 25
if 18 <= age < 65:
    print("Standard ticket")
else:
    print("Discount ticket")
```

```text
$ python age_group.py
Standard ticket
```

Test the edges, where bugs love to hide:

```text
>>> 18 <= 17 < 65
False
>>> 18 <= 18 < 65
True
>>> 18 <= 64 < 65
True
>>> 18 <= 65 < 65
False
```

At every edge decide whether the number itself counts. If yes, use `<=`. If not, use `<`.

### 11. Three pitfalls

Pitfall 1: `day == "Sat" or "Sun"` looks like English. On a Monday:

**`weekend_bug.py`**

```python
day = "Mon"
if day == "Sat" or "Sun":
    print("Weekend!")
else:
    print("Weekday")
```

```text
$ python weekend_bug.py
Weekend!
```

Python reads it as `(day == "Sat") or "Sun"`. The first part is False, so the answer is the text `"Sun"`, which is truthy. The fix is a full question on each side of the `or` (or a shorter way: `day in ["Sat", "Sun"]`):

**`weekend_fix.py`**

```python
day = "Mon"
if day == "Sat" or day == "Sun":
    print("Weekend!")
else:
    print("Weekday")
```

```text
$ python weekend_fix.py
Weekday
```

**`weekend_in.py`**

```python
day = "Mon"
if day in ["Sat", "Sun"]:
    print("Weekend!")
else:
    print("Weekday")
```

```text
$ python weekend_in.py
Weekday
```

Pitfall 2: another sentence that sounds right in English, "at least 18 and under 65":

**`ticket.py`**

```python
age = 25
if age >= 18 and < 65:
    print("Standard ticket")
```

```text
$ python ticket.py
  File "ticket.py", line 2
    if age >= 18 and < 65:
                     ^
SyntaxError: invalid syntax
```

Each side of the `and` must be a full question, with a name on the left. Write the name again:

**`ticket_fix.py`**

```python
age = 25
if age >= 18 and age < 65:
    print("Standard ticket")
```

```text
$ python ticket_fix.py
Standard ticket
```

Pitfall 3: forgetting `int`. The person types 18, but the text `"18"` is not equal to the number 18, and there is no error at all:

**`age_check.py`**

```python
age = input("Age: ")
if age == 18:
    print("Exactly eighteen")
else:
    print("Not eighteen")
```

```text
$ python age_check.py
Age: 18
Not eighteen
```

Wrap `input` in `int`:

**`age_check_fix.py`**

```python
age = int(input("Age: "))
if age == 18:
    print("Exactly eighteen")
else:
    print("Not eighteen")
```

```text
$ python age_check_fix.py
Age: 18
Exactly eighteen
```

## Interview tip

"What is short-circuit evaluation in Python?" With `and`, Python stops at the first falsy value. With `or`, it stops at the first truthy value. Anything on the right is never run, which lets you put a safety check on the left (`count != 0 and total / count > 50`).

## Common mistakes

- Using `and` with `or` without brackets.
- Writing `day == "Sat" or "Sun"` instead of a full question on each side.
- Writing `age >= 18 and < 65` (a missing name), instead of `age >= 18 and age < 65` or `18 <= age < 65`.
- Comparing `input` text with a number (forget `int`).
- Using the `x or default` trick when zero is a valid answer.
- `=` where you meant `==`, and comparing floats with `==`.

## Clean up

Nothing to clean up.

## Next

[M03-L03 · Repeating with while](../m03-l03-repeating-with-while/)
