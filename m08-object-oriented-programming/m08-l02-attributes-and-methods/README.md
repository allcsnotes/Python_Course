# M08-L02 · Attributes and Methods

> Video: Module 8, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- How to write your own methods, and what `self` really is (the object in front of the dot)
- The difference between a method that returns an answer and one that changes the object
- Instance attributes (one object) versus class attributes (shared by all), and why a list in the class is a trap
- Class methods (`@classmethod`, `cls`) as alternative ways to build an object, like `from_dict`
- Static methods (`@staticmethod`) for small helpers that live with the class

## Before you start

- Python 3.14 or newer. Check with `python --version` (use `python3` if `python` is not found on your machine).
- Open a terminal in this folder (`m08-object-oriented-programming/m08-l02-attributes-and-methods`).
- You need [M08-L01 · Classes and Objects](../m08-l01-classes-and-objects/README.md): classes, `__init__`, `self`.
- Prices are whole rupees. For money we use whole numbers and `//`, never floats.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | The mystery: Lukas appears in the SQL course |
| `methods.py` | The `describe` method, called two ways |
| `missing_self.py` | Pitfall: a method without `self` |
| `discount.py` | `price_after` (returns) and `apply_discount` (changes the object) |
| `currency.py` | A class attribute and how reading and writing differ |
| `shared_bad.py` | Proof that the two `students` lists are the same list |
| `shared_fixed.py` | The cure: create the list in `__init__` |
| `cls_demo.py` | A tiny class method that prints `cls` |
| `from_dict.py` | Alternative constructor `from_dict` |
| `from_line.py` | Alternative constructor `from_line` |
| `price_from_text.py` | A static method |
| `no_brackets.py` | Pitfall: calling a method without brackets |
| `no_self.py` | Pitfall: `price` instead of `self.price` inside a method |
| `no_decorator.py` | Pitfall: `cls` without `@classmethod` |
| `tryit.py` | The "try it yourself" solution |

Every file runs on its own, with `python <file>`.

## Follow along

### 1. The mystery of Lukas

Asha makes two courses, adds Lukas to the Python course only, then prints the students of the SQL course.

```python
class Course:
    students = []

    def __init__(self, title, price):
        self.title = title
        self.price = price


python_course = Course("Python", 499)
sql_course = Course("SQL", 399)
python_course.students.append("Lukas")
print(sql_course.students)
```

```bash
python hook.py
```

```text
['Lukas']
```

Lukas is in the SQL course too. This is not a Python bug: the mistake is where the list was put. We will solve it in step 6.

### 2. Methods: what an object can do

An object has attributes (what it knows: `title`, `price`) and methods (what it can do). A method is a function written inside a class, with `self` as its first name.

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def describe(self):
        return f"{self.title} costs Rs {self.price}"


python_course = Course("Python", 499)
print(python_course.describe())
print(Course.describe(python_course))
```

```bash
python methods.py
```

```text
Python costs Rs 499
Python costs Rs 499
```

Both lines are the same. When you write `python_course.describe()`, Python turns it into `Course.describe(python_course)`. The object in front of the dot becomes `self`. That is the whole secret of `self`.

If you forget `self`, as in `def describe():`:

```bash
python missing_self.py
```

```text
Traceback (most recent call last):
  File "missing_self.py", line 11, in <module>
    print(python_course.describe())
          ~~~~~~~~~~~~~~~~~~~~~~^^
TypeError: Course.describe() takes 0 positional arguments but 1 was given
```

You passed nothing, but Python quietly passed the object, and the method had no name to receive it. Every method begins with `self`.

### 3. Methods with more parameters

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def price_after(self, percent):
        return self.price * (100 - percent) // 100

    def apply_discount(self, percent):
        self.price = self.price_after(percent)


python_course = Course("Python", 499)
print(python_course.price_after(10), python_course.price)
python_course.apply_discount(10)
print(python_course.price)
```

```bash
python discount.py
```

```text
449 499
449
```

- `price_after` only works out an answer. The course keeps its price (499).
- `apply_discount` changes the course itself, and reuses `price_after` by calling `self.price_after(...)`.
- `//` is floor division: `499 * 90 // 100` is `449`. No floats for money.

Good habit: if the caller needs an answer, return it. If the job is to change the object, change `self` and return nothing. A method that does both surprises people.

### 4. Where data lives: instance attributes and class attributes

Think of a school. Every student has their own bag (instance attribute, set with `self.` in `__init__`). The notice board in the hallway belongs to the whole school (class attribute, written directly in the class, with no `self`).

```python
class Course:
    currency = "Rs"

    def __init__(self, title, price):
        self.title = title
        self.price = price


python_course = Course("Python", 499)
sql_course = Course("SQL", 399)
print(python_course.currency, sql_course.currency)
Course.currency = "INR"
print(python_course.currency, sql_course.currency)
python_course.currency = "USD"
print(python_course.currency, sql_course.currency)
print(Course.currency)
```

```bash
python currency.py
```

```text
Rs Rs
INR INR
USD INR
INR
```

Two rules:

- Reading looks in the object first, then in the class.
- Writing through an object always writes into that object's own bag. `python_course.currency = "USD"` gave that one course its own `currency`; the class value stayed `INR`. To change the shared value for everybody, write through the class name: `Course.currency = "INR"`.

