# M08-B04 · Build the allcsvideos Domain Model

> Video: Module 8, Build 4. Watch it first, then follow along here.

Asha's first allcsvideos.com shop kept everything in plain dictionaries and lists, and Priya was charged twice. In this
build you create a real, tested model of the shop: courses, lessons, students and enrollments, where every rule lives
inside the class that owns the data.

## What you'll learn

- How to plan a domain model on paper: the real things, how they connect (has-a, so composition), and the rules
- Picking the right tool for each piece: an `Enum`, frozen data classes, a class with a property, your own error family
- Keeping every rule inside the class that owns the data, so every entrance goes through the same door
- Making a class feel built in with `__len__`, `__iter__`, `__str__` and `__repr__`
- Writing a small test script, and breaking a rule on purpose to watch a test fail
- Saving and loading with `to_dict`, a `from_dict` class method and JSON

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No packages to install: everything uses the standard library.
- You should have finished Module 8 (lessons 1 to 6) and Module 6 (JSON). No other folder is needed.
- Run every command from the folder named in the step. `domain.py` and `storage.py` must sit in the same folder as the
  script that imports them.

## Files in this folder

| File | What it is |
|------|------------|
| `domain.py` | The finished model: `Level`, the errors, `Lesson`, `Student`, `Course`, `Enrollment` (148 lines) |
| `storage.py` | `save_courses` and `load_courses`, JSON on disk (16 lines) |
| `demo.py` | The demo from the video: two courses, enrollments, refusals, save and load |
| `test_domain.py` | The test script: 14 checks (12 rules plus 2 save and load checks) |
| `before.py` | The old dictionary-and-list code that caused the double charge |
| `broken.py` | Feeds a hand-edited, damaged course to `from_dict` |
| `around.py` | Walks around the counter with `course._price` |
| `twin.py` | Same email, different spelling of the name |
| `mutant/` | `domain.py` with the double-enrol check switched off, plus its 12-check test script |
| `steps/step1/` to `steps/step6/` | The model as it is at the end of each step in the video, with the small `try` scripts |

Files `courses.json` and `test_courses.json` are created when you run `demo.py` and `test_domain.py`. They are not
in the repo.

## Follow along

### 1. Plan on paper first

No code yet. A domain model is the real things your business talks about, written as classes:

- A **course** is what we sell.
- A **lesson** is one video inside a course.
- A **student** is a person who learns.
- An **enrollment** is the link: this student joined that course, and finished these lessons.

A course has lessons. An enrollment has a student and has a course. None of them is a kind of another one, so there is
no inheritance, only objects that hold other objects (composition).

The rules the model must keep:

1. A price is whole rupees, never below zero.
2. A lesson lasts at least one minute, and a student's email contains an `@`.
3. A student can enrol in a course only once.
4. Only the lessons of a course can be completed, and progress is a percentage.
5. Courses can be saved to JSON and loaded back.
6. Every rule lives inside the class that owns the data.

The tool for each piece: an enum for the level, one parent error with children, frozen data classes for `Lesson` and
`Student`, a normal class with a property for `Course`, and a data class for `Enrollment`.

### 2. See the problem: the old code

```bash
python before.py
```

```text
{'title': 'Python Basics', 'price': -500, 'prise': 599}
['priya@example.com', 'priya@example.com']
```

No error at all. The price is minus 500, there is a new key `prise` next to the real `price`, and Priya is in the list
twice. A dictionary and a list have no rules.

### 3. See the finished model

```bash
python demo.py
```

```text
Python Basics (Rs 499, beginner)
3 lessons, 45 min
Priya: 66 percent
Lukas: 100 percent
Refused: Priya is already in Python Basics
Refused: price cannot be negative, got -499
Saved and loaded 2 courses
Priya is still at 66 percent
```

Now we build it from an empty file, in six steps. The folder `steps/stepN/` holds the code as it is at the end of each
step, so you can type it yourself and compare.

### 4. Step one: the words (enum and errors)

Code: `steps/step1/domain.py` (19 lines).

A value with a small, fixed set of choices is an enum. The values are text, so the JSON file stays easy to read:

```python
class Level(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
```

Why not plain text? A typo like `"begginer"` is just another text. `Level.BEGINER` does not exist, so Python stops you.

The errors: one parent, `DomainError`, and two children, `AlreadyEnrolledError` and `UnknownLessonError`. Callers can
catch one exact problem, or the whole family with `DomainError`.

