# M10-L04 · What's New in Modern Python

> Video: Module 10, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- Why the same file can work on one Python and crash on another (the version story)
- The walrus `:=` (3.8) and exception groups with `except*` (3.11)
- Better f-strings (3.12) and the new REPL (3.13)
- Template strings `t"..."` (3.14) and deferred hints (3.14)
- For each feature: which version brought it, and when to use it or not

## Before you start

- Python 3.14 or newer. Check with `python --version`. Template strings and deferred hints need 3.14.
- Docker is optional: the "on Python 3.13" runs below use the image `python:3.13.16-slim`. You can skip those runs or read the outputs only.
- Nothing else is needed. Features are explained from scratch.

## Files in this folder

| File | What it is |
|------|------------|
| `enrol.py` | The hook: a hint names a class written further down |
| `hints_ask.py` | The same classes, printing `__annotations__` |
| `hints_ghost.py` | A hint that names `Ghost`: it only fails when asked |
| `hints_quotes.py` | The old fix: the class name in quotes |
| `hints_future.py` | The old fix: `from __future__ import annotations` |
| `walrus_count.py` | The walrus in an `if` |
| `loop_old.py` | A sentinel loop with two `input()` calls |
| `walrus_loop.py` | The same loop with one `input()` and the walrus |
| `walrus_comp.py` | The walrus in a comprehension filter |
| `walrus_nobr.py` | Mistake: the walrus without round brackets |
| `walrus_stmt.py` | Mistake: the walrus as a plain line |
| `group_raise.py` | `send_all` raises an `ExceptionGroup` |
| `group_plain.py` | A plain `except` cannot catch a group |
| `group_catch.py` | `except*` splits the group |
| `group_part.py` | A kind with no block travels on |
| `group_mix.py` | Mistake: `except` and `except*` in one `try` |
| `fstr_quotes.py` | Reusing the same quotes in an f-string (3.12) |
| `fstr_multi.py` | An f-string expression on several lines (3.12) |
| `tstr_f.py` | An f-string builds an unsafe page |
| `tstr_look.py` | What a t-string holds |
| `tstr_safe.py` | `clean_html` escapes each value |
| `tstr_old.py` | A t-string printed (a syntax error on 3.13) |
| `tstr_add.py` | Mistake: adding a t-string to text |
| `tryit.py` | A model answer to the Try it yourself tasks |

## Follow along

### 1. The hook: same file, two Pythons, two different results

Asha writes two small classes on her laptop. An `Enrollment` holds a student and a course, and its `__init__` says with a type hint that `student` is a `Student`. The `Student` class is written below it. She runs it on her laptop, which has Python 3.14. Guess the output.

```python
class Enrollment:
    def __init__(self, student: Student, course: str):
        self.student = student
        self.course = course


class Student:
    def __init__(self, name: str):
        self.name = name


print(Enrollment(Student("Lukas"), "Python").student.name)
```

```bash
python enrol.py
```

```
Lukas
```

It works. Now she copies the same file to a server that was set up last year, with Python 3.13. Same file, same command. Guess again.

```bash
python enrol.py   # on Python 3.13
```

```
Traceback (most recent call last):
  File "enrol.py", line 1, in <module>
    class Enrollment:
    ...<2 lines>...
            self.course = course
  File "enrol.py", line 2, in Enrollment
    def __init__(self, student: Student, course: str):
                                ^^^^^^^
NameError: name 'Student' is not defined
```

`NameError: name 'Student' is not defined`. Python read the hint `student: Student` and looked for a class with that name, but that class comes later in the file, so it did not exist yet. Same code, two Pythons, two different results. Step 8 explains the fix that arrived in 3.14.

### 2. Python versions and features

Think of the apps on your phone: an update brings a new button, and a very old phone may not be able to run the new version. A new Python arrives every October; the first number stays 3 and the second goes up by one. A feature is born in one version, and code that uses it needs that version or newer. On an older Python the same line is a crash. Today's features on a timeline: **3.8** (2019) the walrus, **3.11** (2022) error groups, **3.12** (2023) better f-strings, **3.13** (2024) the new REPL, **3.14** (2025) template strings and deferred hints.

Remember `requires-python` from the `uv` project lesson? It is the promise that protects you: "this project needs 3.14 or newer" and `uv` refuses to run it on anything older. For every feature we ask three questions: what problem does it solve, which version brought it, and when is it a good idea or a bad one?

### 3. The walrus `:=` (Python 3.8)