Use a class attribute only for a value that is the same for every object and does not change per object (a currency, a platform name, a limit).

### 5. Prove that the list is shared

```python
class Course:
    students = []

    def __init__(self, title, price):
        self.title = title
        self.price = price


python_course = Course("Python", 499)
sql_course = Course("SQL", 399)
print(python_course.students is sql_course.students)
```

```bash
python shared_bad.py
```

```text
True
```

`students` is a class attribute, so there is only one list, and both courses have a label on it. `is` asks whether two names are on the same object.

### 6. The cure: create changeable things in `__init__`

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price
        self.students = []


python_course = Course("Python", 499)
sql_course = Course("SQL", 399)
python_course.students.append("Lukas")
print(sql_course.students)
print(python_course.students is sql_course.students)
```

```bash
python shared_fixed.py
```

```text
[]
False
```

This is the same trap as the mutable default argument from the functions module: one list made once and shared. Rule: a class attribute is fine for a value that is the same for everyone and never changes. Anything that can change (a list, a dictionary, a set) is created in `__init__`, so each object gets its own.

### 7. Class methods: another way to build an object

A line starting with `@` above a `def` is a decorator, a label that changes how the function behaves (you will build your own in Module 9). `@classmethod` says: this method belongs to the class, so its first name is not `self` but `cls`, the class itself.

A tiny test first:

```python
class Course:
    @classmethod
    def show(cls):
        print(cls)


Course.show()
```

```bash
python cls_demo.py
```

```text
<class '__main__.Course'>
```

`cls` is `Course`, handed over by Python: the class in front of the dot. So `cls(title, price)` does the same as `Course(title, price)`. Now a real one. Rows from a CSV file arrive as dictionaries and every value is text, so the price must become an `int`:

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], int(data["price"]))


row = {"title": "Python", "price": "499"}
python_course = Course.from_dict(row)
print(python_course.title, python_course.price + 1)
```

```bash
python from_dict.py
```

```text
Python 500
```

`price + 1` worked, so the price is a real number. A second door, `from_line`, for text like `SQL, 399`:

```python
    @classmethod
    def from_line(cls, line):
        title, price = line.split(",")
        return cls(title.strip(), int(price))


sql_course = Course.from_line("SQL, 399")
print(sql_course.title, sql_course.price)
```

```bash
python from_line.py
```

```text
SQL 399
```

By habit, a class method that builds an object is named `from_...`. We use `cls` and not the name `Course` inside, because in the inheritance lesson a child class can reuse the method and `cls` will then be the child class.

### 8. Static methods: a helper that needs nothing

A price typed as `Rs 1,499` should become `1499`. The helper needs no object and no class, so it is a static method: no `self`, no `cls`.

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @staticmethod
    def price_from_text(text):
        return int(text.replace("Rs", "").replace(",", ""))


print(Course.price_from_text("Rs 1,499"))
```

```bash
python price_from_text.py
```

```text
1499
```

It could also be a plain function outside the class, and often that is fine. Put it inside when it clearly belongs with the class.

Which kind of method?

- Needs the data of one object (for example "is this course free?"): a normal method, receives `self`.
- Builds an object in a new way (for example from a line of text): a class method, receives `cls`.
- Needs neither (for example cleaning a piece of text): a static method, receives nothing.

### 9. Pitfalls

Calling a method without brackets:

```bash
python no_brackets.py
```

```text
<bound method Course.describe of <__main__.Course object at 0x105195fd0>>
```

A name without brackets is not a call. "Bound" means the method is already tied to `python_course`. The address **will differ** on your machine. Fix: `python_course.describe()`.

Forgetting `self.` inside a method (`return price == 0`):

```bash
python no_self.py
```

```text
Traceback (most recent call last):
  File "no_self.py", line 10, in <module>
    print(Course("Python", 499).is_free())
          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "no_self.py", line 7, in is_free
    return price == 0
           ^^^^^
NameError: name 'price' is not defined. Did you mean: 'self.price'?
```

Forgetting the decorator (`def from_dict(cls, data)` without `@classmethod`):

```bash
python no_decorator.py
```

```text
Traceback (most recent call last):
  File "no_decorator.py", line 11, in <module>
    python_course = Course.from_dict(row)
TypeError: Course.from_dict() missing 1 required positional argument: 'data'
```

Without the decorator the dictionary landed in `cls`, and `data` got nothing.

### 10. Try it yourself

Make a `Course` with a class attribute `tax_percent = 18`, a method `with_tax` that returns the price plus tax (floor divide), and a class method `from_line`. Print `with_tax()` of the course built from `"Python,500"`. Solution is `tryit.py`:

```bash
python tryit.py
```

```text
590
```

## Common mistakes

- A changeable list or dictionary written directly in the class: every object shares it. Create it in `__init__`.
- Forgetting `self` as the first name of a method.
- Writing `price` instead of `self.price` inside a method.
- Forgetting the brackets when calling a method (you get a "bound method" printed).
- Forgetting `@classmethod`: the first argument is then treated as `self`.
- Thinking `python_course.currency = "USD"` changes the class: it only creates an attribute on that one object.

## Clean up

Nothing to clean up. If Python created a `__pycache__` folder, you can delete it.

## Next

[M08-L03 · Encapsulation and Properties](../m08-l03-encapsulation-and-properties/README.md)
