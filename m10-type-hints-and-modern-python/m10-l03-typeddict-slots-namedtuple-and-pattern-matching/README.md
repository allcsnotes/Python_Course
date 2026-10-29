# M10-L03 · TypedDict, Slots, NamedTuple and Pattern Matching

> Video: Module 10, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- How to describe the keys of a dictionary with `TypedDict` (and `NotRequired`) so a checker can read it
- How `NamedTuple` gives a tuple names and why it never changes
- How `@dataclass(slots=True)` stops attribute typos and saves memory
- Which of the four to choose: dict, `TypedDict`, `NamedTuple` or data class
- `match`: sequence, mapping and class patterns, guards, `|` and `as`, and why a bare name captures

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `uv` from module 7 for the pyright steps (pyright is added the same way as in [M10-L02](../m10-l02-checking-types-with-pyright-generics-and-protocol/README.md)): `uv init --no-package`, then `uv add --dev pyright`. Docker is not needed.
- Dictionaries and JSON (modules 5 and 6), dataclasses and enums (module 8), `match` basics (module 3).

## Files in this folder

| File | What it is |
|------|------------|
| `dict_typo.py` | The hook: a typo in a dictionary key is found only when the line runs |
| `typed_dict.py` | `CourseData(TypedDict)`: the shape of the dictionary |
| `typed_bad.py` | The same with a typo and a wrong price: pyright finds both |
| `notrequired.py` | `NotRequired[str]` for a key that may be missing |
| `tuple_plain.py` | A plain tuple: position is the only name |
| `nt_basic.py` | `NamedTuple` with a default |
| `nt_more.py` | A named tuple is locked: `_replace` and `_asdict` |
| `dc_typo.py` | A data class accepts the typo `pirce` silently |
| `dc_slots.py` | `slots=True` turns the typo into an error |
| `slots_memory.py` | 100,000 courses with and without slots |
| `m_seq.py` | Sequence patterns: commands as lists |
| `m_trap.py` | The trap: `case FREE:` is a capture, not a comparison |
| `m_enum.py` | Compare with a dotted name: `Plan.FREE` |
| `m_map.py` | Mapping patterns: events as dictionaries |
| `m_class.py` | Class patterns: `Enrolled(student=who)` |
| `m_guard.py` | Guards: `case [...] if amount >= 5000` |
| `m_or.py` | `|` and `as chosen` |
| `m_nested.py` | Nested patterns |
| `together.py` | `TypedDict`, `NamedTuple` and `match` in one summary |
| `json_trust.py` | Mistake 1: a `TypedDict` is a promise, not a guard |
| `isinstance_td.py` | Mistake 2: `isinstance` with a `TypedDict` |
| `p_order.py` | Mistake 3: the broad case first |
| `p_string.py` | Mistake 4: text is not a sequence for `match` |

## Follow along

### 1. The hook: a typo found one line too late

Asha gets a course from the website as JSON text and loads it, as in module 6. It arrives as a dictionary, and she writes a small function to show the title and the price. Look closely: one key name is not quite right. Will Python warn her before the program runs, or only when that line runs?

```python
import json

text = '{"title": "Python Basics", "price": 1499}'
course = json.loads(text)


def show(course):
    return f"{course['title']} costs {course['pirce']}"


print(show(course))
```

```bash
python dict_typo.py
```

```
Traceback (most recent call last):
  File "dict_typo.py", line 11, in <module>
    print(show(course))
          ~~~~^^^^^^^^
  File "dict_typo.py", line 8, in show
    return f"{course['title']} costs {course['pirce']}"
                                      ~~~~~~^^^^^^^^^
KeyError: 'pirce'
```

`KeyError: 'pirce'`. Python found the typo only when the line ran. In a real program that line might run once a week, for one customer. A plain dictionary has no idea which keys are allowed. Today you fix that: write the shape of the data down once, so a checker can read it before the program runs.

### 2. `TypedDict`: the shape of a dictionary

Four tools today, in this order: `TypedDict` for dictionaries, `NamedTuple` for fixed records, `slots` for objects, and `match` for choosing by shape. First, a paper form with printed boxes: a clerk reads it before it is posted and sends it back if a box is missing or has the wrong kind of answer. The printed form is a `TypedDict`.

