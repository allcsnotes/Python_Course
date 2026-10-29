# M10-L02 · Checking Types with Pyright, Generics and Protocol

> Video: Module 10, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- How to read a pyright message: file, line, column, level, sentence and rule
- How to handle `None` with a check, and how pyright narrows types (`reveal_type`)
- Why the hook was clean in standard mode, and how strict mode catches it
- One function for a list of anything: generics with `def first[T](items: list[T]) -> T`
- `Protocol`: duck typing written down, and why `Any` switches the checking off
- Four pitfalls: a leftover `reveal_type`, an unresolved import, `# type: ignore`, and instantiating a Protocol

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `uv` from module 7. Docker is not needed.
- [M10-L01 · Type Hints](../m10-l01-type-hints/README.md): you installed pyright there. Here you use it in a project folder called `allcs-site`.
- The pyright messages below were made with pyright 1.1.414 (in a clean project). Newer versions may word a message slightly differently.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | `add_gst` without hints: pyright is quiet, Python crashes (the hook) |
| `hook_fixed.py` | `add_gst` with hints, for strict mode |
| `errors.py` | A file with three mistakes on purpose |
| `errors_fixed.py` | The same file, fixed |
| `narrow1.py` | The `None` problem: `.upper()` on `str | None` |
| `narrow2.py` | The fix: an early return, with `reveal_type` |
| `narrow2_run.py` | The same without `reveal_type`, ready to run |
| `narrow3.py` | Narrowing with `isinstance` |
| `first_a.py` | `list` and `object`: pyright loses track |
| `first_b.py` | The same function twice, for `str` and for `int` |
| `first_t.py` | `first[T]`: one function for any list |
| `first_run.py` | `first[T]` at run time |
| `first_old.py` | The older spelling with `TypeVar` |
| `box.py` | A class with a blank: `Box[T]` |
| `proto1.py` | `Payable` Protocol with `Course`, `Bundle` and `Student` |
| `iterable.py` | `Iterable[str]` is a Protocol too |
| `any1.py` | `Any` switches the checking off |
| `any2.py` | `json.loads` returns `Any`, and `Any` spreads |
| `reveal_left.py` | Pitfall 1: `reveal_type` left in the file |
| `missing_import.py` | Pitfall 2: `import rich` that is not installed |
| `ignored.py` | Pitfall 3: `# type: ignore` hides a real bug |
| `make_protocol.py` | Pitfall 4: making an object from a Protocol |

## Follow along

### 1. The hook: pyright says everything is fine, then the program crashes

Asha adds `add_gst` to allcsvideos.com: it takes a price and adds 18 percent (`price * 118 // 100`). She wrote no hints. There are two calls: one with the number `999` and one with the text `"999"`. Last lesson she installed pyright, so she checks the file first. Guess two things: what will pyright report, and what will the program print?

First create the project (the video does the same; versions and the interpreter path will differ on your computer):

```bash
uv init --no-package
```

```
Initialized project `allcs-site`
```

```bash
uv add --dev pyright
```

```
Using CPython 3.14.10+freethreaded
Creating virtual environment at: .venv
Resolved 4 packages in 10ms
Installed 3 packages in 155ms
 + nodeenv==1.11.0
 + pyright==1.1.414
 + typing-extensions==4.16.0
```

```bash
cat pyproject.toml
```

```
[project]
name = "allcs-site"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = []

[dependency-groups]
dev = [
    "pyright>=1.1.414",
]
```

Now the hook file:

```python
def add_gst(price):
    return price * 118 // 100


print(add_gst(999))
print(add_gst("999"))
```

```bash
uv run pyright hook.py
```

```
 * Install prebuilt node (26.13.0) ..... done.
0 errors, 0 warnings, 0 informations
```

```bash
python hook.py
```

