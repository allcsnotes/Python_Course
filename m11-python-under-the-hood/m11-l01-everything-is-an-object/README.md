# M11-L01 · Everything Is an Object

> Video: Module 11, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- The three things every Python object has: identity, type and value
- Why even a number has methods, and how to ask an object what it can do with `dir()`
- Why functions, classes and modules are objects too ("first class")
- The small integer cache: why `256 is 256` but `257 is 257` can be `False`, and string interning
- Why you compare values with `==`, and `None` with `is None`

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed.
- Names as labels on objects (module 5, lesson 6), the MRO (module 8, lesson 4) and `__eq__` (module 8, lesson 5).

## Files in this folder

| File | What it is |
|------|------------|
| `three.py` | Identity, type and value of a number |
| `number_methods.py` | A number has methods |
| `dir_names.py` | What can the number 7 do? Ask with `dir()` |
| `kinds.py` | Nine different things, one loop |
| `func_obj.py` | A function is an object |
| `class_obj.py` | A class is an object |
| `module_obj.py` | A module is an object |
| `family.py` | The family tree (`__mro__`) and what sits on top |
| `cache.py` | The small integer cache: -5 to 256 |
| `cache_file.py` | The 257 example as a file |
| `intern_demo.py` | String interning with `sys.intern` |
| `seats_bug.py` | Bug: `is` instead of `==` on a number |
| `seats_fix.py` | The fix: `==` |
| `none_one.py` | There is only one `None` |
| `eq_lies.py` | `==` can lie, `is` cannot |
| `admin_bug.py` | Pitfall: forgetting the brackets on a method |
| `discount_bug.py` | Pitfall: `not discount` with a value of 0 |
| `tryit.py` | A model answer to the Try it yourself tasks |

## Follow along

### 1. The hook: two numbers, two answers

Asha is playing with numbers in the REPL (type `python` and press Enter). She types `a = 256`, `b = 256`, then asks a question you know from module 5: `a is b`. Are the two labels on the very same object? Then the same with a number one bigger. Guess the output.

```pycon
>>> a = 256
>>> b = 256
>>> a is b
True
>>> a = 257
>>> b = 257
>>> a is b
False
```

256 shared one object; 257 did not. A number one bigger and a different answer, with no error and nothing broken. It is a deliberate choice, and it shows how Python stores every value. Today we look under the hood.

### 2. Identity, type and value

In module 5 you learned that a name is a label stuck on an object. Today is about the object itself. Think of a parcel in a warehouse: a tracking number that belongs to this one parcel only, a kind printed on the box, and what is inside. Every Python object has exactly these three things: an **identity** (a number that tells this object apart from every other; the function `id()` gives it), a **type** (`type()` tells you) and a **value** (what is inside). The identity never changes while the object lives, and neither does the type. Only the value can change, and only for a mutable object like a list.

The big claim of this lesson: every value in Python is an object, with an identity, a type and a value. Not only lists and your own classes: numbers, text, `None`, even functions, classes and modules. Check it, starting with a plain number. Guess the three lines:

```python
price = 1999
print(id(price))
print(type(price))
print(price)
```

```bash
python three.py
```

```
4414891120
<class 'int'>
1999
```

First a long number, the identity (yours will be different, so do not copy it). Then `class 'int'`, the type. Then `1999`, the value.

### 3. Even a number has methods

Because a number is an object it can have methods, just like a list has `append`. In many languages a number is raw data with no abilities. In Python it is an object that can do things. `as_integer_ratio()` asks a decimal for its fraction, `is_integer()` asks whether it is a whole number, and `seats.__add__(5)` is the plain `seats + 5` written out. Guess the four lines:

```python
share = 0.75
seats = 7
print(share.as_integer_ratio())
print(share.is_integer())
print(seats.__add__(5))
print(seats + 5)
```

```bash
python number_methods.py
```

```
(3, 4)
False
12
12
```

0.75 is three quarters, which is not a whole number. The last two lines give the same answer: the plus sign is only a shortcut. Python turns it into a call of the `__add__` method on the number, the same idea as `__eq__` and `__len__` in module 8.

How do you find out what an object can do? Ask it, with `dir()`. We list the names of the number 7, keep the ones that do not start with an underscore, and join them. A long list, or an empty one?

```python
seats = 7
names = [
    n for n in dir(seats)
    if not n.startswith("_")
]
print(", ".join(names))
```

```bash
python dir_names.py
```

```
as_integer_ratio, bit_count, bit_length, conjugate, denominator, from_bytes, imag, is_integer, numerator, real, to_bytes
```

Eleven names. Some are methods (`bit_length`, `to_bytes`); some are plain values stored on the number, called **attributes** (`numerator`, `denominator`, `real`, `imag`). An attribute is a name that belongs to an object, and you reach it with a dot.

### 4. Functions, classes and modules are objects too

Test the claim on a whole row of different things: a number, a decimal, text, `None`, a function Asha wrote, a class she wrote, the `math` module, the built-in function `len`, and `type` itself. A loop prints the type name of each one. Guess the nine lines.

