# M08-L03 · Encapsulation and Properties

> Video: Module 8, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- What encapsulation means, and why Python builds it on trust, not locks
- What a single underscore (`_price`) says, and what a double underscore (`__code`) really does (name mangling)
- Getters and setters, and why Python has something shorter: the property
- How `@property` and `@price.setter` check every new value, even in `__init__`
- Why you start with a plain attribute and upgrade later, and three pitfalls

## Before you start

- Python 3.14 or newer. Check with `python --version` (use `python3` if `python` is not found on your machine).
- Open a terminal in this folder (`m08-object-oriented-programming/m08-l03-encapsulation-and-properties`).
- You need [M08-L02 · Attributes and Methods](../m08-l02-attributes-and-methods/README.md) (decorators like `@classmethod`) and the errors lesson (`raise ValueError`).

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The opening problem: a negative price is accepted |
| `under.py` | The single underscore: a sign, not a lock |
| `mangle.py` | The double underscore: `course.__code` fails |
| `mangle2.py` | `vars()` shows the renamed attribute |
| `getset.py` | Java-style `get_price` and `set_price` |
| `prop_read.py` | A read-only property |
| `prop_calc.py` | A property that is worked out each time (`is_free`) |
| `setter1.py` | A property with a setter that checks the value |
| `setter2.py` | A bad price in `__init__` is rejected too |
| `up1.py` | Version 1: plain attribute and the helper `apply_sale` |
| `up2.py` | Version 2: the same helper, the attribute is now a property |
| `recur.py` | Pitfall: the setter that calls itself |
| `brackets.py` | Pitfall: brackets on a property |
| `bypass.py` | Pitfall: going around the counter with `_price` |
| `tryit.py` | The "try it yourself" solution (`Lesson` with a checked `minutes`) |

Every file runs on its own, with `python <file>`. The tracebacks below show short file names; yours show the full path.

## Follow along

### 1. The problem: a negative price

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


course = Course("Python", 499)
course.price = -500
print("Two seats:", course.price * 2)
```

```bash
python hook.py
```

```text
Two seats: -1000
```

No error. The shop would pay Lukas a thousand rupees for two seats. The class has no way to say "this value is not allowed".

### 2. Encapsulation: the shop counter

Customers talk to the counter; they never walk into the back room. The person at the counter checks everything, so the back room stays tidy. Encapsulation means an object keeps its data in the back room and offers a counter to everybody else, with the data and its rules in one place.

Java has `private`. Python has no real lock, only a promise between humans. Python gives you two tools: a naming habit, and the property.

### 3. One underscore: staff only

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self._price = price


course = Course("Python", 499)
print(course._price)
course._price = 399
print(course._price)
```

```bash
python under.py
```

```text
499
399
```

No error. The underscore changes nothing for Python; it tells other programmers "inside detail, may change". Use it freely inside the class and treat it as staff only from outside.

### 4. Two underscores: a disguise, not a lock

```python
class Course:
    def __init__(self, title, code):
        self.title = title
        self.__code = code


course = Course("Python", "PY-2026")
print(course.title)
print(course.__code)
```

```bash
python mangle.py
```

```text
Python
Traceback (most recent call last):
  File "mangle.py", line 9, in <module>
    print(course.__code)
          ^^^^^^^^^^^^^
AttributeError: 'Course' object has no attribute '__code'
```

It looks like a lock. Look closer with `vars()`:

```bash
python mangle2.py
```

```text
{'title': 'Python', '_Course__code': 'PY-2026'}
PY-2026
```

Python renamed the attribute by putting the class name in front (name mangling), so `course._Course__code` works. It exists so a class can keep a name to itself when a class built on top of it uses the same word (next lesson). In everyday code a single underscore is enough.

### 5. Getters and setters (the Java way)

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self._price = price

    def get_price(self):
        return self._price

    def set_price(self, value):
        if value < 0:
            raise ValueError("price cannot be negative")
        self._price = value


course = Course("Python", 499)
course.set_price(course.get_price() + 100)
print(course.get_price())
course.set_price(-500)
```

```bash
python getset.py
```

```text
599
Traceback (most recent call last):
  File "getset.py", line 18, in <module>
    course.set_price(-500)
    ~~~~~~~~~~~~~~~~^^^^^^^
  File "getset.py", line 11, in set_price
    raise ValueError("price cannot be negative")
ValueError: price cannot be negative
```

The check works, but `course.set_price(course.get_price() + 100)` is noisy. With a plain attribute it would be `course.price += 100`. A property gives both.

### 6. A read-only property

A property looks like an attribute from outside but runs a small method behind the scenes. Put the decorator `@property` above the method:

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self._price = price

    @property
    def price(self):
        return self._price


course = Course("Python", 499)
print(course.price)
course.price = 399
```

```bash
python prop_read.py
```