```
1178
Traceback (most recent call last):
  File "hook.py", line 6, in <module>
    print(add_gst("999"))
          ~~~~~~~^^^^^^^
  File "hook.py", line 2, in add_gst
    return price * 118 // 100
           ~~~~~~~~~~~~^^~~~~
TypeError: unsupported operand type(s) for //: 'str' and 'int'
```

Pyright says everything is fine and the very next line crashes. Is the camera broken? No, but to see why it stayed quiet we first have to learn to read what pyright says.

### 2. Reading pyright's messages

Before a book is printed a proofreader reads every page. They never print the book; they only put a note in the margin: which page, which line, what is wrong, and which rule it breaks. Pyright is that proofreader. Here is a file with three mistakes on purpose: `total` takes a list of ints and promises text, `shout` has the typo `uper`, and the last line calls `total` with two arguments.

```python
def total(prices: list[int]) -> str:
    return sum(prices)


def shout(title: str) -> str:
    return title.uper()


print(total([999, 499], 5))
```

```bash
uv run pyright errors.py
```

```
errors.py
  errors.py:2:12 - error: Type "int" is not assignable to return type "str"
    "int" is not assignable to "str" (reportReturnType)
  errors.py:6:18 - error: Cannot access attribute "uper" for class "str"
    Attribute "uper" is unknown (reportAttributeAccessIssue)
  errors.py:9:25 - error: Expected 1 positional argument (reportCallIssue)
3 errors, 0 warnings, 0 informations
```

Read a message like an address: the file name, then line 2, column 12 (how many characters from the left), then the level (`error`), a plain-English sentence, and in brackets the name of the rule it breaks, for example `reportReturnType`.

- Message 1: the type `int` is not assignable to the return type `str`. "Assignable" means allowed to go into that slot. The function promised text and this line gives back a number.
- Message 2: cannot access attribute `uper` for class `str`. It is the typo, caught before the program runs.
- Message 3: expected 1 positional argument. A positional argument is one you pass by its place (module 4). `total` takes one and we passed two.

Pyright uses three levels. An **error** is a mismatch it is sure about. A **warning** is something suspicious that might be on purpose. An **information** is only a note. The last line counts them all. One more detail for later modules: when pyright finds errors the command ends with exit code 1. A build server uses that number to stop a bad change.

```bash
echo $?
```

```
1
```

Fix all three (`-> int`, `upper`, one argument) and check again:

```python
def total(prices: list[int]) -> int:
    return sum(prices)


def shout(title: str) -> str:
    return title.upper()


print(total([999, 499]))
print(shout("python"))
```

```bash
uv run pyright errors_fixed.py
```

```
0 errors, 0 warnings, 0 informations
```

```bash
echo $?
```

```
0
```

Zero errors and exit code 0. Now the program runs:

```bash
python errors_fixed.py
```

```
1498
PYTHON
```

### 3. Handling `None` and narrowing

The question the last lesson left open: what do you do about `None`? Here is `find_title` with its honest signature `str | None`, and `show`, which asks for `.upper()` straight away. Guess what pyright says.

```python
COURSES = {"C101": "Python Basics", "C102": "SQL Basics"}


def find_title(course_id: str) -> str | None:
    return COURSES.get(course_id)


def show(course_id: str) -> None:
    title = find_title(course_id)
    print(title.upper())
```

```bash
uv run pyright narrow1.py
```

```
narrow1.py
  narrow1.py:10:17 - error: "upper" is not a known attribute of "None" (reportOptionalMemberAccess)
1 error, 0 warnings, 0 informations
```

The rule is called `reportOptionalMemberAccess`. Pyright read the signature: `find_title` may give back `None`, and `None` has no `upper`. It reports the line before the program has run. The cure is to check first, like a door with a sign: if the box is empty, stop here. We use an early return (module 4). To see what pyright believes there is a helper, `reveal_type(name)`: it prints the type pyright has worked out for that name on that line. It is not part of Python, only pyright understands it, so we remove it before running.