A plain hint `dict` says only "this is a dictionary". A `TypedDict` is a class that inherits from `TypedDict`, with the keys as annotations, the same notes you wrote on dataclass fields in module 8. Guess the two prints (the second asks Python for the type of the data):

```python
from typing import TypedDict


class CourseData(TypedDict):
    title: str
    price: int
    level: str


def show(course: CourseData) -> str:
    return f"{course['title']} costs Rs {course['price']}"


data: CourseData = {
    "title": "Python Basics",
    "price": 1499,
    "level": "beginner",
}
print(show(data))
print(type(data))
```

```bash
python typed_dict.py
```

```
Python Basics costs Rs 1499
<class 'dict'>
```

`type(data)` is `dict`. A `TypedDict` is not a new kind of object: it is an ordinary dictionary, and everything from module 5 still works. The class is only a description for the checker. Now the payoff. This file has Asha's typo and a price that is the text `"free"`. Python alone would not complain about the price, so we ask the checker first. Set up a pyright project as in the previous lesson (the versions and node download will differ on your computer):

```bash
uv init --no-package
```

```
Initialized project `shapes`
```

```bash
uv add --dev pyright
```

```
Using CPython 3.14.10+freethreaded
Creating virtual environment at: .venv
Resolved 4 packages in 5ms
Installed 3 packages in 114ms
 + nodeenv==1.11.0
 + pyright==1.1.414
 + typing-extensions==4.16.0
```

```python
from typing import TypedDict


class CourseData(TypedDict):
    title: str
    price: int
    level: str


def show(course: CourseData) -> str:
    return f"{course['title']} costs Rs {course['pirce']}"


data: CourseData = {
    "title": "Python Basics",
    "price": "free",
    "level": "beginner",
}
print(show(data))
```

```bash
uv run pyright typed_bad.py
```

```
 * Install prebuilt node (26.13.0) ..... done.
typed_bad.py
  typed_bad.py:11:42 - error: Could not access item in TypedDict
    "pirce" is not a defined key in "CourseData" (reportGeneralTypeIssues)
  typed_bad.py:16:14 - error: Type "dict[str, str]" is not assignable to declared type "CourseData"
    "Literal['free']" is not assignable to "int" (reportAssignmentType)
2 errors, 0 warnings, 0 informations
```

Two errors, and the program never ran. Line 11: `pirce` is not a defined key in `CourseData`. Line 16: the text `'free'` is not assignable to `int`. The checker looked over the form and found both mistakes.

Not every key must be present. A course may have a note, or not. Wrap the type in `NotRequired` from `typing`. Without that wrapper a missing key is an error for the checker. Two courses: `a` has no note, `b` has one. Guess both lines:

```python
from typing import NotRequired, TypedDict


class CourseData(TypedDict):
    title: str
    price: int
    note: NotRequired[str]


a: CourseData = {"title": "Python Basics", "price": 1499}
b: CourseData = {"title": "SQL", "price": 999, "note": "new"}
for course in (a, b):
    print(course["title"], course.get("note", "no note"))
```

```bash
python notrequired.py
```

```
Python Basics no note
SQL new
```

If you read a `NotRequired` key with square brackets, the checker warns you because the key might be missing. The old rule still holds: brackets for keys that must be there, `.get` with a default for keys that may not.

### 3. `NamedTuple`: a tuple with names

A printed train ticket has labelled columns (passenger, from, to, seat). Nobody scribbles on a ticket; if something changes you get a new one. In module 5 a course was a tuple: title, price, level. Guess the two prints:

```python
course = ("Python Basics", 1499, "beginner")
print(course[1])
print(course[2])
```

```bash
python tuple_plain.py
```

```
1499
beginner
```

It works, but nothing says that slot 1 is the price. You have to remember it, and a year later you will not. Position is the only name a tuple has. A `NamedTuple` keeps everything good about a tuple and adds names: import it from `typing` and write a class that inherits from it, with the fields as annotations, exactly like a dataclass. We make a course with two values so `level` takes its default. Guess all four lines:

```python
from typing import NamedTuple


class Course(NamedTuple):
    title: str
    price: int
    level: str = "beginner"


course = Course("Python Basics", 1499)
print(course)
print(course.price, course[1])
title, price, level = course
print(title, level)
```

