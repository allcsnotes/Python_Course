# M10-L01 · Type Hints

> Video: Module 10, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- What a type hint is, and what it is not: a note that Python stores and ignores
- How to write hints for parameters, results, defaults and `None`
- Hints for containers: `list[str]`, `dict[str, int]`, `tuple[str, int]`, and `str | None`
- How the checker `pyright` catches a wrong call before the program runs
- Four pitfalls: hints are not checked at run time, `Optional` is not an optional argument, hints that lie, and a hint alone makes no variable

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `uv` from module 7 for the pyright step (step 5). Docker is not needed.
- [M09-B05 · Build a Decorator Toolkit](../../m09-writing-pythonic-code/m09-b05-build-a-decorator-toolkit/README.md): the crash at the end of that build is the hook of this lesson.

## Files in this folder

| File | What it is |
|------|------------|
| `enrol.py` | The hook: `enrol` crashes when it gets the text `"Lukas"` instead of a user |
| `ignored.py` | `double` with a hint, called with text and a decimal: Python does not complain |
| `stored.py` | Python stores the hints in `__annotations__` |
| `types_a.py` | `int`, `str`, `bool` hints: `label` and `total_minutes` |
| `types_b.py` | A default value with a hint, and `-> None` |
| `catch.py` | `enrol` with hints, still passing the text `"Lukas"` (pyright will catch it) |
| `catch_fixed.py` | The same file with a real user: pyright reports zero errors |
| `cont_list.py` | `list[str]` in and out |
| `cont_dict.py` | `dict[str, int]` and `tuple[str, int]` |
| `none_find.py` | A function that returns `str | None` |
| `none_trap.py` | The `None` trap: `.upper()` on `None` |
| `optional_same.py` | `Optional[str]` is the same as `str | None` |
| `optional_param.py` | Pitfall 2: `Optional` does not make the argument optional |
| `wrong_hint.py` | Pitfall 3: a hint that lies |
| `var_only.py` | Pitfall 4: a hint alone does not create a variable |
| `tryit.py` | A model answer to the Try it yourself task |

## Follow along

### 1. The hook: a crash one step away from the mistake

At the end of module 9, Asha's toolkit crashed because someone passed the text `"Lukas"` instead of a user. Here is that mistake in a tiny program: a `User` class from module 8 with a `name` and a `logged_in` flag, and `enrol`, a function that refuses people who have not logged in. The first call passes Priya, a real user; the second passes plain text. Guess the output.

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    logged_in: bool = False


def enrol(user, course_id):
    if not user.logged_in:
        return f"{user.name} must log in first"
    return f"{user.name} joined {course_id}"


print(enrol(User("Priya", True), "C101"))
print(enrol("Lukas", "C101"))
```

```bash
python enrol.py
```

```
Priya joined C101
Traceback (most recent call last):
  File "enrol.py", line 17, in <module>
    print(enrol("Lukas", "C101"))
          ~~~~~^^^^^^^^^^^^^^^^^
  File "enrol.py", line 11, in enrol
    if not user.logged_in:
           ^^^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'logged_in'
```

The `AttributeError` message is correct, but it points inside `enrol`, one step away from the real mistake. The real mistake is the call, where we handed over the wrong kind of thing. What if your tools could shout about that call before you ever ran the program? They can, if you write down what each argument should be. That note is a **type hint**.

### 2. A hint is a note: Python ignores it

A speed-limit sign is only a note painted on a board; it cannot stop a car. Add a speed camera (a checker) and it reports every car that breaks the rule. Even without the camera, the sign is useful, because every driver knows what to expect. The kind of a value is its **type**; the sign is the type hint. Test whether Python obeys the sign. `double` hints `int` in and `int` out. We call it with `21`, with the text `"ab"` and with `2.5`:

```python
def double(n: int) -> int:
    return n * 2