```python
COURSES = {"C101": "Python Basics", "C102": "SQL Basics"}


def find_title(course_id: str) -> str | None:
    return COURSES.get(course_id)


def show(course_id: str) -> None:
    title = find_title(course_id)
    reveal_type(title)
    if title is None:
        print("No such course")
        return
    reveal_type(title)
    print(title.upper())


show("C101")
show("C999")
```

```bash
uv run pyright narrow2.py
```

```
narrow2.py
  narrow2.py:10:17 - information: Type of "title" is "str | None"
  narrow2.py:14:17 - information: Type of "title" is "str"
0 errors, 0 warnings, 2 informations
```

Read the two informations. On line 10, before the check, `title` is `str | None`. On line 14, after the check, it is `str`. And 0 errors: the call to `upper` is allowed now. The `if` lets only one kind of value continue past the `return`, so pyright makes the type narrower step by step as it follows your code. That is called **narrowing**. Remove `reveal_type` and the program runs; pyright reports zero errors for this version too.

```python
COURSES = {"C101": "Python Basics", "C102": "SQL Basics"}


def find_title(course_id: str) -> str | None:
    return COURSES.get(course_id)


def show(course_id: str) -> None:
    title = find_title(course_id)
    if title is None:
        print("No such course")
        return
    print(title.upper())


show("C101")
show("C999")
```

```bash
uv run pyright narrow2_run.py
```

```
0 errors, 0 warnings, 0 informations
```

```bash
python narrow2_run.py
```

```
PYTHON BASICS
No such course
```

Other checks narrow too. `label` takes a price that is an `int` or text. Inside the `if isinstance(price, str)`, pyright knows `price` is text, so `upper` is allowed; after the `return` only `int` is left:

```python
def label(price: int | str) -> str:
    reveal_type(price)
    if isinstance(price, str):
        reveal_type(price)
        return price.upper()
    reveal_type(price)
    return f"Rs {price}"
```

```bash
uv run pyright narrow3.py
```

```
narrow3.py
  narrow3.py:2:17 - information: Type of "price" is "int | str"
  narrow3.py:4:21 - information: Type of "price" is "str"
  narrow3.py:6:17 - information: Type of "price" is "int"
0 errors, 0 warnings, 3 informations
```

So these checks all narrow: `if x is None`, `if x is not None`, `isinstance`, and even a plain `if x` (because `None` and empty text both count as false). Whichever you choose, the checker follows it.

### 4. Strict mode: why the hook was quiet

Think of the speed camera: it compares each car with the sign. `add_gst` has no signs. With no hint, pyright treats the parameter as *unknown*, meaning it could be anything, and anything is allowed. Pyright has levels of strictness. **Standard** is the default for the command: it checks the signs that exist and trusts you about the rest. **Strict** wants every sign to exist. You choose the level in `pyproject.toml` (module 7) under a `[tool.pyright]` heading. Add these two lines at the end (below, we do it with a command and then show the file):

```bash
cat pyproject.toml
```

```
[project]
name = "allcs-site"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = []

[dependency-groups]
dev = [
    "pyright>=1.1.414",
]

[tool.pyright]
typeCheckingMode = "strict"
```

Same file as the hook, same pyright, strict mode. Guess: still zero errors?

```bash
uv run pyright hook.py
```

```
hook.py
  hook.py:1:5 - error: Return type is unknown (reportUnknownParameterType)
  hook.py:1:13 - error: Type of parameter "price" is unknown (reportUnknownParameterType)
  hook.py:1:13 - error: Type annotation is missing for parameter "price" (reportMissingParameterType)
  hook.py:2:12 - error: Return type is unknown (reportUnknownVariableType)
  hook.py:6:7 - error: Argument type is unknown
    Argument corresponds to parameter "values" in function "print" (reportUnknownArgumentType)
5 errors, 0 warnings, 0 informations
```