The assignment expression is written `:=`; turn your head sideways: the colon is the eyes and the equals sign is the tusks. A shop assistant reads the price tag while picking up the item: both in one move. The walrus gives a value a name and uses it in the same place. Asha has five course titles. If there are more than three she wants a warning that says how many. The count is needed twice (the test and the message); the walrus names it inside the test. Guess the output:

```python
titles = ["Python", "SQL", "Git", "Go", "Rust"]
if (count := len(titles)) > 3:
    print(f"Too many titles: {count}")
```

```bash
python walrus_count.py
```

```
Too many titles: 5
```

Round brackets, `count := len(titles)`: Python works out `len`, puts the answer in `count`, and then compares `count` with 3. Keep the round brackets around the walrus part (see the mistakes below).

`len` is cheap, so you could call it twice. The walrus really helps when a call is slow or cannot be repeated. The classic case is asking a person a question. The sentinel loop from module 3 asks once before the loop and once at the end of every round:

```python
name = input("Student name: ")
while name != "done":
    print(f"Welcome, {name}")
    name = input("Student name: ")
print("Bye")
```

With the walrus there is one question, at the top. The three answers are typed by you (`Lukas`, `Priya`, `done`); the program below was run with exactly those answers:

```bash
python walrus_loop.py
```

```
Student name: Lukas
Welcome, Lukas
Student name: Priya
Welcome, Priya
Student name: done
Bye
```

Same behaviour, one question instead of two. A third place is a comprehension. Asha has five lines, some empty or only spaces, and wants the cleaned text without the empty ones. The first version calls `strip` twice; the second calls it once, in the filter:

```python
lines = ["Python", "  ", "SQL ", "", " Git"]
once = [x.strip() for x in lines if x.strip()]
print(once)
twice = [text for x in lines if (text := x.strip())]
print(twice)
```

```bash
python walrus_comp.py
```

```
['Python', 'SQL', 'Git']
['Python', 'SQL', 'Git']
```

When to use it: when it removes a repeated call or a duplicate line and the line stays easy to read. When not: when you are squeezing a whole program into one line. If you have to stop and puzzle over the line, write two plain lines instead.

### 4. Exception groups and `except*` (Python 3.11)

A school sends report cards to four parents by email. Two addresses have no `@`, one mail server is too slow. Not one problem, but different problems at once. In module 6 an exception was one note about one problem and the program stopped at the first. Python 3.11 has a note that holds many: an `ExceptionGroup`. Here `send_all` tries every email, collects the errors, and raises them together (the `.xx` addresses count as a slow server):

```python
def send_all(emails):
    errors = []
    for email in emails:
        if "@" not in email:
            errors.append(ValueError(f"bad: {email}"))
        elif email.endswith(".xx"):
            errors.append(TimeoutError(f"slow: {email}"))
    if errors:
        raise ExceptionGroup("mail failed", errors)

emails = ["asha@x.com", "lukas.com", "priya@y.xx", "meera"]
send_all(emails)
```

```bash
python group_raise.py
```

```
  + Exception Group Traceback (most recent call last):
  |   File "group_raise.py", line 12, in <module>
  |     send_all(emails)
  |     ~~~~~~~~^^^^^^^^
  |   File "group_raise.py", line 9, in send_all
  |     raise ExceptionGroup("mail failed", errors)
  | ExceptionGroup: mail failed (3 sub-exceptions)
  +-+---------------- 1 ----------------
    | ValueError: bad: lukas.com
    +---------------- 2 ----------------
    | TimeoutError: slow: priya@y.xx
    +---------------- 3 ----------------
    | ValueError: bad: meera
    +------------------------------------
```

The traceback shows the group with its three numbered sub-errors. A plain `except` does not work on a group:

```python
errors = [ValueError("bad address")]
try:
    raise ExceptionGroup("mail failed", errors)
except ValueError:
    print("caught")
```

```bash
python group_plain.py
```

```
  + Exception Group Traceback (most recent call last):
  |   File "group_plain.py", line 3, in <module>
  |     raise ExceptionGroup("mail failed", errors)
  | ExceptionGroup: mail failed (1 sub-exception)
  +-+---------------- 1 ----------------
    | ValueError: bad address
    +------------------------------------
```

The `ValueError` is inside the group, but the group itself is not a `ValueError`, so the plain `except` never matches (and the program ends with an unhandled group). The spelling that works is `except*`: a star right after `except`. Read it as: from the group, take out all the errors of this kind. With `as`, the name holds a smaller group with only those errors. Guess the output:

```python
def send_all(emails):
    errors = []
    for email in emails:
        if "@" not in email:
            errors.append(ValueError(f"bad: {email}"))
        elif email.endswith(".xx"):
            errors.append(TimeoutError(f"slow: {email}"))
    if errors:
        raise ExceptionGroup("mail failed", errors)

emails = ["asha@x.com", "lukas.com", "priya@y.xx", "meera"]

try:
    send_all(emails)
except* ValueError as group:
    print("bad addresses:", len(group.exceptions))
    for error in group.exceptions:
        print(" ", error)
except* TimeoutError as group:
    print("slow servers:", len(group.exceptions))
```

```bash
python group_catch.py
```

```
bad addresses: 2
  bad: lukas.com
  bad: meera
slow servers: 1
```

Both blocks ran, each with its own share of the group. Remember the rule from module 6: a plain `except` runs only the first block that matches. `except*` is different: the group is split and every matching block gets its part. What if one kind has no block?

```python
errors = [ValueError("bad"), TimeoutError("slow")]
try:
    raise ExceptionGroup("mail failed", errors)
except* ValueError:
    print("handled the value errors")
```

```bash
python group_part.py
```

```
handled the value errors
  + Exception Group Traceback (most recent call last):
  |   File "group_part.py", line 3, in <module>
  |     raise ExceptionGroup("mail failed", errors)
  | ExceptionGroup: mail failed (1 sub-exception)
  +-+---------------- 1 ----------------
    | TimeoutError: slow
    +------------------------------------
```

The `ValueError` is handled; the `TimeoutError` is left over and travels on up as a smaller group, so the program still stops. Nothing is swallowed silently.

Honest advice: you will rarely write exception groups by hand. You will meet them when many jobs run together, as in the async lessons of module 12. Use `except*` only when you are catching a group.

### 5. Better f-strings (Python 3.12)

f-strings (module 2) had annoying rules: inside the curly braces you could not use the same kind of quote that wraps the text, and the braces could not stretch over several lines. In 3.12 the rules were removed. Here `student["name"]` sits in double quotes inside an f-string that also uses double quotes. Before 3.12 that was a syntax error.

```python
student = {"name": "Lukas"}
print(f"Welcome, {student["name"]}!")
```

```bash
python fstr_quotes.py
```

```
Welcome, Lukas!
```

Second, several lines: a long calculation can sit on its own lines, even with a comment. Guess the output:

```python
price = 1999
count = 3
discount = 500
print(f"Total: {
    price * count  # three seats
    - discount
}")
```

```bash
python fstr_multi.py
```

```
Total: 5497
```

1999 times 3 is 5997, minus 500. The comment is ignored like any comment. When to use: reusing quotes is a real convenience for dictionary keys. Multiple lines inside braces are rarely needed: if an expression needs three lines, work it out on a line above and give it a name.

### 6. The new REPL (Python 3.13)

The REPL is where you typed `2 + 3` in module 1 and Python answered straight away. Python 3.13 brought a new one. Open it by typing `python` and try these (the colours cannot be shown here, so they are described):

- **Colour.** `1 / 0` shows the prompt in bold purple, numbers in yellow and the error in red. The code you type is coloured as you type it too (that part arrived in 3.14).
- **Blocks come back as one piece.** Type a two-line `for` loop and run it, then press the up arrow: the whole block comes back as one piece, ready to edit.
- **Plain `exit`.** In module 1 you typed `exit()` with brackets; now `exit` alone is enough, and the same goes for `quit` and `help`.
- **Three more keys** listed in the Python documentation: F1 opens help, F2 shows your history without the prompts and the output, F3 is paste mode for big pieces of code.

This is what the screens look like (plain text):

```pycon
>>> 1 / 0
Traceback (most recent call last):
  File "<python-input-0>", line 1, in <module>
    1 / 0
    ~~^~~
ZeroDivisionError: division by zero
>>> for n in range(2):
...     print(n)
... 
0
1
>>> exit
```

When to use it: always, it is the default. Remember, the REPL is a notepad for small ideas. Real code lives in files.

### 7. Template strings (Python 3.14)

First, a problem. Priya registers on allcsvideos.com and types her name. The website puts the name into a page with an f-string. But a mean visitor does not type a name: here it is the word Lukas between bold tags. Guess what the page contains.

```python
name = "<b>Lukas</b>"
print(f"<p>Hello {name}</p>")
```

```bash
python tstr_f.py
```

```
<p>Hello <b>Lukas</b></p>
```

