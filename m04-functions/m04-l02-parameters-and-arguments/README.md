# M04-L02 · Parameters and Arguments

> Video: Module 4, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- The difference between a parameter (the blank in the definition) and an argument (the value in the call)
- Positional arguments (matched by place: order and count must be right) and keyword arguments (matched by name)
- Default values, and the rule that blanks without a default come first
- The mutable-default trap (`students=[]`) and its fix (`students=None`)
- Why a function does not change your own label, and the errors you get from wrong calls

## Before you start

- Python 3.14 or newer (`python --version`). Do [M04-L01](../m04-l01-functions-as-recipes/) first.
- A terminal opened in this folder.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The opening puzzle: two arguments in the wrong order |
| `sale.py`, `swap.py` | `sale_price` with right and swapped positional arguments |
| `missing.py`, `too_many.py` | Too few and too many arguments |
| `keywords.py`, `print_sep.py` | Keyword arguments, and `sep=` as one you already know |
| `mixed.py`, `typo.py` | A positional after a keyword, and a misspelled keyword |
| `defaults.py`, `order.py` | Default values, and a default in the wrong place |
| `enroll.py` | Defaults and keywords together |
| `names.py`, `trap.py`, `fix.py` | A first look at a list, the mutable-default trap, and the fix |
| `outside.py`, `coupon.py` | Names live only inside the function; a function does not change your label |

## Follow along

### 1. The puzzle

A function welcomes a student to a course. Will both calls print the same sentence?

**`hook.py`**

```python
def welcome(name, course):
    print("Welcome", name, "to", course)

welcome("Lukas", "Python Basics")
welcome("Python Basics", "Lukas")
```

```text
$ python hook.py
Welcome Lukas to Python Basics
Welcome Python Basics to Lukas
```

The second line says "Welcome Python Basics to Lukas". There is no error, Python did exactly what we told it: the same two values were just handed over in the other order. How does a function know which value goes where?

### 2. Parameters and arguments

Think of a coffee-shop order slip with two blanks (size, milk). The blanks have names and wait to be filled in. A customer fills them in (large, oat) and the next customer fills in the same slip differently. The blank on the slip, the name in the `def` line, is a parameter. The answer that fills it, the value in the call, is an argument. A parameter belongs to the definition, an argument belongs to the call. (Both words start with P or A: parameter is placeholder, argument is actual value.)

### 3. A first function with two parameters

A shop on allcsvideos wants a sale price: take a price and cut a percent off it. `price` and `percent` are the parameters (blanks). The two calls hand over different arguments:

**`sale.py`**

```python
def sale_price(price, percent):
    return price - price * percent / 100

print(sale_price(1000, 20))
print(sale_price(500, 10))
```

```text
$ python sale.py
800.0
450.0
```

Python made two labels, `price` and `percent`, and stuck them on the values from the call. Then the body ran and the answer was handed back. Then the two labels were removed: they only live while the function runs, and the next call makes fresh ones.

### 4. Positional arguments: order and count

Python matched the arguments by position: the first value goes into the first blank, like a queue. So the order matters. Swap them:

**`swap.py`**

```python
def sale_price(price, percent):
    return price - price * percent / 100

print(sale_price(20, 1000))
```

```text
$ python swap.py
-180.0
```

A negative price! Python put 20 into `price` and 1000 into `percent`. It never checks if the values make sense. That is exactly what happened in the puzzle. The count must be right too:

**`missing.py`**

```python
def sale_price(price, percent):
    return price - price * percent / 100

print(sale_price(1000))
```

```text
$ python missing.py
Traceback (most recent call last):
  File "missing.py", line 4, in <module>
    print(sale_price(1000))
          ~~~~~~~~~~^^^^^^
TypeError: sale_price() missing 1 required positional argument: 'percent'
```

**`too_many.py`**

```python
def sale_price(price, percent):
    return price - price * percent / 100

print(sale_price(1000, 20, 5))
```

```text
$ python too_many.py
Traceback (most recent call last):
  File "too_many.py", line 4, in <module>
    print(sale_price(1000, 20, 5))
          ~~~~~~~~~~^^^^^^^^^^^^^
TypeError: sale_price() takes 2 positional arguments but 3 were given
```

With positional arguments two things must be right: the count and the order.

### 5. Keyword arguments

To make a mix-up impossible, name the blanks when you call: the parameter name, an equals sign, the value. Every value carries its own label, so the order stops mattering:

**`keywords.py`**

```python
def sale_price(price, percent):
    return price - price * percent / 100

print(sale_price(price=1000, percent=20))
print(sale_price(percent=20, price=1000))
print(sale_price(1000, percent=20))
```

```text
$ python keywords.py
800.0
800.0
800.0
```

You already did this with `print("Welcome", "Lukas", sep=", ")`:

**`print_sep.py`**

```python
print("Welcome", "Lukas", sep=", ")
```

```text
$ python print_sep.py
Welcome, Lukas
```

Rules for mixing: positional arguments first, keyword arguments after. Break it:

**`mixed.py`**

```python
def sale_price(price, percent):
    return price - price * percent / 100

print(sale_price(price=1000, 20))
```

```text
$ python mixed.py
  File "mixed.py", line 4
    print(sale_price(price=1000, 20))
                                   ^
SyntaxError: positional argument follows keyword argument
```

It is a syntax error, found before anything ran. One more slip, a typo in the name:

