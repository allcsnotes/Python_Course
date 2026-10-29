# M04-L03 · args and kwargs

> Video: Module 4, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- `*args`: one star in a `def` collects extra positional values into a tuple (a bag)
- `**kwargs`: two stars collect extra keyword values into a dictionary (a notes box), and how to loop over it with `.items()`
- The order in a `def`: normal parameters, `*args`, then `**kwargs`
- Unpacking in a call: `*basket` and `**course` spread a list or a dictionary into separate values
- Three mistakes, and when not to use stars at all

## Before you start

- Python 3.14 or newer (`python --version`). Do [M04-L02](../m04-l02-parameters-and-arguments/) first.
- A terminal opened in this folder.
- Tuples and dictionaries get their own lessons in Module 5. Here you only need to read them as bundles: a tuple is a bundle of values in order, written with round brackets, and a dictionary is a bundle of name and value pairs, written with curly brackets.

## Files in this folder

| File | What it is |
|------|------------|
| `fixed.py` | A two-parameter `total_price`: the second call, with three prices, fails |
| `bag.py`, `total.py`, `total_args.py` | `*prices`: a peek into the bag, the full helper, and the name `*args` |
| `enroll.py`, `log.py`, `log_bad.py` | Normal parameters together with a bag, and a parameter after the bag |
| `kw_peek.py`, `kw_loop.py` | `**details`: a peek into the notes box, and looping over it |
| `checkout.py`, `order_bad.py` | Using both catchers, and the wrong order |
| `unpack_print.py`, `unpack_star.py`, `unpack_kw.py`, `unpack_kw2.py` | Unpacking with `*` and `**` in a call |
| `unpack_forgot.py`, `checkout_typo.py`, `checkout_fix.py` | Mistakes: no star in the call, a typo in a keyword, and the fix |
| `tryit.py` | Your turn: join any number of titles with dashes (a solution) |

## Follow along

### 1. The problem

Asha wrote a helper `total_price(first, second)`. Lukas puts three courses in his cart, so she calls it with three prices:

**`fixed.py`**

```python
def total_price(first, second):
    return first + second

print(total_price(1499, 999))
print(total_price(1499, 999, 1999))
```

```text
$ python fixed.py
2498
Traceback (most recent call last):
  File "fixed.py", line 5, in <module>
    print(total_price(1499, 999, 1999))
          ~~~~~~~~~~~^^^^^^^^^^^^^^^^^
TypeError: total_price() takes 2 positional arguments but 3 were given
```

The first call works, the second stops with a `TypeError`, the same kind as last lesson. `print` accepts one thing or fifty things, so how does it do that?

### 2. The bag and the notes box

A cashier does not say "sorry, only three items". Our parameters so far are fixed slots. There are two catchers for extra values. One star catches extra values that have no name and keeps them in order (a bag). Two stars catch extra values that have a name and keep them as pairs (a notes box, like gift, coupon, ...). You have met the star: between two numbers it multiplies, two stars mean power. In a `def` line, it means something new.

### 3. *args: the bag

A parameter with one star, `*prices`, collects every extra plain value. First peek inside:

**`bag.py`**

```python
def show(*prices):
    print(prices)
    print(type(prices))

show(1499, 999, 1999)
show()
```

```text
$ python bag.py
(1499, 999, 1999)
<class 'tuple'>
()
<class 'tuple'>
```

The values arrive as a tuple, a bundle of values in order, in round brackets. With no extra values it is an empty tuple. Now the full helper: `total` starts at zero, a loop adds every price in the bundle:

**`total.py`**

```python
def total_price(*prices):
    total = 0
    for price in prices:
        total += price
    return total

print(total_price(1499, 999))
print(total_price(1499, 999, 1999, 499))
print(total_price())
```

```text
$ python total.py
2498
4996
0
```

The star makes the bag, and the name after it is only a label. Programmers almost always call it `args`:

**`total_args.py`**

```python
def total_price(*args):
    total = 0
    for price in args:
        total += price
    return total

print(total_price(1499, 999))
```

```text
$ python total_args.py
2498
```

Use a clear name like `prices` when the values have a clear meaning, and `args` when they do not.