```text
499
Traceback (most recent call last):
  File "prop_read.py", line 13, in <module>
    course.price = 399
    ^^^^^^^^^^^^
AttributeError: property 'price' of 'Course' object has no setter
```

Reading works with no brackets. With only `@property`, the value is read only.

### 7. A property that is worked out every time

```python
    @property
    def is_free(self):
        return self._price == 0


paid = Course("Python", 499)
free = Course("Intro to Python", 0)
print(paid.is_free)
print(free.is_free)
```

```bash
python prop_calc.py
```

```text
False
True
```

Nothing stores the answer: it is computed fresh each time, so it can never be out of date.

### 8. A setter that checks every new value

Add a second method with the same name and the decorator `@price.setter`:

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError(f"price cannot be negative, got {value}")
        self._price = value


course = Course("Python", 499)
course.price = 599
print(course.price)
course.price = -500
```

```bash
python setter1.py
```

```text
599
Traceback (most recent call last):
  File "setter1.py", line 20, in <module>
    course.price = -500
    ^^^^^^^^^^^^
  File "setter1.py", line 13, in price
    raise ValueError(f"price cannot be negative, got {value}")
ValueError: price cannot be negative, got -500
```

The caller wrote an ordinary assignment, and the check ran by itself. Note `self.price = price` (no underscore) in `__init__`: it goes through the setter, so a brand new course is checked too:

```python
try:
    course = Course("Python", -500)
except ValueError as error:
    print("Rejected:", error)
```

```bash
python setter2.py
```

```text
Rejected: price cannot be negative, got -500
```

(`setter2.py` has the full class above this `try` block.) A course with a negative price can never be created: this fixes the opening problem.

### 9. Start plain, upgrade later

Version 1 uses a plain `price` attribute, and a helper somewhere in the shop's code:

```python
def apply_sale(course):
    course.price = course.price - 100
```

```bash
python up1.py
```

```text
399
```

Next month the rule "no negative prices" arrives. With Java-style methods every caller would have to change. In Python only the class changes: `price` becomes a property with a setter. The helper stays exactly the same:

```bash
python up2.py
```

```text
399
Traceback (most recent call last):
  File "up2.py", line 25, in <module>
    apply_sale(quiz)
    ~~~~~~~~~~^^^^^^
  File "up2.py", line 18, in apply_sale
    course.price = course.price - 100
    ^^^^^^^^^^^^
  File "up2.py", line 13, in price
    raise ValueError(f"price cannot be negative, got {value}")
ValueError: price cannot be negative, got -50
```

The normal course still gives 399, and a quiz pack costing 50 is rejected at the exact line that caused it. So do not write getters and setters from the start; upgrade a plain attribute to a property only when you need a rule.

### 10. Pitfalls

**The setter that calls itself.** Inside the setter, `self.price = value` calls the setter again:

```bash
python recur.py
```

```text
Traceback (most recent call last):
  File "recur.py", line 15, in <module>
    course = Course("Python", 499)
  File "recur.py", line 4, in __init__
    self.price = price
    ^^^^^^^^^^
  File "recur.py", line 12, in price
    self.price = value
    ^^^^^^^^^^
  ...
RecursionError: maximum recursion depth exceeded
```

(The real output repeats the `self.price = value` lines about a thousand times; the middle is cut here.) Fix: inside the setter store into `self._price`.

**Brackets on a property.**

```bash
python brackets.py
```

```text
Traceback (most recent call last):
  File "brackets.py", line 12, in <module>
    print(course.price())
          ~~~~~~~~~~~~^^
TypeError: 'int' object is not callable
```

`course.price` is already the number; brackets would call it.

**Going around the counter.**

```bash
python bypass.py
```

```text
-500
```

`course._price = -500` skips the setter and the check. It is a promise: inside the class use the underscore name, outside use the property.

### 11. Try it yourself

Take the `Lesson` class from lesson 1 and make `minutes` a property that rejects anything below 1 with a `ValueError`. Add a read-only property `is_long` that is `True` when minutes is above 60. Test with 45, 90 and 0. Solution is `tryit.py`:

```bash
python tryit.py
```

```text
False
True
Traceback (most recent call last):
  File "tryit.py", line 25, in <module>
    lesson.minutes = 0
    ^^^^^^^^^^^^^^
  File "tryit.py", line 13, in minutes
    raise ValueError(f"minutes must be at least 1, got {value}")
ValueError: minutes must be at least 1, got 0
```

## Common mistakes

- Writing `self.price = value` inside the price setter: infinite recursion. Store in `self._price`.
- Calling a property with brackets: `course.price()`.
- Assigning to `course._price` from outside, which skips the check.
- Believing `__code` is truly private: it is only renamed to `_Course__code`.
- Writing get and set methods up front: start with a plain attribute and upgrade when a rule is needed.

## Clean up

Nothing to clean up. If Python created a `__pycache__` folder, you can delete it.

## Next

[M08-L04 · Inheritance and Composition](../m08-l04-inheritance-and-composition/README.md)