**`typo.py`**

```python
def sale_price(price, percent):
    return price - price * percent / 100

print(sale_price(1000, persent=20))
```

```text
$ python typo.py
Traceback (most recent call last):
  File "typo.py", line 4, in <module>
    print(sale_price(1000, persent=20))
          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: sale_price() got an unexpected keyword argument 'persent'. Did you mean 'percent'?
```

Recap: parameters are the blanks in the definition, arguments are the values in the call, positional arguments are matched by place (order and count matter), keyword arguments are matched by name (order does not matter), and positional come first.

### 6. Default values

At a coffee shop you say "a coffee, please" and the cashier does not ask about the size: a default is used. A default value is written in the definition: `percent=10`. If the caller gives a value it replaces the default, otherwise the default is used. `print` itself has a default for `sep`, one space.

**`defaults.py`**

```python
def sale_price(price, percent=10):
    return price - price * percent / 100

print(sale_price(1000))
print(sale_price(1000, 25))
print(sale_price(1000, percent=50))
```

```text
$ python defaults.py
900.0
750.0
500.0
```

1000 with no percent used the default 10 and gave 900.0. 1000 and 25 replaced the default and gave 750.0, and `percent=50` as a keyword gave 500.0.

One rule: blanks without a default must come first. Break it:

**`order.py`**

```python
def sale_price(percent=10, price):
    return price - price * percent / 100
```

```text
$ python order.py
  File "order.py", line 1
    def sale_price(percent=10, price):
                               ^^^^^
SyntaxError: parameter without a default follows parameter with a default
```

Python refuses the definition itself. Defaults and keywords work best together:

**`enroll.py`**

```python
def enroll(student, course="Python",
           level="basic"):
    print(student, "joined", course, level)

enroll("Lukas")
enroll("Priya", "Java")
enroll("Asha", level="advanced")
```

```text
$ python enroll.py
Lukas joined Python basic
Priya joined Java basic
Asha joined Python advanced
```

Lukas gets both defaults. Priya replaces the course and keeps the level. Asha used a keyword to replace only the level. Without the keyword she would have to repeat the course just to reach the level.

### 7. The famous trap: a list as a default

A list is a row of values between square brackets (lists get their own module). `append` adds a value at the end and changes the list itself, in place, without making a new list:

**`names.py`**

```python
names = []
names.append("Lukas")
names.append("Priya")
print(names)
```

```text
$ python names.py
['Lukas', 'Priya']
```

A sign-in sheet: `add_student` takes a name and a list called `students`. The idea sounds right: if nobody passes a list, start with an empty one (`students=[]`). Call it three times with no list:

**`trap.py`**

```python
def add_student(name, students=[]):
    students.append(name)
    return students

print(add_student("Lukas"))
print(add_student("Priya"))
print(add_student("Asha"))
```

```text
$ python trap.py
['Lukas']
['Lukas', 'Priya']
['Lukas', 'Priya', 'Asha']
```

Priya's call also shows Lukas, and Asha's call shows all three. A bug that shows only from the second call on, with no error at all. It is the mutable default trap. Python creates a default value once, when the `def` line runs, not each time you call the function. Picture a clipboard bought once when the office opened: every visitor who does not bring their own clipboard writes on the same one. A default of `10` is safe because nobody can write on the number ten.

The fix has a famous shape: make the default `None`, and create the list inside the function:

**`fix.py`**

```python
def add_student(name, students=None):
    if students is None:
        students = []
    students.append(name)
    return students

print(add_student("Lukas"))
print(add_student("Priya"))
team = ["Asha"]
print(add_student("Meera", team))
```

```text
$ python fix.py
['Lukas']
['Priya']
['Asha', 'Meera']
```

Lukas alone. Priya alone: each call got a fresh sheet. And the third call used our own list, `team`, with Asha already in it. The rule: never use a list (or any changeable value) as a default. Use `None` and create the list inside.

### 8. Two more slips

Using the blank names outside the function. We call `sale_price(price, percent)` but never created those labels:

**`outside.py`**

```python
def sale_price(price, percent=10):
    return price - price * percent / 100

print(sale_price(price, percent))
```

```text
$ python outside.py
Traceback (most recent call last):
  File "outside.py", line 4, in <module>
    print(sale_price(price, percent))
                     ^^^^^
NameError: name 'price' is not defined. Did you mean: 'print'?
```

The labels `price` and `percent` live only inside the function. And does a function change my own label? Outside we have `price` on 1000:

**`coupon.py`**

```python
def apply_coupon(price):
    price = price - 100
    return price

price = 1000
new_price = apply_coupon(price)
print(price, new_price)
```

```text
$ python coupon.py
1000 900
```

The outside `price` did not move. Two labels both named `price` sit on the same 1000 at the call. Inside, the function moves its own label to 900, and the outside label stays where it was.

## Interview tip

"What is the difference between a parameter and an argument?" A parameter is the name in the function definition. An argument is the value passed when the function is called.

## Common mistakes

- Positional arguments in the wrong order, or the wrong number of them.
- A positional argument after a keyword argument, or a misspelled keyword.
- A parameter without a default after one with a default.
- A list (or other changeable value) as a default: use `None` instead.
- Using a function's parameter names outside the function.

## Clean up

Nothing to clean up.

## Next

[M04-L03 · args and kwargs](../m04-l03-args-and-kwargs/)