Five errors: the return type is unknown, the parameter `price` is unknown, the type annotation is missing, and `print` receives an unknown argument. Add the signs (`price: int`, `-> int`) and run pyright again, still in strict mode:

```bash
uv run pyright hook_fixed.py
```

```
hook_fixed.py
  hook_fixed.py:6:15 - error: Argument of type "Literal['999']" cannot be assigned to parameter "price" of type "int" in function "add_gst"
    "Literal['999']" is not assignable to "int" (reportArgumentType)
1 error, 0 warnings, 0 informations
```

Now it reports the real bug: on line 6, the argument `Literal['999']` cannot be assigned to parameter `price` of type `int`. The text was caught before the program ran. Remove the two `[tool.pyright]` lines again to go back to standard mode (the later outputs in this README use standard mode):

Which level should you use? Start with standard. Use strict for new code, or for one important file at a time. If you switch an old project to strict in one step you will get hundreds of errors. Add hints to function signatures first: they matter most.

### 5. Generics: one function for a list of anything

Asha needs the first item of a list. For a list of titles, `first_str`; for a list of prices, `first_int`. Same body written twice with different hints:

```python
def first_str(items: list[str]) -> str:
    return items[0]


def first_int(items: list[int]) -> int:
    return items[0]


print(first_str(["Python", "SQL Basics"]).upper())
print(first_int([999, 499]) + 1)
```

```bash
python first_b.py
```

```
PYTHON
1000
```

A shortcut: write `list` with nothing inside and say the result is `object`, the most general type. Does pyright complain about `.upper()` on the result?

```python
def first(items: list) -> object:
    return items[0]


titles = ["Python", "SQL Basics"]
print(first(titles).upper())
```

```bash
uv run pyright first_a.py
```

```
first_a.py
  first_a.py:6:21 - error: Cannot access attribute "upper" for class "object"
    Attribute "upper" is unknown (reportAttributeAccessIssue)
1 error, 0 warnings, 0 informations
```

The program would work, because the first item really is text, but pyright lost track: all it knows is that some `object` came out. The idea: a form with a blank to fill in. The first item of a list of *blank* is a *blank*, the same word in both places. Fill in `str` and the answer is `str`. Python's name for such a blank is a **type variable**, and the usual name is `T`. Right after the function name, square brackets declare the blank:

```python
def first[T](items: list[T]) -> T:
    return items[0]


titles = ["Python", "SQL Basics"]
prices = [999, 499]
reveal_type(first(titles))
reveal_type(first(prices))
print(first(prices).upper())
```

```bash
uv run pyright first_t.py
```

```
first_t.py
  first_t.py:7:13 - information: Type of "first(titles)" is "str"
  first_t.py:8:13 - information: Type of "first(prices)" is "int"
  first_t.py:9:21 - error: Cannot access attribute "upper" for class "int"
    Attribute "upper" is unknown (reportAttributeAccessIssue)
1 error, 0 warnings, 2 informations
```

Pyright fills in the blank at each call from the list you pass: `first(titles)` is `str`, `first(prices)` is `int`, and `.upper()` on a price is now an error (`cannot access attribute "upper" for class "int"`). At run time nothing changes, Python ignores the blank like every hint:

```bash
python first_run.py
```

```
PYTHON
1000
```

Before Python 3.12 you wrote the same thing differently, and you will meet it in older code: import `TypeVar` and write `T = TypeVar("T")`. It means exactly the same:

```python
from typing import TypeVar

T = TypeVar("T")


def first(items: list[T]) -> T:
    return items[0]


reveal_type(first(["Python", "SQL Basics"]))
print(first([999, 499]))
```

```bash
uv run pyright first_old.py
```

```
first_old.py
  first_old.py:10:13 - information: Type of "first(["Python", "SQL Basics"])" is "str"
0 errors, 0 warnings, 1 information
```