```bash
cd steps/step1
python try1.py
```

```text
Level.BEGINNER
Level.ADVANCED
['beginner', 'intermediate', 'advanced']
AlreadyEnrolledError - Priya enrolled twice
```

`Level("advanced")` finds a member by its value. The error is caught by `except DomainError` because a child is a
parent.

### 5. Step two: the lesson and the student

Code: `steps/step2/domain.py` (40 lines).

Both are small bundles of facts that never change after they are made, so they are frozen data classes
(`@dataclass(frozen=True)`). Frozen objects cannot be changed by accident and can go into a set. The rule goes into
`__post_init__`, which Python calls right after the generated `__init__`.

```bash
cd ../step2
python try2.py
```

```text
Lesson(title='Loops', minutes=15)
True
Student(name='Priya', email='priya@example.com')
1
Traceback (most recent call last):
  File "try2.py", line 12, in <module>
    loops.minutes = 20
    ^^^^^^^^^^^^^
  File "<string>", line 17, in __setattr__
dataclasses.FrozenInstanceError: cannot assign to field 'minutes'
```

(The file path in the traceback on your machine will be longer.) Equal facts mean equal objects (`True`), a set holds
the twin once (`1`), and the frozen lesson defends itself. Now the rules:

```bash
python try2b.py
```

```text
refused: minutes must be positive
refused: email needs an @ sign
```

### 6. Step three: the course

Code: `steps/step3/domain.py` (85 lines).

`Course` needs a rule that holds at every moment, not only at birth, so it is a normal class with a property. In
`__init__`, `self.price = price` (no underscore) goes through the setter, so a course can never be born with a bad
price. The real value lives in `_price`. The setter checks it is a whole number and not negative. `add_lesson` makes a
`Lesson`, appends it and returns it. `minutes` is a property that sums the lessons. Four dunder methods follow:
`__len__`, `__iter__`, `__str__` (for people) and `__repr__` (for programmers).

```bash
cd ../step3
python try3.py
```

```text
Python Basics (Rs 499, beginner)
[Course('Python Basics', 499)]
3 lessons, 45 minutes
- Variables
- Loops
- Functions
599
Traceback (most recent call last):
  File "try3.py", line 16, in <module>
    course.price = -500
    ^^^^^^^^^^^^
  File "domain.py", line 61, in price
    raise ValueError(msg)
ValueError: price cannot be negative, got -500
```

(Again, your paths will be longer.) Now three prices, each inside `try`:

```bash
python try3b.py
```

```text
refused: price cannot be negative, got -500
refused: price must be whole rupees, got 499.5
accepted: 0
```

A free course (price 0) is allowed.

### 7. Step four: the enrollment

Code: `steps/step4/domain.py` (117 lines).

The course keeps a dictionary from email to `Enrollment`. Two people can share a name, but an email belongs to one
person, and a dictionary key exists only once, so a second `enrol` is easy to spot and raises `AlreadyEnrolledError`.

`Enrollment` is a data class with the student, the course and `done`, a set of finished lessons. Its default is
`field(default_factory=set)`: one shared empty set would belong to every enrollment (the mutable default trap).
`complete` raises `UnknownLessonError` if the lesson is not in the course (`in` works because `Course` has
`__iter__`). `progress` is `100 * finished // lessons`, and 0 for a course with no lessons. `finished` is true at 100.

```bash
cd ../step4
python try4.py
```

```text
0
33
33
100 True
refused: Priya is already in Python Basics
```

One third is floored to 33, and completing the same lesson twice counts once. Then the two edge cases:

```bash
python try4b.py
```

```text
refused: Databases is not in this course
0
```

### 8. Step five: the tests

Code: `steps/step5/test_domain.py` (61 lines).

`check` prints PASS or FAIL for a condition and remembers it. `raises` runs a lambda inside a `try` block and says
whether the expected error happened. Twelve checks cover every rule.

```bash
cd ../step5
python test_domain.py
```

```text
PASS price 499 is accepted
PASS negative price is refused
PASS price with paise is refused
PASS lesson of 0 minutes is refused
PASS email without @ is refused
PASS course counts its lessons
PASS enrolling twice is refused
PASS progress starts at 0
PASS 1 of 3 is 33 percent
PASS same lesson counts once
PASS lesson of another course is refused
PASS 3 of 3 lessons is finished
12 of 12 checks passed
```