print(double(21))
print(double("ab"))
print(double(2.5))
```

```bash
python ignored.py
```

```
42
abab
5.0
```

Python did not complain, not once. It even gave back text from a function that promised a whole number. Does Python at least keep the notes? Every function has a dictionary `__annotations__`:

```python
def double(n: int) -> int:
    return n * 2


print(double.__annotations__)
```

```bash
python stored.py
```

```
{'n': <class 'int'>, 'return': <class 'int'>}
```

The notes are stored (`n` maps to the class `int`, and `return` maps to `int`), but nobody looks at the shelf while the program runs. Tools do. So a type hint is a note: Python keeps it and ignores it. Its value comes from the people and the tools that read it.

### 3. The syntax

For each parameter: the name, a colon, the type. After the closing bracket an arrow `->` and the type of the result. Read `def enrol(user: User, course_id: str) -> str` like a sentence: enrol takes a `User` and a `course_id` that is text, and gives back text. Your own classes work as types too. The basic types you know are `int` (whole numbers), `str` (text), `float` (decimals), `bool` (`True`/`False`) and `None` (nothing).

```python
def label(title: str, minutes: int) -> str:
    return f"{title} ({minutes} min)"


def total_minutes(lessons: int, minutes: int) -> int:
    return lessons * minutes


def is_free(price: int) -> bool:
    return price == 0


print(label("Python Basics", 15))
print(total_minutes(12, 15))
print(is_free(499))
```

```bash
python types_a.py
```

```
Python Basics (15 min)
180
False
```

Each hint tells the reader what goes in and what comes out. Two more details: a default value goes after the hint with spaces around the equals sign (`rate: float = 0.18`), and a function that gives back nothing gets `-> None`.

```python
def price_with_gst(price: int, rate: float = 0.18) -> float:
    return price * (1 + rate)


def show(name: str) -> None:
    print("Course:", name)


print(price_with_gst(1000))
result = show("Python Basics")
print(result)
```

```bash
python types_b.py
```

```
1180.0
Course: Python Basics
None
```

A function without a `return` gives back `None` (module 4); `-> None` tells readers and tools: do not expect a value here.

### 4. Let a checker catch the mistake: pyright

Here is the hook program again with one change: the hints on `enrol`. The last line still passes the plain text `"Lukas"`. Python would crash exactly as before, because it ignores the hints.

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    logged_in: bool = False


def enrol(user: User, course_id: str) -> str:
    if not user.logged_in:
        return f"{user.name} must log in first"
    return f"{user.name} joined {course_id}"


print(enrol(User("Priya", True), "C101"))
print(enrol("Lukas", "C101"))
```

The camera is called **pyright**, a type checker made by Microsoft. It installs like any library in a `uv` project from module 7. `--dev` means only developers need it, the finished program does not. Create a project, copy `catch.py` and `catch_fixed.py` into it, and add pyright (the versions and the interpreter path will differ on your computer):

```bash
uv init --no-package --name hints
```

```
Initialized project `hints`
```

```bash
uv add --dev pyright
```

```
Using CPython 3.14.10+freethreaded
Creating virtual environment at: .venv
Resolved 4 packages in 309ms
Installed 3 packages in 211ms
 + nodeenv==1.11.0
 + pyright==1.1.414
 + typing-extensions==4.16.0
```

Now ask it to check the file. The very first time it fetches a small helper called node. It never runs the program. Guess what it reports and on which line.

```bash
uv run pyright catch.py
```

```
 * Install prebuilt node (26.13.0) ..... done.
catch.py
  catch.py:17:13 - error: Argument of type "Literal['Lukas']" cannot be assigned to parameter "user" of type "User" in function "enrol"
    "Literal['Lukas']" is not assignable to "User" (reportArgumentType)
1 error, 0 warnings, 0 informations
```

One error on line 17, column 13: the text `"Lukas"`. `Literal['Lukas']` just means the text `Lukas` typed straight into the code. In plain words: the function wanted a `User` and got text. Fix it by passing a real user, `User("Lukas")`, and check again:

```bash
uv run pyright catch_fixed.py
```