The tags went straight into the page, so a browser would show Lukas in bold. A `<script>` tag would have run as a program. That attack is called *injection* and module 17 covers it. What if Python kept the fixed text and the inserted values apart, so your code could look at each value before gluing them together? That is a **template string**: put a `t` in front of the quotes. Think of a form letter with blanks. An f-string fills the blanks and seals the envelope; a t-string hands you the letter and the list of fillings separately, so a clerk can check each filling first. Here is a t-string and four prints: the fixed pieces, the values, the name that was inside the braces, and the whole thing. Which of these is a finished sentence?

```python
name = "Lukas"
page = t"<p>Hello {name}</p>"
print(page.strings)
print(page.values)
print(page.interpolations[0].expression)
print(page)
```

```bash
python tstr_look.py
```

```
('<p>Hello ', '</p>')
('Lukas',)
name
Template(strings=('<p>Hello ', '</p>'), interpolations=(Interpolation('Lukas', 'name', None, ''),))
```

Two pieces of fixed text; one value; the expression `name` (the code that stood inside the braces); and the last line is not a sentence at all. It is a template that holds all the parts. To make text from it you write a function. `clean_html` loops over the template, which gives the pieces in order. If a piece is an `Interpolation` (a value) it calls `escape` from the `html` module; otherwise it keeps the fixed text:

```python
from html import escape
from string.templatelib import Interpolation


def clean_html(template):
    parts = []
    for item in template:
        if isinstance(item, Interpolation):
            parts.append(escape(item.value))
        else:
            parts.append(item)
    return "".join(parts)


name = "<b>Lukas</b>"
print(clean_html(t"<p>Hello {name}</p>"))
```

```bash
python tstr_safe.py
```

```
<p>Hello &lt;b&gt;Lukas&lt;/b&gt;</p>
```

The angle brackets became harmless codes. A browser shows them as plain characters, not as tags. Our own `<p>` tags stayed, because they were fixed text. The same idea can protect database queries: a function that receives a template could pass the values on separately instead of gluing them into the query text (module 17 shows the usual defence).

Template strings arrived in Python 3.14 (2025, PEP 750). On 3.13 the very same line is a syntax error:

```python
name = "Lukas"
print(t"Hello {name}")
```

```bash
python tstr_old.py
```

```
Template(strings=('Hello ', ''), interpolations=(Interpolation('Lukas', 'name', None, ''),))
```

```bash
python tstr_old.py   # on Python 3.13
```

```
  File "tstr_old.py", line 2
    print(t"Hello {name}")
           ^^^^^^^^^^^^^^
SyntaxError: invalid syntax
```

When to use them: most days you will not write these functions. Libraries will, so expect tools for HTML, queries and logs to accept t-strings. You write one when a library asks for it or when you need to check values before they are glued into text.

### 8. Deferred hints (Python 3.14)

Back to Asha's server. Before 3.14, Python worked out a hint the moment it read the `def` line. Think of a guest list checked at the door: a guest who arrives later is turned away. In 3.14, hints are stored, not worked out. They are evaluated only when somebody asks: a type checker, or your own code. So a hint can name a class that is written further down. This is the hook code. Let's ask: the last line prints `__annotations__`. Guess the output:

```python
class Enrollment:
    def __init__(self, student: Student, course: str):
        self.student = student
        self.course = course


class Student:
    def __init__(self, name: str):
        self.name = name


print(Enrollment.__init__.__annotations__)
```

```bash
python hints_ask.py
```

```
{'student': <class '__main__.Student'>, 'course': <class 'str'>}
```

`Student` is the class `Student` and `course` is the class `str`. The names were looked up only now, when we asked. By then `Student` existed. And a hint that names nothing real? It does no harm until somebody asks. Here the hint says `Ghost`. The function runs fine; then we ask for the annotations:

```python
def enrol(student: Ghost, course: str):
    return f"{course} for {student}"


print(enrol("Lukas", "Python"))
print(enrol.__annotations__)
```

```bash
python hints_ghost.py
```

```
Python for Lukas
Traceback (most recent call last):
  File "hints_ghost.py", line 6, in <module>
    print(enrol.__annotations__)
          ^^^^^^^^^^^^^^^^^^^^^
  File "hints_ghost.py", line 1, in __annotate__
    def enrol(student: Ghost, course: str):
                       ^^^^^
NameError: name 'Ghost' is not defined
```

`Python for Lukas` as normal, then `NameError: name 'Ghost' is not defined` at the moment of asking. Hints are lazy: they are checked late.

You will meet the old fixes in older code. Writing the name in quotes still works, and it also runs on the 3.13 server:

```python
class Enrollment:
    def __init__(self, student: "Student", course: str):
        self.student = student
        self.course = course


class Student:
    def __init__(self, name: str):
        self.name = name


print(Enrollment(Student("Lukas"), "Python").student.name)
```