### 4. A bag next to normal parameters

Asha enrolls many students in one course. `course` is a normal parameter, so the first value lands there, and everything left goes into the bag:

**`enroll.py`**

```python
def enroll(course, *students):
    for student in students:
        print(f"{student} joined {course}")

enroll("Python Basics", "Asha", "Lukas", "Priya")
```

```text
$ python enroll.py
Asha joined Python Basics
Lukas joined Python Basics
Priya joined Python Basics
```

A second example: `log` writes any number of messages, and `level` comes after the bag with a default:

**`log.py`**

```python
def log(*messages, level="INFO"):
    for message in messages:
        print(f"{level}: {message}")

log("Server started")
log("Disk almost full", "90% used", level="WARN")
```

```text
$ python log.py
INFO: Server started
WARN: Disk almost full
WARN: 90% used
```

A parameter after the bag can only be set by its name. A plain value would just drop into the bag. The mistake from this:

**`log_bad.py`**

```python
def log(*messages, level="INFO"):
    for message in messages:
        print(f"{level}: {message}")

log("Disk almost full", "WARN")
```

```text
$ python log_bad.py
INFO: Disk almost full
INFO: WARN
```

`WARN` was printed as one more message, and the level stayed `INFO`.

### 5. **kwargs: the notes box

Two stars catch the extra named values and keep them as pairs in a dictionary. Peek inside:

**`kw_peek.py`**

```python
def show(**details):
    print(details)
    print(type(details))

show(title="Python Basics", price=1499)
```

```text
$ python kw_peek.py
{'title': 'Python Basics', 'price': 1499}
<class 'dict'>
```

Curly brackets with pairs, and the type is `dict` (dictionary). By habit the name is `kwargs` (say "K W args"). To use the pairs, loop with a method called `.items()`, which hands over the pairs one at a time:

**`kw_loop.py`**

```python
def show_course(**details):
    for name, value in details.items():
        print(f"{name}: {value}")

show_course(title="Python Basics", price=1499,
            level="beginner")
```

```text
$ python kw_loop.py
title: Python Basics
price: 1499
level: beginner
```

The function never knew the names in advance. On allcsvideos, courses have different details: one has a level, another a language, another a deadline. One function can print them all.

### 6. Both catchers together

The order is fixed: normal parameters first, then the one-star bag, then the two-star notes box last. Asha's checkout takes the student, a bag of courses and a notes box of options:

**`checkout.py`**

```python
def checkout(student, *courses, **options):
    print(student)
    print(courses)
    print(options)

checkout("Lukas", "Python Basics", "SQL Basics",
         coupon="NEW10", gift=True)
```

```text
$ python checkout.py
Lukas
('Python Basics', 'SQL Basics')
{'coupon': 'NEW10', 'gift': True}
```

`student` is `Lukas` (the first value), `courses` is a tuple with the two course names, and `options` is a dictionary of the named values. The wrong order is a syntax error:

**`order_bad.py`**

```python
def checkout(**options, *courses):
    print(courses)
```

```text
$ python order_bad.py
  File "order_bad.py", line 1
    def checkout(**options, *courses):
                            ^
SyntaxError: arguments cannot follow var-keyword argument
```

You will often see a function written with only `*args` and `**kwargs`, nothing else. That means "accept anything", often to pass it on to another function.

### 7. Unpacking in a call

Now the reverse direction. Lukas's basket is already a list. How do we hand its three prices to `total_price` as three separate values? A star in a call spreads a list out. Try it on `print` first:

**`unpack_print.py`**

```python
basket = [1499, 999, 1999]
print(basket)
print(*basket)
print(*basket, sep=", ")
print(*range(1, 6))
```

```text
$ python unpack_print.py
[1499, 999, 1999]
1499 999 1999
1499, 999, 1999
1 2 3 4 5
```

The first line shows the list with square brackets, the second shows the three prices separately, the third uses `sep`, and the fourth spreads a `range`. Now our helper:

**`unpack_star.py`**

```python
def total_price(*prices):
    total = 0
    for price in prices:
        total += price
    return total

basket = [1499, 999, 1999]
print(total_price(*basket))
```