Classes can have blanks too. `Box[T]` keeps one item and its `get` method gives that item back. A box with text is a `Box[str]`; a box with a number is a `Box[int]`. This is how `list[str]` from the last lesson works.

```python
class Box[T]:
    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item


title_box = Box("Python")
price_box = Box(999)
reveal_type(title_box)
reveal_type(price_box.get())
```

```bash
uv run pyright box.py
```

```
box.py
  box.py:11:13 - information: Type of "title_box" is "Box[str]"
  box.py:12:13 - information: Type of "price_box.get()" is "int"
0 errors, 0 warnings, 2 informations
```

```bash
python box.py
```

```
Traceback (most recent call last):
  File "box.py", line 11, in <module>
    reveal_type(title_box)
    ^^^^^^^^^^^
NameError: name 'reveal_type' is not defined
```

### 6. Protocol: duck typing written down

A wall socket does not care which brand the plug is. It only cares about the pins. If the pins fit, it works. Python thinks the same way: if it walks like a duck and quacks like a duck, treat it as a duck. You met it in the iterables lesson (any object with `__iter__` and `__next__` is an iterator) and in the context managers lesson (any object with `__enter__` and `__exit__` works in a `with`). We called that a **protocol**: an agreed set of methods.

The problem: `checkout` should take a `Course` or a `Bundle`. Both have a method `amount` that gives the price in rupees, but they are different classes with no shared parent. With a bar we could write `Course | Bundle`, but every new class would mean editing the hint. The tool for this is a `Protocol`: a class with `Protocol` in brackets and one method, `amount`, whose body is three dots (no code, it only describes). Read it: anything that has an `amount` method returning an `int` is `Payable`. `Course` and `Bundle` are ordinary dataclasses with an `amount` method; neither mentions `Payable`. No inheritance, no sign-up. Guess which line pyright flags:

```python
from dataclasses import dataclass
from typing import Protocol


class Payable(Protocol):
    def amount(self) -> int: ...


@dataclass
class Course:
    title: str
    price: int

    def amount(self) -> int:
        return self.price


@dataclass
class Bundle:
    courses: list[Course]

    def amount(self) -> int:
        return sum(c.price for c in self.courses)


@dataclass
class Student:
    name: str


def checkout(item: Payable) -> str:
    return f"Pay Rs {item.amount()}"


python = Course("Python", 999)
sql = Course("SQL Basics", 499)
print(checkout(python))
print(checkout(Bundle([python, sql])))
print(checkout(Student("Lukas")))
```

```bash
uv run pyright proto1.py
```

```
proto1.py
  proto1.py:39:16 - error: Argument of type "Student" cannot be assigned to parameter "item" of type "Payable" in function "checkout"
    "Student" is incompatible with protocol "Payable"
      "amount" is not present (reportArgumentType)
1 error, 0 warnings, 0 informations
```

```bash
python proto1.py
```

```
Pay Rs 999
Pay Rs 1498
Traceback (most recent call last):
  File "proto1.py", line 39, in <module>
    print(checkout(Student("Lukas")))
          ~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "proto1.py", line 32, in checkout
    return f"Pay Rs {item.amount()}"
                     ^^^^^^^^^^^
AttributeError: 'Student' object has no attribute 'amount'
```

Only the last call is flagged: `Student` is incompatible with protocol `Payable`, `amount` is not present. The first two calls are fine and `Course` and `Bundle` never named `Payable`. At run time Python does not read the protocol: the first two lines print, then Lukas crashes with `AttributeError`. The protocol warned you before the run.

In module 8 you met abstract classes: a parent names the methods and each child must inherit from it, by name. A Protocol needs no inheritance; pyright checks by shape, not by family tree. Use an abstract class when you own all the classes and want shared code; use a Protocol when the objects come from anywhere. You have used protocols all along: `Iterable` from `collections.abc` is one (anything with `__iter__`). `count_titles` takes an `Iterable[str]`. Guess which of the four calls pyright flags:

```python
from collections.abc import Iterable


def count_titles(titles: Iterable[str]) -> int:
    return sum(1 for _ in titles)


print(count_titles(["Python", "SQL"]))
print(count_titles(("Python", "SQL", "Git")))
print(count_titles(t.title() for t in ["a", "b"]))
print(count_titles(42))
```

```bash
uv run pyright iterable.py
```

```
iterable.py
  iterable.py:11:20 - error: Argument of type "Literal[42]" cannot be assigned to parameter "titles" of type "Iterable[str]" in function "count_titles"
    "Literal[42]" is incompatible with protocol "Iterable[str]"
      "__iter__" is not present (reportArgumentType)
1 error, 0 warnings, 0 informations
```

```bash
python iterable.py
```

```
2
3
2
Traceback (most recent call last):
  File "iterable.py", line 11, in <module>
    print(count_titles(42))
          ~~~~~~~~~~~~^^^^
  File "iterable.py", line 5, in count_titles
    return sum(1 for _ in titles)
                          ^^^^^^
TypeError: 'int' object is not iterable
```

Only `42`: it is incompatible with protocol `Iterable[str]`, `__iter__` is not present. At run time the first three calls work and the last one crashes with `TypeError: 'int' object is not iterable`: the same sentence from the checker and from Python.

### 7. `Any`: the escape hatch

`Any` from `typing` means "could be anything, do not check it". `read_price` takes a `course: Any` and returns `course.price`. We call it with the text `"Python"`. Guess what pyright says and what the program does.

```python
from typing import Any


def read_price(course: Any) -> int:
    return course.price


print(read_price("Python"))
```

```bash
uv run pyright any1.py
```

```
0 errors, 0 warnings, 0 informations
```

```bash
python any1.py
```

```
Traceback (most recent call last):
  File "any1.py", line 8, in <module>
    print(read_price("Python"))
          ~~~~~~~~~~^^^^^^^^^^
  File "any1.py", line 5, in read_price
    return course.price
           ^^^^^^^^^^^^
AttributeError: 'str' object has no attribute 'price'
```

Zero errors, and the program crashes. `Any` switched the camera off for this value: whatever you do with it is allowed, even something that cannot work. Compare it with `object` from before: `object` accepts every value but allows almost nothing, so `upper` was an error; `Any` accepts every value and allows everything. That is why it is called an escape hatch.

`Any` also spreads, and it sneaks in without you writing it. `json.loads` (the JSON lesson) returns `Any`:

```python
import json

raw = '{"title": "Python", "price": 999}'
data = json.loads(raw)
reveal_type(data)
reveal_type(data["price"])
```

```bash
uv run pyright any2.py
```

```
any2.py
  any2.py:5:13 - information: Type of "data" is "Any"
  any2.py:6:13 - information: Type of "data["price"]" is "Any"
0 errors, 0 warnings, 2 informations
```

Everything that comes out of an `Any` is `Any`. One small hole and the checking stops. (Running this file in Python would fail with `NameError: name 'reveal_type' is not defined`, see pitfall 1.) So avoid writing `Any` yourself. There are better tools and you know them now: the exact type, a union with the bar for a few choices, a blank `T` for any type that stays the same, and a `Protocol` for anything with the right methods.

### 8. Four pitfalls

**1. `reveal_type` left in the file.** Pyright understands it and prints the type. What does Python do?

```python
price = 999
reveal_type(price)
print(price)
```

```bash
uv run pyright reveal_left.py
```

```
reveal_left.py
  reveal_left.py:2:13 - information: Type of "price" is "Literal[999]"
0 errors, 0 warnings, 1 information
```

```bash
python reveal_left.py
```

```
Traceback (most recent call last):
  File "reveal_left.py", line 2, in <module>
    reveal_type(price)
    ^^^^^^^^^^^
NameError: name 'reveal_type' is not defined
```