A test that cannot fail proves nothing, so the video breaks the model on purpose: in `enrol`, the check
`if student.email in self.enrollments:` becomes `if False:`. That broken copy is in `mutant/`:

```bash
cd ../../mutant
python test_domain.py
```

The output is the same as above except for these two lines:

```text
FAIL enrolling twice is refused
...
11 of 12 checks passed
```

One test fails and is named. Put the model back and the tests are green again.

### 9. Step six: save and load

Code: `steps/step6/domain.py` (148 lines) and `steps/step6/storage.py` (16 lines).

JSON cannot store a `Course` object, only plain text, numbers, lists and dictionaries. So `to_dict` turns a course into
those. The way back is `from_dict`, a class method (`@classmethod`, first argument `cls`), so you can call
`Course.from_dict(...)` before any course exists. It rebuilds the course through the normal doors: the constructor,
`add_lesson`, `enrol` and `complete`, so every rule runs while loading too. `storage.py` writes and reads the JSON file.

```bash
cd ../steps/step6
python try6.py
```

```text
[
  {
    "title": "Python Basics",
    "price": 499,
    "level": "beginner",
    "lessons": [
      [
        "Variables",
        12
      ],
      [
        "Loops",
        15
      ]
    ],
    "students": [
      {
        "name": "Priya",
        "email": "priya@example.com",
        "done": [
          "Variables"
        ]
      }
    ]
  }
]
Python Basics (Rs 499, beginner)
50
```

This creates `courses.json` in the folder you ran it from. Priya is at 50 percent: one lesson of two.

### 10. The whole program

Go back to the top of this folder. `domain.py` is the same file as `steps/step6/domain.py`. It has eight parts: imports,
enum and errors; `Lesson` and `Student`; the start of `Course` with the price property; `add_lesson`, `enrol` and
`minutes`; `to_dict`; `from_dict`; the dunder methods; and `Enrollment`.

```bash
cd ../..
python demo.py
python test_domain.py
```

`demo.py` prints the output from step 3 of this README. `test_domain.py` prints the 12 lines from step five, then:

```text
PASS save keeps the progress
PASS save keeps the level
14 of 14 checks passed
```

## What can still go wrong

Run each of these from the top of this folder.

**A hand-edited JSON file.** One course has a price of -499, another has the level `expert`:

```bash
python broken.py
```

```text
Refused: price cannot be negative, got -499
Refused: 'expert' is not a valid Level
```

Loading goes through the same doors, so a damaged file cannot sneak in bad data.

**Going around the counter.** The underscore name skips the setter:

```bash
python around.py
```

```text
-500
```

The rules protect against mistakes, not against someone who walks around on purpose. The underscore means staff only.

**The same person, spelled differently.** `Priya R` with Priya's email:

```bash
python twin.py
```

```text
False
Refused: Priya R is already in Python Basics
```

A data class compares every field, so the twin is not equal. But `enrol` looks at the email, so it is refused anyway.

**Rules change.** If a lesson must be at least five minutes, you change one place: the class that owns the data.

## Common mistakes

- Writing `self._price = price` in `__init__`. That skips the setter, so a course can be born with a bad price. Write
  `self.price = price`.
- Using a plain text for the level. A typo is just another text; an enum rejects it.
- A shared mutable default. `done: set = set()` is not allowed in a data class; use `field(default_factory=set)`.
- Putting a check in loose code outside the class. One forgotten check lets a bad value in.
- Dividing by the number of lessons without checking for zero lessons.
- Forgetting that `from_dict` must use `enrol` and `complete`, otherwise loading skips the rules.

## Try it yourself

Five upgrades from the video. Pick one and try it:

1. Add an `Instructor` class and give every course one (composition again).
2. Add a payment error, a child of `DomainError`, and refuse to enrol until a payment is made.
3. Sort enrollments by progress using `__lt__`.
4. Print a certificate when an enrollment is finished.
5. Add a `discount` property to the price, in whole rupees.

## Clean up

```bash
rm -f courses.json test_courses.json steps/step6/courses.json
```

Delete any `__pycache__` folders too. Nothing else was created.

## Next

You have finished Module 8. Try the practice sheet for this module:
[M08 Practice Sheet](../../practice/m08-object-oriented-programming/).