```bash
python nt_basic.py
```

```
Course(title='Python Basics', price=1499, level='beginner')
1499 1499
Python Basics beginner
```

The print shows the class name and every field with its name. The price works by name and by position, unpacking works as before, and `level` came from the default. And like any tuple it cannot be changed: this file tries to set the price and catches the error. Then `_replace` builds a changed copy and `_asdict` turns the record into a dictionary.

```python
from typing import NamedTuple


class Course(NamedTuple):
    title: str
    price: int


course = Course("Python Basics", 1499)
try:
    course.price = 999
except AttributeError as error:
    print("error:", error)
cheaper = course._replace(price=999)
print(course.price, cheaper.price)
print(cheaper._asdict())
```

```bash
python nt_more.py
```

```
error: can't set attribute
1499 999
{'title': 'Python Basics', 'price': 999}
```

The old record is locked, `_replace` gave a new record with price 999 while the old one still says 1499, and `_asdict` gives a dictionary ready to be saved as JSON. (The underscore is not a warning: it only keeps these names apart from your field names.) Because it never changes, a named tuple can also be a dictionary key or an item in a set. Use it for small fixed records: a point on a map, a price range, a row of a table.

### 4. `slots=True`: stop attribute typos, save memory

A normal object is a cupboard where anyone can screw on an extra shelf at any time just by naming it. Misspell `price` and a new shelf appears quietly while the real one stays untouched. Here a dataclass has two fields; Asha misspells the name when she changes the price, then prints the price and asks `vars` what is inside.

```python
from dataclasses import dataclass


@dataclass
class Course:
    title: str
    price: int


course = Course("Python Basics", 1499)
course.pirce = 999
print(course.price)
print(vars(course))
```

```bash
python dc_typo.py
```

```
1499
{'title': 'Python Basics', 'price': 1499, 'pirce': 999}
```

No error at all, the price is still 1499, and `vars` shows a third entry `pirce` beside the two real ones. An object keeps its attributes in a hidden dictionary, which accepts any name. The fix is one word in the decorator: `slots=True`. Python builds each object with exactly the places named in the class and no hidden dictionary. Same typo, again with `try` to print the message. Guess both:

```python
from dataclasses import dataclass


@dataclass(slots=True)
class Course:
    title: str
    price: int


course = Course("Python Basics", 1499)
try:
    course.pirce = 999
except AttributeError as error:
    print("error:", error)
try:
    print(vars(course))
except TypeError as error:
    print("error:", error)
```

```bash
python dc_slots.py
```

```
error: 'Course' object has no attribute 'pirce' and no __dict__ for setting new attributes
error: vars() argument must have __dict__ attribute
```

The typo is now an error (`no attribute 'pirce'`), and `vars` fails too, because there is no dictionary any more. That is the price of slots, and usually a fair one.

