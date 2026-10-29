# M08-L01 · Classes and Objects

> Video: Module 8, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- Why a dictionary cannot guarantee that every course has the right parts, and how a class fixes that
- What a class (a blueprint) and an object (one thing built from it, also called an instance) are
- How `__init__` and `self` set up every new object, step by step
- That every object keeps its own attributes, and that two names on one object share them
- How to look inside an object with `type()` and `vars()`, and what a typo does on read and on write

## Before you start

- Python 3.14 or newer. Check with `python --version` (use `python3` if `python` is not found on your machine).
- Open a terminal in this folder (`m08-object-oriented-programming/m08-l01-classes-and-objects`).
- You need the ideas from Module 2 (names and objects, `type()`), Module 4 (functions) and Module 6 (errors). No earlier lesson folder is needed to run the files.
- The running example is the course catalogue of allcsvideos.com. Every price is a whole number of rupees.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The opening problem: two courses as dictionaries, one with a wrong key (`name` instead of `title`) |
| `type_of.py` | `type()` of `5`, `"Lukas"` and a list: Python's own classes (the video calls this file the "types" demo) |
| `empty.py` | The smallest class, `class Course: pass`, and one object built from it |
| `byhand.py` | Attributes added by hand after the object exists, and one missing attribute |
| `init0.py` | `Course` with `__init__` and one object, nothing printed (used in the slow-motion explanation) |
| `init1.py` | The same class, printing `title` and `price` |
| `missing.py` | Building a `Course` without a price |
| `many.py` | Three courses from one class, one price changed |
| `alias.py` | Two names on one object |
| `inside.py` | `type()`, `is` and `vars()` on an object |
| `calls.py` | `int("499")`, `str(499)`, `list("abc")`: calls to Python's own classes |
| `typo.py` | Reading a misspelled attribute (`pricee`) |
| `typo2.py` | Writing a misspelled attribute |
| `noself.py` | Pitfall 1: `title = title` without `self.` |
| `noselfarg.py` | Pitfall 2: `self` missing in the brackets |
| `students.py` | A second class, `Student`, with Lukas and Priya |
| `catalog.py` | A list of `Course` objects and a total |
| `tryit.py` | The "try it yourself" solution (`Lesson` class) |

Every file runs on its own, with `python <file>`.

## Follow along

### 1. The problem: a dictionary with a typo

Asha stores courses as dictionaries. A teammate typed `name` instead of `title` in the second one.

```python
course_a = {"title": "Python", "price": 499}
course_b = {"name": "SQL", "price": 399}

for course in [course_a, course_b]:
    print(course["title"], course["price"])
```

Run it:

```bash
python hook.py
```

You should see (the path in the traceback line will be longer on your machine):

```text
Python 499
Traceback (most recent call last):
  File "hook.py", line 5, in <module>
    print(course["title"], course["price"])
          ~~~~~~^^^^^^^^^
KeyError: 'title'
```

Nothing checked, when the dictionary was made, that a course has the right parts. A class will.

### 2. A class is a blueprint, an object is a house

A blueprint says what parts a house has (a door, windows, a colour). A builder uses it to build real houses. One blueprint, many houses, and painting one house does not repaint the others.

In Python the blueprint is a class and each house is an object, also called an instance. You have used classes already:

```bash
python type_of.py
```

```text
<class 'int'>
<class 'str'>
<class 'list'>
```

`int`, `str` and `list` are blueprints Python built for you. The number `5` is one object made from `int`.

### 3. Your first class

Write the word `class`, the name, a colon, and `pass` (the do-nothing word) inside:

```python
class Course:
    pass


python_course = Course()
print(type(python_course))
print(python_course)
```

```bash
python empty.py
```

```text
<class '__main__.Course'>
<__main__.Course object at 0x109b29fd0>
```

Class names start with a capital letter and each new word is capitalised (`Course`, `Student`, `PaymentError`). Variables stay lowercase. `__main__` is the name Python gives to the file you ran. The long code after `at` is the place in memory where the object lives: **yours will differ**.

### 4. Attributes added by hand

A label that belongs to an object is called an attribute. Write the object, a dot, the name, `=`, the value:

```python
class Course:
    pass


python_course = Course()
python_course.title = "Python"
python_course.price = 499
print(python_course.title, python_course.price)

sql_course = Course()
sql_course.title = "SQL"
print(sql_course.price)
```

```bash
python byhand.py
```

```text
Python 499
Traceback (most recent call last):
  File "byhand.py", line 12, in <module>
    print(sql_course.price)
          ^^^^^^^^^^^^^^^^
AttributeError: 'Course' object has no attribute 'price'
```

It works, but it is fragile: nothing guarantees every course gets a title and a price.

### 5. `__init__` and `self`

If a class has a function named exactly `__init__` ("dunder init": dunder means double underscore, init means set up), Python runs it automatically for every new object.

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