```
0 errors, 0 warnings, 0 informations
```

```bash
python catch_fixed.py
```

```
Priya joined C101
Lukas must log in first
```

Zero errors, and now the program runs: `Priya joined C101`, then `Lukas must log in first`.

The same checking can run inside your editor while you type. VS Code with the Python extension includes Pylance, which is built on pyright. By default it stays quiet about type mismatches. In the settings, set `python.analysis.typeCheckingMode` to `basic`.

### 5. Hints for lists, dictionaries and tuples

Put the type of the items in square brackets after the word `list`. Read the brackets as "of": a list of `str`, like a shelf of books.

```python
def first_names(students: list[str]) -> list[str]:
    return [name.split()[0] for name in students]


print(first_names(["Asha Rao", "Lukas Weber"]))
```

```bash
python cont_list.py
```

```
['Asha', 'Lukas']
```

A dictionary needs two types, one for the keys and one for the values: `dict[str, int]` is a dict from `str` to `int`, like a phone book from names to numbers. A tuple is a fixed group where each place has its own type: `tuple[str, int]` means exactly two items, first text, then a whole number. `cheapest` takes the dictionary and gives back such a pair. Guess the output:

```python
prices: dict[str, int] = {"C101": 499, "C102": 799}


def cheapest(prices: dict[str, int]) -> tuple[str, int]:
    code = min(prices, key=lambda c: prices[c])
    return code, prices[code]


print(cheapest(prices))
```

```bash
python cont_dict.py
```

```
('C101', 499)
```

`list[str]`: any number of items, all text. `dict[str, int]`: keys of one type, values of another. `tuple[str, int]`: a fixed pair. The brackets can nest, so `list[tuple[str, int]]` is a list of such pairs. In older code you will see capital `List` and `Dict` imported from `typing`; they mean exactly the same. Since Python 3.9 the plain lowercase words work by themselves.

### 6. Maybe nothing: `str | None`

Looking up a course that does not exist has nothing to give. How do we write "text or `None`"? With a vertical bar: `str | None`.

```python
COURSES = {"C101": "Python Basics", "C102": "SQL Basics"}


def find_title(course_id: str) -> str | None:
    return COURSES.get(course_id)


print(find_title("C101"))
print(find_title("C999"))
```

```bash
python none_find.py
```

```
Python Basics
None
```

The signature is honest: whoever calls this function knows that `None` may come back. And that matters, because `None` is a trap. Call `find_title` and ask for `.upper()` straight away, once for each code. Guess the output:

```python
COURSES = {"C101": "Python Basics", "C102": "SQL Basics"}


def find_title(course_id: str) -> str | None:
    return COURSES.get(course_id)


print(find_title("C101").upper())
print(find_title("C999").upper())
```

```bash
python none_trap.py
```

```
PYTHON BASICS
Traceback (most recent call last):
  File "none_trap.py", line 9, in <module>
    print(find_title("C999").upper())
          ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'upper'
```

The hint `str | None` was a warning: handle the `None` case before you use the text. A checker like pyright reads that warning and reports the line before the program runs.

In code written before Python 3.10 you will meet an older spelling: `Optional[str]`, from `typing`. Is it really the same thing? Let Python answer:

```python
from typing import Optional

print(Optional[str] == (str | None))
print(str | None)
print(Optional[str])
```

```bash
python optional_same.py
```

```
True
str | None
str | None
```

Read `Optional` as "maybe `None`". For new code prefer the bar: it needs no import and reads like English.

### 7. Why bother? Three reasons

1. Documentation that cannot go stale. A comment can become wrong without anyone noticing; a hint sits in the first line and a checker complains when the code disagrees with it.
2. Help from your editor. When it knows `user` is a `User`, it offers `name` and `logged_in` as soon as you type `user.`, and warns about a misspelled name.
3. Bugs found early. A mistake found by a checker costs seconds, before the program runs; the same mistake found by a customer costs trust.

Hints are optional, so teams add them step by step, usually on function signatures first, because that is where wrong values enter.