The second gift is memory: a hidden dictionary for every object costs space. Here we build 100,000 courses of each kind and ask `tracemalloc` (Python's memory counter) how much memory they use:

```python
import tracemalloc
from dataclasses import dataclass


@dataclass
class Plain:
    title: str
    price: int


@dataclass(slots=True)
class Slim:
    title: str
    price: int


def megabytes(kind):
    tracemalloc.start()
    items = [kind("Python", 1499) for _ in range(100000)]
    used = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()
    return used / 1_000_000


print(f"plain: {megabytes(Plain):.1f} MB")
print(f"slots: {megabytes(Slim):.1f} MB")
```

```bash
python slots_memory.py
```

```
plain: 9.6 MB
slots: 5.6 MB
```

In the video: plain 9.6 MB, slots 5.6 MB, about 40 percent less for the same data. Your numbers will differ a little, but slots is always smaller. For a handful of objects nobody cares; for hundreds of thousands (rows loaded from a file) it matters. You can combine it with `frozen=True` from module 8 so objects are locked as well.

### 5. Which one to use?

Four tools, four questions.

- Does the data arrive as a dictionary (from JSON) and stay one? `TypedDict`.
- Is it a small fixed record that you never edit? `NamedTuple`.
- Is it an object that changes or has methods? A dataclass.
- Are there very many of them, or is a typo a risk? Add `slots=True`.

Test yourself: (1) the reply from a web service, loaded as a dictionary; (2) the latitude and longitude of a city; (3) a million student objects in memory, which Asha edits. Pause and decide.

Answers: (1) a `TypedDict`, because it is a dictionary and stays one. (2) a `NamedTuple`, a fixed record with two named parts. (3) a dataclass with `slots=True`, because they change and there are very many.

### 6. `match`: sequence patterns

Second half of the lesson. A sorting machine at the post office does not read every word: it looks at the *shape* of each parcel. In module 3, `match` compared a value with simple patterns. A pattern can also describe a shape. Start with commands typed as lists of words. The pattern is written like the list itself. A plain name inside the pattern is a label: if the shape fits, Python sticks the label on the matching piece. `*courses` (the star from module 5) takes everything left over into a list. Guess four lines: `quit`, `enrol Lukas`, `enrol Priya` with two courses, and `enrol` alone.

```python
def run(command):
    match command:
        case ["quit"]:
            return "bye"
        case ["enrol", name]:
            return f"enrolling {name}"
        case ["enrol", name, *courses]:
            return f"{name} takes {len(courses)} courses"
        case _:
            return "unknown command"


print(run(["quit"]))
print(run(["enrol", "Lukas"]))
print(run(["enrol", "Priya", "C101", "C102"]))
print(run(["enrol"]))
```

```bash
python m_seq.py
```

```
bye
enrolling Lukas
Priya takes 2 courses
unknown command
```

`enrol` alone is an unknown command, because every `enrol` pattern needs at least a name.

**An important trap.** What does a bare name in a pattern do? It *captures*; it never compares. Asha has a constant `FREE` in capital letters and writes `case FREE:` hoping to compare the plan with it.

```python
FREE = "free"


def label(plan):
    match plan:
        case FREE:
            return "no payment"
        case _:
            return "paid plan"


print(label("pro"))
```

```bash
python m_trap.py
```

```
  File "m_trap.py", line 6
    case FREE:
         ^^^^
SyntaxError: name capture 'FREE' makes remaining patterns unreachable
```

`SyntaxError: name capture 'FREE' makes remaining patterns unreachable`. A bare name accepts anything and sticks the label on it, so the case below can never run, and Python noticed. To compare you have two choices: write the value itself (like the text `"free"` in quotes), or use a name with a dot in it, such as an enum member from module 8. A dotted name is looked up and compared. Guess three lines:

```python
from enum import Enum


class Plan(Enum):
    FREE = "free"
    PRO = "pro"


def label(plan):
    match plan:
        case Plan.FREE:
            return "no payment"
        case Plan.PRO:
            return "paid plan"
        case _:
            return "unknown"


print(label(Plan.PRO))
print(label(Plan.FREE))
print(label("pro"))
```

```bash
python m_enum.py
```

```
paid plan
no payment
unknown
```

The plain text `"pro"` matches neither member: a member is not its value (module 8).

### 7. `match`: mapping and class patterns, guards

Data from JSON arrives as dictionaries, so patterns can look like dictionaries too: a key, a colon and a pattern for the value. Two rules: every key in the pattern must be present, and extra keys are ignored. Four events come in: the first has a `course` key no pattern mentions; the second is a payment with an amount; the third is a payment with no amount; the fourth is a refund that carries an amount.

```python
def handle(event):
    match event:
        case {"type": "enrolled", "student": name}:
            return f"{name} enrolled"
        case {"type": "paid", "amount": amount}:
            return f"paid {amount} rupees"
        case {"type": "refund"}:
            return "refund started"
        case _:
            return "unknown event"


events = [
    {"type": "enrolled", "student": "Lukas", "course": "C101"},
    {"type": "paid", "amount": 1499},
    {"type": "paid"},
    {"type": "refund", "amount": 499},
]
for event in events:
    print(handle(event))
```

```bash
python m_map.py
```

```
Lukas enrolled
paid 1499 rupees
unknown event
refund started
```

The extra `course` key was ignored. The payment without an amount fits no case and falls to `unknown event`. A refund's extra `amount` is ignored.

Objects can be matched too. A class pattern looks like a call: the class name with brackets. Python checks that the object is of that class, then picks out attributes. Guess three lines: an `Enrolled` for Lukas, a `Paid` for Priya, and the plain text `"Priya"`.

```python
from dataclasses import dataclass


@dataclass
class Enrolled:
    student: str
    course: str


@dataclass
class Paid:
    student: str
    amount: int


def handle(event):
    match event:
        case Enrolled(student=who):
            return f"{who} joined"
        case Paid(who, amount):
            return f"{who} paid {amount}"
        case _:
            return "unknown"


print(handle(Enrolled("Lukas", "C101")))
print(handle(Paid("Priya", 1499)))
print(handle("Priya"))
```

```bash
python m_class.py
```

```
Lukas joined
Priya paid 1499
unknown
```

One warning: the brackets matter. A bare class name without brackets would be a capture and cause the same `SyntaxError` as before.

Sometimes the shape is not enough. Add a **guard**: the word `if` and a condition after the pattern. The case matches only when the shape fits *and* the condition is true. Guess three lines: pay 9999, pay 1499 and pay -5.

```python
def pay(command):
    match command:
        case ["pay", amount] if amount >= 5000:
            return "needs approval"
        case ["pay", amount] if amount > 0:
            return f"paid {amount}"
        case ["pay", _]:
            return "invalid amount"
        case _:
            return "unknown command"


print(pay(["pay", 9999]))
print(pay(["pay", 1499]))
print(pay(["pay", -5]))
```

```bash
python m_guard.py
```

```
needs approval
paid 1499
invalid amount
```

`-5` fits the shape but fails both guards, so the third case catches it. Cases are tried from top to bottom, so put the most specific ones first.

Two more tools. A bar `|` joins patterns (as in module 3), and `as` with a label keeps the one that matched:

```python
def starter(code):
    match code:
        case "C101" | "C102" as chosen:
            return f"starter course {chosen}"
        case _:
            return "other course"


print(starter("C102"))
print(starter("C300"))
```

```bash
python m_or.py
```

```
starter course C102
other course
```

Patterns nest, just like JSON does. A student can be a whole dictionary with a name inside it; the pattern simply reaches in:

```python
events = [
    {"type": "enrolled", "student": {"name": "Lukas"}},
    {"type": "enrolled", "student": "Asha"},
    {"type": "paid", "student": {"name": "Priya"}},
]
for event in events:
    match event:
        case {"type": "enrolled", "student": {"name": who}}:
            print("enrolled:", who)
        case {"type": "paid", "student": {"name": who}}:
            print("paid:", who)
        case _:
            print("skipped:", event)
```

```bash
python m_nested.py
```

```
enrolled: Lukas
skipped: {'type': 'enrolled', 'student': 'Asha'}
paid: Priya
```

`Asha`'s event is skipped because `student` is text, not a dictionary, so the shape does not fit.

### 8. Using all of it together

A list of today's events, each one a `TypedDict`. The summary is a `NamedTuple` with `income` and `refunds`. And `match` decides what each event means: a paid event with a positive amount adds to income (a guard), a refund adds to refunds, and the login event matches nothing and is skipped. Run Python, then the checker:

```python
from typing import NamedTuple, NotRequired, TypedDict


class Event(TypedDict):
    type: str
    amount: NotRequired[int]


class Report(NamedTuple):
    income: int
    refunds: int


def summarise(events: list[Event]) -> Report:
    income = refunds = 0
    for event in events:
        match event:
            case {"type": "paid", "amount": rs} if rs > 0:
                income += rs
            case {"type": "refund", "amount": rs}:
                refunds += rs
    return Report(income, refunds)


events: list[Event] = [
    {"type": "paid", "amount": 1499},
    {"type": "login"},
    {"type": "paid", "amount": 999},
    {"type": "refund", "amount": 499},
]
report = summarise(events)
print(report)
income, refunds = report
print(income - refunds)
```

```bash
uv run pyright together.py
```

```
0 errors, 0 warnings, 0 informations
```

```bash
python together.py
```

```
Report(income=2498, refunds=499)
1999
```

Income 2498, refunds 499, and unpacked the net is 1999. The checker says zero errors: the `TypedDict`, the `NamedTuple` and the `match` all agree with each other.

### 9. Four mistakes

**1. A `TypedDict` is a promise, not a guard.** The price arrives as the text `"free"` from JSON, and we tell the checker it is a `CourseData`. First the checker, then Python:

```python
import json
from typing import TypedDict


class CourseData(TypedDict):
    title: str
    price: int


text = '{"title": "Python Basics", "price": "free"}'
course: CourseData = json.loads(text)
print(course["price"] + 100)
```

```bash
uv run pyright json_trust.py
```

```
0 errors, 0 warnings, 0 informations
```

```bash
python json_trust.py
```

```
Traceback (most recent call last):
  File "json_trust.py", line 12, in <module>
    print(course["price"] + 100)
          ~~~~~~~~~~~~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
```

The checker says zero errors and Python crashes (`can only concatenate str`). The function that loads JSON can return anything, so the checker trusts you. A `TypedDict` never looks at the real data. To check data from outside, write real checks (or use a validation library, later in the course).

**2. `isinstance` with a `TypedDict`.** Is the data a dict? Fine. Is it a `CourseData`?

```python
from typing import TypedDict


class CourseData(TypedDict):
    title: str
    price: int


data = {"title": "SQL", "price": 999}
print(isinstance(data, dict))
print(isinstance(data, CourseData))
```

```bash
uv run pyright isinstance_td.py
```

```
isinstance_td.py
  isinstance_td.py:11:24 - error: Second argument to "isinstance" must be a class or tuple of classes
    TypedDict class not allowed for instance or class checks (reportArgumentType)
1 error, 0 warnings, 0 informations
```

```bash
python isinstance_td.py
```

```
True
Traceback (most recent call last):
  File "isinstance_td.py", line 11, in <module>
    print(isinstance(data, CourseData))
          ~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/typing.py", line 3279, in __subclasscheck__
    raise TypeError('TypedDict does not support instance and class checks')
TypeError: TypedDict does not support instance and class checks
```

`True`, then a `TypeError`: `TypedDict` does not support instance and class checks. A `TypedDict` exists only for the checker; at run time it is just a dict, so there is nothing to test. To check the keys, test them yourself.

**3. Order.** Asha writes the broad case first, then the case for `quit`. What does `run(["quit"])` print?

```python
def run(command):
    match command:
        case [first, *rest]:
            return f"first word is {first}"
        case ["quit"]:
            return "bye"


print(run(["quit"]))
```

```bash
python p_order.py
```

```
first word is quit
```

`first word is quit`. The `quit` case is never reached and Python gave no warning, because a pattern with a star is perfectly valid. The first case that fits wins, so put the specific cases first and the broad ones last.

**4. Text is not a sequence for `match`.** The pattern is two items. We try a list, a tuple and the text `"ab"`:

```python
for value in (["a", "b"], ("a", "b"), "ab"):
    match value:
        case [first, second]:
            print("two items:", first, second)
        case _:
            print("no match:", value)
```

```bash
python p_string.py
```

```
two items: a b
two items: a b
no match: ab
```

The list and the tuple match; the text does not, even though it has two letters. `match` treats text as one value, not a row of letters, so a sequence pattern never matches a string by accident.

## Common mistakes

1. Believing a `TypedDict` checks data at run time. It is a promise for the checker only.

2. Using `isinstance(data, CourseData)`: it raises `TypeError`.

3. Writing `case FREE:` for a constant: a bare name captures (and gives a `SyntaxError` when other cases follow). Use the value, or a dotted name such as `Plan.FREE`.

4. Writing a class pattern without brackets (`case Enrolled:`): it is a capture too.

5. Putting a broad `case [first, *rest]` before a specific one: the specific one is never reached.

6. Expecting `match` to treat `"ab"` as two letters. Text is one value.

## Clean up

Nothing to clean up on your computer except the `shapes` project folder you made for pyright. Delete it when you are done.

## Next

Next lesson: [M10-L04 · What's New in Modern Python](../m10-l04-whats-new-in-modern-python/README.md). A handful of new features, from the walrus to template strings, each one run for real.

Your turn first: write a `TypedDict` for a lesson with a title and minutes and a function that takes it; make a `NamedTuple` for a point; and write a `match` that handles three commands: `start`, `stop` and `pause`.