```python
import math


def greet(name):
    return f"Hello, {name}"


class Course:
    pass


things = [
    1999, 0.75, "Lukas", None,
    greet, Course, math, len, type,
]
for thing in things:
    print(type(thing).__name__)
```

```bash
python kinds.py
```

```
int
float
str
NoneType
function
type
module
builtin_function_or_method
type
```

Even `None` has a type. The function Asha defined is an object of type `function`. A class is an object too, and its type is called `type`. The `math` module is an object. And `type` itself has the type `type`. The loop treated all nine things the same way: each one is an object with a type. That is what "everything is an object" means.

Since a function is an object, you can do with it what you do with any object. `welcome = greet` (no brackets) sticks a second label on the function itself; it does not call it. You can even give the function an attribute of your own:

```python
def greet(name):
    return f"Hello, {name}"


welcome = greet
print(welcome("Lukas"))
print(welcome is greet)
print(greet.__name__)
greet.language = "English"
print(welcome.language)
```

```bash
python func_obj.py
```

```
Hello, Lukas
True
greet
English
```

Classes work the same way: `Product = Course` is a second label on the class itself, and `Product()` builds a course.

```python
class Course:
    pass


Product = Course
first = Product()
print(type(first))
print(type(Course))
print(Product is Course)
```

```bash
python class_obj.py
```

```
<class '__main__.Course'>
<class 'type'>
True
```

The type of `first` is `Course`: that course was made from the class. The type of `Course` is `type`: the class is itself an object, made by `type`. Modules too:

```python
import math

calc = math
print(type(math))
print(calc.sqrt(16))
print(calc is math)
print(math.__name__)
```

```bash
python module_obj.py
```

```
<class 'module'>
4.0
True
math
```

The `math` module is an object, `calc` is the same module under another label, and every module knows its own name. So functions, classes and modules can all be put in a variable, kept in a list and handed to other functions. Programmers say functions are *first class*. It only means: they are ordinary objects.

### 5. The family tree

Every class has a family tree, the MRO from module 8, lesson 4: the order Python searches. Here are three trees and what sits at the top. Guess the five lines:

```python
class Course:
    pass


print(Course.__mro__)
print(bool.__mro__)
print(type(Course))
print(type(type))
print(type(object))
```

```bash
python family.py
```

```
(<class '__main__.Course'>, <class 'object'>)
(<class 'bool'>, <class 'int'>, <class 'object'>)
<class 'type'>
<class 'type'>
<class 'type'>
```

`Course` has two members: `Course`, then `object`. `bool` has three: `bool`, `int`, `object`: a `True` or `False` is a kind of whole number, which is why `True + 1` is 2. Every family tree ends at `object`. The last three lines say: `Course` is made by `type`; `type` is made by `type` (the chain ends because `type` is its own type); and `object` is made by `type` too. So `object` is the top of every family tree, and `type` makes every class.

### 6. The mystery: 256 and 257

Why did 256 share one object and 257 did not? Picture a print shop that sells number tickets. Small numbers are needed all the time, so the shop prints them in advance and keeps them in a box. Ask for number 100 and you get a ready-made ticket, the very same ticket for everyone. Python does exactly this. When it starts, it makes a ready box of the whole numbers from -5 to 256. Whenever your program needs one of those, it hands out the same object. That box is the **small integer cache**. A number outside that range is built fresh each time. Test the edges: for each of five numbers we build the number twice, from text with `int(str(n))`, and ask whether the two are the same object:

```python
for n in [-6, -5, 0, 256, 257]:
    first = int(str(n))
    second = int(str(n))
    print(n, first is second)
```

```bash
python cache.py
```

```
-6 False
-5 True
0 True
256 True
257 False
```

The cache is exactly -5 to 256. We built the numbers from text on purpose. Here is the very first example again, but as a file: `a = 257`, `b = 257`, `print(a is b)`. In the REPL it said `False`. Guess what the file says.

```python
a = 257
b = 257
print(a is b)
```

```bash
python cache_file.py
```

```
True
```

`True`! The same two lines and a different answer. The REPL runs each line on its own, so each 257 is built separately. A file is prepared as a whole (module 1, lesson 4) and Python sees that the same number is used twice. So when you use `is` on numbers, the answer depends on the cache, on how the code was run and on the Python version. These are details of how Python is built, not rules of the language. Never write code that depends on them.

### 7. Strings are shared sometimes: interning

Text has a similar trick called **interning**: Python keeps one shared copy of some short texts, like words that look like variable names, because they are used again and again. Asha makes the text `python` two ways, typed directly and glued from six single letters with `join`. She asks: equal? The same object? Then she passes the glued one through `sys.intern` and asks again. Guess the three lines.

```python
import sys

first = "python"
second = "".join(["p", "y", "t", "h", "o", "n"])
print(first == second)
print(first is second)
third = sys.intern(second)
print(first is third)
```

```bash
python intern_demo.py
```

```
True
False
True
```

The texts are equal; the typed one and the glued one are two different objects; `intern` handed back the shared copy, the same object as the typed one. You will almost never call `intern` yourself. The point: whether two equal texts are one object depends on how they were made. `==` always gives the right answer for text. The word `is` does not.