### 8. Pitfalls

**1. Believing that hints are checked while the program runs.** You saw it in step 2: `double` accepted text. If you need a real check at run time, write an `if` and raise an error, as in module 6.

**2. `Optional` does not mean the argument is optional.** `greet` takes `name: Optional[str]`. We call it with `None`, and then with nothing at all:

```python
from typing import Optional


def greet(name: Optional[str]):
    return f"Hello, {name}"


print(greet(None))
print(greet())
```

```bash
python optional_param.py
```

```
Hello, None
Traceback (most recent call last):
  File "optional_param.py", line 9, in <module>
    print(greet())
          ~~~~~^^
TypeError: greet() missing 1 required positional argument: 'name'
```

`Optional` only says the value may be `None`. To make the argument itself optional, give it a default: `name: str | None = None`.

**3. A hint that lies.** `average` says it gives back an `int`, but `sum / len` uses a slash, and a slash always gives a float.

```python
def average(prices: list[int]) -> int:
    return sum(prices) / len(prices)


print(average([100, 201]))
```

```bash
python wrong_hint.py
```

```
150.5
```

Python stays quiet because it ignores the sign. A checker would flag the line. A wrong hint is worse than no hint, because readers trust it. Keep hints true: here, `-> float`.

**4. A hint alone does not create a variable.**

```python
count: int
print(count)
```

```bash
python var_only.py
```

```
Traceback (most recent call last):
  File "var_only.py", line 2, in <module>
    print(count)
          ^^^^^
NameError: name 'count' is not defined. Did you mean: 'round'?
```

The hint only says what `count` will be. It does not make the name. Give it a value: `count: int = 0`.

### 9. Try it yourself: model answer

Write `full_price` with a `price: int` and a `gst: float` with a default. Write `first_word`, which gives back `str | None`. Call `full_price` with the text `"500"` and watch Python run until the multiplication fails. Then check the file with pyright. One answer:

```python
def full_price(price: int, gst: float = 0.18) -> float:
    return price * (1 + gst)


def first_word(text: str) -> str | None:
    words = text.split()
    return words[0] if words else None


print(full_price(500))
print(first_word("Type hints are notes"))
print(first_word(""))
print(full_price("500"))
```

```bash
python tryit.py
```

```
590.0
Type
None
Traceback (most recent call last):
  File "tryit.py", line 13, in <module>
    print(full_price("500"))
          ~~~~~~~~~~^^^^^^^
  File "tryit.py", line 2, in full_price
    return price * (1 + gst)
           ~~~~~~^~~~~~~~~~~
TypeError: can't multiply sequence by non-int of type 'float'
```

```bash
uv run pyright tryit.py
```

```
tryit.py
  tryit.py:13:18 - error: Argument of type "Literal['500']" cannot be assigned to parameter "price" of type "int" in function "full_price"
    "Literal['500']" is not assignable to "int" (reportArgumentType)
1 error, 0 warnings, 0 informations
```

Python runs until the multiplication fails at run time, but pyright reports the wrong call before anything runs.

## Common mistakes

1. Believing Python checks hints while the program runs. It does not; use pyright, or an `if` and `raise`.

2. Thinking `Optional[str]` makes an argument optional. It only means "may be `None`"; add `= None` for a default.

3. Writing a hint that is not true (`-> int` for a function that returns a float). A wrong hint is worse than none.

4. Writing `count: int` and expecting a variable to exist.

5. Using the result of a `str | None` function without handling `None` first.

## Clean up

Nothing to clean up on your computer except the `hints` project folder you made for pyright. Delete it when you are done.

## Next

Next lesson: [M10-L02 · Checking Types with Pyright, Generics and Protocol](../m10-l02-checking-types-with-pyright-generics-and-protocol/README.md). You will read pyright's messages properly, handle the `None` case, and write one function that works for a list of anything.

Your turn first: write `full_price` and `first_word` yourself, call `full_price` with the text `"500"`, and check the file with pyright.