python_course = Course("Python", 499)
print(python_course.title)
print(python_course.price)
```

```bash
python init1.py
```

```text
Python
499
```

We gave two values but wrote three names. Python adds `self` itself: it is the new object being built ("this house"). In slow motion (`init0.py` has just the class and the one call):

1. `Course("Python", 499)` makes a new, empty `Course` object.
2. Python calls `__init__`: `self` is the new object, `title` is `"Python"`, `price` is `499`.
3. `self.title = title` sticks an attribute called `title` on the object, and `self.price = price` does the same.
4. `__init__` ends and Python hands back the finished object. The name `python_course` is stuck on it.

`title` (no `self`) is a parameter: it lives only while `__init__` runs. `self.title` is an attribute: it stays on the object.

### 6. A course without a price is refused

```python
sql_course = Course("SQL")
```

```bash
python missing.py
```

```text
Traceback (most recent call last):
  File "missing.py", line 7, in <module>
    sql_course = Course("SQL")
TypeError: Course.__init__() missing 1 required positional argument: 'price'
```

Same message as for functions, because `__init__` is a function. The blueprint now guarantees: no `Course` exists without a title and a price.

### 7. One blueprint, many objects

```python
python_course = Course("Python", 499)
sql_course = Course("SQL", 399)
docker_course = Course("Docker", 449)

sql_course.price = 349
print(python_course.price)
print(sql_course.price)
print(docker_course.price)
```

```bash
python many.py
```

```text
499
349
449
```

Only the SQL course changed. The class says which parts exist; the values belong to each object.

Names are labels and `=` never makes a copy. This is true for objects too:

```python
sql_course = Course("SQL", 399)
same_course = sql_course
same_course.price = 349
print(sql_course.price)
print(same_course is sql_course)
```

```bash
python alias.py
```

```text
349
True
```

One object, two labels. If you want a second, separate course, build it with `Course(...)` again.

### 8. Look inside an object

```python
python_course = Course("Python", 499)
print(type(python_course))
print(type(python_course) is Course)
print(vars(python_course))
```

```bash
python inside.py
```

```text
<class '__main__.Course'>
True
{'title': 'Python', 'price': 499}
```

`vars()` shows an object's attributes as a dictionary. The difference from a plain dictionary: now the blueprint decides which keys every object gets.

Python's own types work the same way. These are calls to the classes `int`, `str` and `list`:

```bash
python calls.py
```

```text
499
499
['a', 'b', 'c']
```

### 9. Typos: reading fails, writing does not

```python
print(python_course.pricee)
```

```bash
python typo.py
```

```text
Traceback (most recent call last):
  File "typo.py", line 8, in <module>
    print(python_course.pricee)
          ^^^^^^^^^^^^^^^^^^^^
AttributeError: 'Course' object has no attribute 'pricee'. Did you mean: 'price'?
```

Reading a wrong name fails, and Python even suggests the fix. But writing a wrong name does not fail:

```python
python_course.pricee = 399
print(python_course.price)
```

```bash
python typo2.py
```

```text
499
```

Python quietly stuck a new attribute called `pricee` on the object; the real price never changed. A class helps but does not stop every typo. Lesson 3 (properties) and lesson 6 (frozen data classes) give stricter tools.

### 10. Pitfall: forgetting `self.` inside `__init__`

```python
class Course:
    def __init__(self, title, price):
        title = title
        self.price = price
```

```bash
python noself.py
```

```text
499
Traceback (most recent call last):
  File "noself.py", line 9, in <module>
    print(python_course.title)
          ^^^^^^^^^^^^^^^^^^^
AttributeError: 'Course' object has no attribute 'title'
```

Plain `title` was only a parameter and vanished when `__init__` ended.

### 11. Pitfall: forgetting `self` in the brackets

```python
class Course:
    def __init__(title, price):
        title.price = price


python_course = Course("Python", 499)
```

```bash
python noselfarg.py
```

```text
Traceback (most recent call last):
  File "noselfarg.py", line 6, in <module>
    python_course = Course("Python", 499)
TypeError: Course.__init__() takes 2 positional arguments but 3 were given
```

You gave two values, Python added the object, that makes three. `self` is always the first name.

### 12. Another class, and a list of objects

```bash
python students.py
```

```text
Lukas lives in Frankfurt
Priya lives in Delhi
```

Objects can live in a list like any other value:

```bash
python catalog.py
```

```text
Python 499
SQL 399
Docker 449
Total: 1347
```

Compared with a list of dictionaries, every item is now guaranteed to have a title and a price.

### 13. Try it yourself

Write a class `Lesson` with `title` and `minutes`, build "Variables" (12 minutes) and "Loops" (18 minutes), and print the total minutes. The solution is `tryit.py`:

```bash
python tryit.py
```

```text
30
```

## Common mistakes

- Forgetting `self.` in `__init__` (`title = title`): the value is lost when `__init__` ends.
- Forgetting `self` in the brackets: "takes 2 positional arguments but 3 were given".
- Thinking `b = a` copies an object: it only adds a second label to the same object.
- Believing a class stops all typos: reading a wrong name fails, writing a wrong name silently creates a new attribute.
- Vague object names like `course1` or `x`. Use `python_course`, `sql_course`: the code then reads like a sentence.

## Clean up

Nothing to clean up. If Python created a `__pycache__` folder, you can delete it.

## Next

[M08-L02 · Attributes and Methods](../m08-l02-attributes-and-methods/README.md)