### 8. Why `is` is a bug for values

Asha counts the seats in two halls, 500 each. A function adds them with `sum`. Then she checks `if total_seats(halls) is 1000` and prints `sold out`. But she wrote `is` instead of `==`. (Python 3.14 even warns about it.)

```python
def total_seats(halls):
    return sum(halls)


halls = [500, 500]
if total_seats(halls) is 1000:
    print("sold out")
else:
    print("seats left")
```

```bash
python seats_bug.py
```

```
seats_bug.py:6: SyntaxWarning: "is" with 'int' literal. Did you mean "=="?
  if total_seats(halls) is 1000:
seats left
```

`seats left`, although the halls are full. The sum was built while the program ran, a fresh object; it is not the object stored for the 1000 in the file, so the answer from `is` is `False`. The fix is one word: `==` compares the values.

```python
def total_seats(halls):
    return sum(halls)


halls = [500, 500]
if total_seats(halls) == 1000:
    print("sold out")
else:
    print("seats left")
```

```bash
python seats_fix.py
```

```
sold out
```

The rule: keep the word `is` for one question only, "the very same object?". For values like numbers, text and lists, use `==`. There is just one value we check with `is`: `None`.

### 9. Why `is None`

In module 2, lesson 4 you were told: write `is None`, not `== None`, and the reason would come in module 11. Here it is. How many copies of `None` exist? Exactly one. `nothing` is set to `None`; `result` is set to `print("saved")`, and `print` gives back `None`. Guess the output.

```python
nothing = None
result = print("saved")
print(nothing is result)
```

```bash
python none_one.py
```

```
saved
True
```

`saved`, then `True`. Two different places produced `None` and it is the same object. There is only one `None` in the whole of Python, shared by everyone: a **singleton**. Because there is only one, `is None` is the perfect question: is this label on the one and only `None`? It is fast and clear. Now, can `==` be fooled? Yes. A class decides what `==` means (`__eq__`, module 8). Here a helper says yes to every comparison:

```python
class Anything:
    def __eq__(self, other):
        return True


thing = Anything()
print(thing == None)
print(thing is None)
```

```bash
python eq_lies.py
```

```
True
False
```

`==` asked the object and the object lied: it says it equals `None`. But `is` asks Python itself, not the object, and nobody can change its answer. So `== None` usually works; `is None` always works. In real code a library object or a test helper may change `__eq__` and the bug is silent. The habit costs nothing: `is None` and `is not None`.

### 10. Two pitfalls

**1. Forgetting the brackets.** Asha's `User` class has a method `is_admin`. A function is an object and objects count as true (truthy, module 2). This user is not an admin. What does the `if` print?

```python
class User:
    def is_admin(self):
        return False


user = User()
if user.is_admin:
    print("Welcome, admin")
else:
    print("Welcome, student")
```

```bash
python admin_bug.py
```

```
Welcome, admin
```

`Welcome, admin` for a student. `user.is_admin` without brackets is not a call: it is the method object itself, and any function object counts as true. The fix: add the brackets so Python calls it and gets `False`.

**2. Checking for missing with `not`.** Asha has a `discount` of 0: a real value, which means no discount. She writes `if not discount` and then `if discount is None`. Guess both.

```python
discount = 0
if not discount:
    print("no discount set")
if discount is None:
    print("missing")
else:
    print("discount is", discount)
```

```bash
python discount_bug.py
```

```
no discount set
discount is 0
```

The first check printed `no discount set`, but the discount is zero, a real value. `not discount` is true for zero, empty text, an empty list and `None`. `is None` is true only for `None`. When the question is "is there a value at all?", use `is None`.

### 11. Try it yourself: model answer

Five small tasks: print the identity, type and value of a text; call a method on a decimal; put a function, a class and a module in a list and print their types; build two big numbers from text and compare them with `is` and `==`; and check something with `is None`. One answer:

```python
import math

title = "Python"
print(id(title) > 0, type(title), title)
print((2.5).is_integer())


def greet():
    pass


class Course:
    pass


for thing in [greet, Course, math]:
    print(type(thing).__name__)
big = int("1000")
same = int("1000")
print(big is same, big == same)


class Always:
    def __eq__(self, other):
        return True


item = Always()
print(item == None, item is None)
```

```bash
python tryit.py
```

```
True <class 'str'> Python
False
function
type
module
False True
True False
```

## Common mistakes

1. Comparing values with `is`. It checks identity, and the answer depends on caches and on how the code ran. Use `==`.

2. Checking `== None` instead of `is None`: a class can make `==` lie.

3. Forgetting the brackets on a method call (`user.is_admin`): a method object always counts as true.

4. Using `if not x` to test for "missing": 0, empty text and empty lists count as nothing too.

5. Writing code that depends on the small integer cache or on string interning.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next lesson: [M11-L02 · Memory and Garbage Collection](../m11-l02-memory-and-garbage-collection/README.md). Every object takes up space in memory. Who is still using each one, and who cleans up the rest?