```text
$ python unpack_star.py
4497
```

Two stars do the same for pairs. `course` is a dictionary with `title` and `price`:

**`unpack_kw.py`**

```python
def label(title, price):
    return f"{title} costs Rs {price}"

course = {"title": "Python Basics", "price": 1499}
print(label(**course))
```

```text
$ python unpack_kw.py
Python Basics costs Rs 1499
```

**`unpack_kw2.py`**

```python
def show_course(**details):
    for name, value in details.items():
        print(f"{name}: {value}")

course = {"title": "Python Basics", "price": 1499}
show_course(**course)
```

```text
$ python unpack_kw2.py
title: Python Basics
price: 1499
```

So the star has two jobs in two places. In the `def` line it packs the extras into a bag. In a call it unpacks a list or dictionary into separate values.

### 8. Three mistakes

Mistake 1, forgetting the star in the call. The whole list went into the bag as one item:

**`unpack_forgot.py`**

```python
def total_price(*prices):
    total = 0
    for price in prices:
        total += price
    return total

basket = [1499, 999, 1999]
print(total_price(basket))
```

```text
$ python unpack_forgot.py
Traceback (most recent call last):
  File "unpack_forgot.py", line 8, in <module>
    print(total_price(basket))
          ~~~~~~~~~~~^^^^^^^^
  File "unpack_forgot.py", line 4, in total_price
    total += price
TypeError: unsupported operand type(s) for +=: 'int' and 'list'
```

Mistake 2, a typo in a keyword argument. `checkout` is called with `cupon` instead of `coupon`:

**`checkout_typo.py`**

```python
def checkout(student, *courses, **options):
    print(student)
    print(courses)
    print(options)

checkout("Lukas", "Python Basics", "SQL Basics",
         cupon="NEW10")
```

```text
$ python checkout_typo.py
Lukas
('Python Basics', 'SQL Basics')
{'cupon': 'NEW10'}
```

No error at all! The notes box catches every name, even a wrong one. The fix: if the function expects a coupon, make it a real parameter with a default of `None`, and the wrong name is rejected:

**`checkout_fix.py`**

```python
def checkout(student, *courses, coupon=None):
    print(student)
    print(courses)
    print(coupon)

checkout("Lukas", "Python Basics", "SQL Basics",
         cupon="NEW10")
```

```text
$ python checkout_fix.py
Traceback (most recent call last):
  File "checkout_fix.py", line 6, in <module>
    checkout("Lukas", "Python Basics", "SQL Basics",
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
             cupon="NEW10")
             ^^^^^^^^^^^^^^
TypeError: checkout() got an unexpected keyword argument 'cupon'. Did you mean 'coupon'?
```

Mistake 3 is the sneaky one from earlier, `log("Disk almost full", "WARN")` (step 4): a plain value cannot set a parameter after the bag. The rule of thumb: use `*args` and `**kwargs` only when you truly need any number of values, or must pass everything on. Otherwise name your parameters.

## Your turn

A helper that takes any number of course titles and joins them with dashes (here is one solution, with a list passed using a star):

**`tryit.py`**

```python
def dashed(*titles):
    return "-".join(titles)

print(dashed("Python", "SQL", "Git"))
courses = ["Python", "SQL", "Git"]
print(dashed(*courses))
```

```text
$ python tryit.py
Python-SQL-Git
Python-SQL-Git
```

## Interview tip

"What do `*args` and `**kwargs` do, and are the names special?" In a definition, `*args` collects extra positional values into a tuple and `**kwargs` collects extra keyword values into a dictionary. The names are only a habit: the stars do the work. In a call, the stars unpack a list or a dictionary.

## Common mistakes

- Forgetting the star in the call (the whole list becomes one item).
- Typos in keyword names being swallowed silently by `**kwargs`.
- Trying to set a parameter after `*args` by position.
- Using `**kwargs` before `*args` in a `def` (syntax error).
- Using stars when plain named parameters would be clearer.

## Clean up

Nothing to clean up.

## Next

[M04-L04 · Scope: What a Function Can See](../m04-l04-scope-what-a-function-can-see/)