```bash
python hints_quotes.py
```

```
Lukas
```

```bash
python hints_quotes.py   # on Python 3.13
```

```
Lukas
```

So does a line at the top of the file, `from __future__ import annotations`:

```python
from __future__ import annotations

class Enrollment:
    def __init__(self, student: Student, course: str):
        self.student = student
        self.course = course


class Student:
    def __init__(self, name: str):
        self.name = name


print(Enrollment(Student("Lukas"), "Python").student.name)
```

```bash
python hints_future.py
```

```
Lukas
```

```bash
python hints_future.py   # on Python 3.13
```

```
Lukas
```

When to use it: automatically, there is nothing to switch on. If your code must also run on older Pythons, like Asha's server, keep the quotes.

### 9. Five mistakes

**1. The walrus without round brackets.** Asha removes them. What does `count` hold?

```python
titles = ["Python", "SQL", "Git", "Go", "Rust"]
if count := len(titles) > 3:
    print(count)
```

```bash
python walrus_nobr.py
```

```
True
```

`True`, not 5. Without brackets Python first compares `len(titles)` with 3, which gives `True`, and the walrus stores that answer. The fix: round brackets around the walrus part.

**2. The walrus as a plain line.** `count := 5` on its own:

```python
count := 5
print(count)
```

```bash
python walrus_stmt.py
```

```
  File "walrus_stmt.py", line 1
    count := 5
          ^^
SyntaxError: invalid syntax
```

`SyntaxError: invalid syntax`, with arrows under the walrus. A walrus lives inside an expression. For a plain line, use the equals sign.

**3. Mixing `except` and `except*` in one `try`.**

```python
try:
    pass
except ValueError:
    pass
except* TimeoutError:
    pass
```

```bash
python group_mix.py
```

```
  File "group_mix.py", line 5
    except* TimeoutError:
    ^^^^^^^
SyntaxError: cannot have both 'except' and 'except*' on the same 'try'
```

`SyntaxError: cannot have both 'except' and 'except*' on the same 'try'`. Choose one style for each `try`: plain for a single error, star for a group.

**4. Treating a t-string as text.** Here we add it to a string:

```python
name = "Lukas"
print("Hello " + t"{name}")
```

```bash
python tstr_add.py
```

```
Traceback (most recent call last):
  File "tstr_add.py", line 2, in <module>
    print("Hello " + t"{name}")
          ~~~~~~~~~^~~~~~~~~~~
TypeError: can only concatenate str (not "string.templatelib.Template") to str
```

`TypeError: can only concatenate str (not "string.templatelib.Template") to str`. A template is not text yet. Run it through your function first.

**5. Using a new feature on an older Python** (the hook). Check the version on the machine that runs the code, write `requires-python` in your project, and test on the oldest Python you support.

### 10. Try it yourself: model answer

Five small tasks: a walrus loop, a comprehension with a walrus, an exception group caught with `except*`, an f-string with reused quotes, and a t-string that escapes its values. One answer:

```python
from html import escape
from string.templatelib import Interpolation

words = iter(["go", "sql", "stop", "rust"])
while (word := next(words)) != "stop":
    print(word)
lines = ["x", " ", "y "]
print([t for line in lines if (t := line.strip())])
try:
    raise ExceptionGroup("two", [ValueError("a"), KeyError("b")])
except* ValueError as group:
    print(len(group.exceptions))
except* KeyError as group:
    print(len(group.exceptions))
plan = {"name": "yearly"}
print(f"Plan: {plan["name"]}")
name = "<i>Asha</i>"
parts = [escape(i.value) if isinstance(i, Interpolation) else i for i in t"<p>{name}</p>"]
print("".join(parts))
```

```bash
python tryit.py
```

```
go
sql
['x', 'y']
1
1
Plan: yearly
<p>&lt;i&gt;Asha&lt;/i&gt;</p>
```

## Common mistakes

1. Writing the walrus without round brackets: it stores the comparison result (`True`), not the value.

2. Using `:=` as a plain statement: use `=`.

3. Mixing `except` and `except*` in the same `try`.

4. Adding a t-string to text. Pass it through a function that turns it into a `str`.

5. Using a 3.14 feature on a server that still runs 3.13. Set `requires-python` and test on the oldest Python you support.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next lesson: [M11-L01 · Everything Is an Object](../../m11-python-under-the-hood/m11-l01-everything-is-an-object/README.md). You have seen what Python can do; next we look under the hood and ask what a value really is inside Python.