Pyright says the type of `price` is `int`; Python says `NameError: name 'reveal_type' is not defined`. `reveal_type` is only a helper for the checker. Delete it before you run, or import it from `typing`, where it prints a line when it runs.

**2. Import could not be resolved.** This file imports `rich`, but the project has no `rich`:

```python
from rich.table import Table

table = Table()
print(table)
```

```bash
uv run pyright missing_import.py
```

```
missing_import.py
  missing_import.py:1:6 - error: Import "rich.table" could not be resolved (reportMissingImports)
1 error, 0 warnings, 0 informations
```

```bash
python missing_import.py
```

```
Traceback (most recent call last):
  File "missing_import.py", line 1, in <module>
    from rich.table import Table
ModuleNotFoundError: No module named 'rich'
```

Pyright says the import could not be resolved; Python says `ModuleNotFoundError`, as you know from module 7. The fix is the same for both: `uv add rich`.

**3. `# type: ignore`.** A comment at the end of a line tells pyright to be quiet. `discount` takes an `int` price, but we pass the text `"999"` and hide the warning:

```python
def discount(price: int, percent: int) -> int:
    return price - price * percent // 100


print(discount("999", 10))  # type: ignore
```

```bash
uv run pyright ignored.py
```

```
0 errors, 0 warnings, 0 informations
```

```bash
python ignored.py
```

```
Traceback (most recent call last):
  File "ignored.py", line 5, in <module>
    print(discount("999", 10))  # type: ignore
          ~~~~~~~~^^^^^^^^^^^
  File "ignored.py", line 2, in discount
    return price - price * percent // 100
                   ~~~~~~~~~~~~~~~~^^~~~~
TypeError: unsupported operand type(s) for //: 'str' and 'int'
```

Pyright reports zero errors and the program crashes. Hiding a real warning does not fix it. Use `# type: ignore` only for a problem you understand and cannot fix.

**4. Making an object from a Protocol.**

```python
from typing import Protocol


class Payable(Protocol):
    def amount(self) -> int: ...


item = Payable()
```

```bash
uv run pyright make_protocol.py
```

```
make_protocol.py
  make_protocol.py:8:8 - error: Cannot instantiate Protocol class "Payable" (reportAbstractUsage)
1 error, 0 warnings, 0 informations
```

```bash
python make_protocol.py
```

```
Traceback (most recent call last):
  File "make_protocol.py", line 8, in <module>
    item = Payable()
  File "/usr/lib/python3.14/typing.py", line 1877, in _no_init_or_replace_init
    raise TypeError('Protocols cannot be instantiated')
TypeError: Protocols cannot be instantiated
```

Pyright: cannot instantiate Protocol class `Payable`. Python: `TypeError: Protocols cannot be instantiated`. A Protocol is only a description, like the shape of a socket. You cannot plug it into the wall.

## Common mistakes

1. Trusting a clean pyright run on a file with no hints: unknown means allowed. Use strict mode, or add hints to the signatures.

2. Using a `str | None` result without checking for `None` first (`reportOptionalMemberAccess`).

3. Leaving `reveal_type` in a file you run.

4. Silencing a real problem with `# type: ignore`.

5. Using `Any` to make an error go away. It switches the checking off for everything that touches the value.

6. Calling `Payable()` (making an object from a Protocol).

## Clean up

Nothing to clean up on your computer except the `allcs-site` project folder you made for pyright. Delete it when you are done.

## Next

Next lesson: [M10-L03 · TypedDict, Slots, NamedTuple and Pattern Matching](../m10-l03-typeddict-slots-namedtuple-and-pattern-matching/README.md). You will describe dictionary-shaped data, like JSON, with exact types, make small strict objects, and match values by their shape.

Your turn first: use `find_title` without checking for `None` and fix it with an early return; turn on strict mode and add hints to a small function; write `last[T]`; and write a Protocol with one method plus a class that fits it.
