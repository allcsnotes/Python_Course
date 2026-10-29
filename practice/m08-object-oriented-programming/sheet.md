# Module 08 · Practice Sheet: 20 Object-Oriented Programming Exercises

Write each program yourself before you open the answer. Every exercise is a small Python file you can run in the terminal. The exercises use Module 8 (classes and objects, attributes and methods, encapsulation and properties, inheritance and composition, dunder methods, dataclasses, enums and abstract classes) and may also use anything from Modules 1 to 7.

**How to work:**
- Use **Python 3.14** (check with `python --version`; on Mac or Linux the command may be `python3`).
- Put each program in its own file, `Ex01.py` to `Ex20.py`. Run it with **`python Ex01.py`**.
- The exercises use the allcsvideos platform and its cast: Asha, Lukas, Priya, Meera and Rahul (plus Sofia, Arjun, Mia and Chen as extra students). Money is written as **Rs**, always in whole rupees.
- They go from easy to harder, **about three or four per lesson**. Some are **predict the output** (guess on paper first, then run), some are **fix the broken code** (read the error, or the wrong output, then repair it), and some build a small class.
- Each answer has a hint, a short explanation, a full solution, and the **real output** from running it with Python 3.14. Open the hint first, and only then the solution.
- All 20 solutions are in the folder **`solutions/`** next to this sheet. Run them with `python Ex07.py` from inside that folder.
- None of the exercises read from the keyboard or from files, so nothing needs typing while a program runs.
- Where an error is printed, the exact words come from Python 3.14. Older versions word some of these messages a little differently.

---


## M08 · L01 Classes and Objects

### 1 · The student class
Asha needs a place to keep the students of allcsvideos. Write a class `Student` whose `__init__` takes `name` and `city` and stores both on the object. Then:

1. make three students: Lukas from Frankfurt, Priya from Delhi and Sofia from Madrid
2. put them in a list called `students` and loop over it, printing `Lukas lives in Frankfurt` and so on
3. Priya moves: change her `city` to `"Mumbai"` and print `Priya moved to Mumbai`
4. print the cities of Lukas and Sofia (they must not have changed)
5. print `type(lukas) is Student`

### 2 · Predict the output (objects, labels and their own data)
**Write your guesses first.** The class `Lesson` is a blueprint, and `a`, `b`, `c` and `twin` are labels. Predict every line this file prints (it prints 7 lines). Pay attention to which labels point at the **same** object.

```python
class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes


a = Lesson("Variables", 12)
b = Lesson("Loops", 18)
c = a
c.minutes = 15
twin = Lesson("Loops", 18)

print(a.minutes, b.minutes)
print(c is a, b is twin)
print(type(a) is Lesson)
print(vars(b))
print(a.minutes + b.minutes)
b.title = "Loops 2"
print(twin.title, b.title)
print(b.minutes == twin.minutes)
```

Run it and mark your wrong guesses. Draw the labels as sticky notes on boxes if you get stuck on `c` and `a`.

### 3 · Fix the broken class code
Meera sent five small files that all use a class. Run each one and read what happens. Files a, b, c and d crash; file e does **not** crash but prints a number you did not want. Fix them all, then put the repaired versions in one file.

```python
# file a
class Course:
    def __init__(self, title, price):
        title = title
        self.price = price


course = Course("Python", 499)
print(course.title)
```
```python
# file b
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


sql = Course("SQL")
print(sql.title, sql.price)
```
```python
# file c
class Lesson:
    def __init__(title, minutes):
        title.minutes = minutes


lesson = Lesson("Variables", 12)
print(lesson.minutes)
```
```python
# file d
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


course = Course("Python", 499)
print(course.pricee)
```
```python
# file e
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price


course = Course("Python", 499)
course.pricee = 399
print(course.price)
```

What Python says:

```text
a: AttributeError: 'Course' object has no attribute 'title'
b: TypeError: Course.__init__() missing 1 required positional argument: 'price'
c: TypeError: Lesson.__init__() takes 2 positional arguments but 3 were given
d: AttributeError: 'Course' object has no attribute 'pricee'. Did you mean: 'price'?
e: (no error) prints   499
```

**Goal after fixing all five** (the repaired classes and calls in one file, in the same order; for file e, change the price to 399 correctly):

```text
Python
SQL 399
Variables 12
499
399
```

## M08 · L02 Attributes and Methods

### 4 · Discounts and tax
Priya is adding prices to the allcsvideos shop. Write a class `Course` with:

- a **class attribute** `tax_percent = 18`
- `__init__(self, title, price)`
- `describe(self)` that **returns** `Python costs Rs 499` style text
- `price_after(self, percent)` that **returns** the price after the discount, without changing the course (whole rupees: use `//`)
- `apply_discount(self, percent)` that **changes** the course's own price using `price_after`
- `with_tax(self)` that returns the price plus `tax_percent` percent (whole rupees)

Then, in this order:

1. build `py = Course("Python", 499)` and print `py.describe()`
2. print `py.price_after(20)` and `py.price` on one line
3. call `py.apply_discount(20)` and print `py.describe()` again
4. print `py.with_tax()`
5. set `Course.tax_percent = 5` and print `py.with_tax()` again
6. give only `py` its own `tax_percent = 0`, build `sql = Course("SQL", 399)`, and print `py.with_tax()` and `sql.with_tax()` on one line

**Expected output:**

```text
Python costs Rs 499
399 499
Python costs Rs 399
470
418
399 418
```

### 5 · Predict the output (class attributes)
**Write your guesses first.** `currency` and `students` are written on the **class**, not inside `__init__`. Predict every line this file prints (it prints 6 lines).

```python
class Course:
    currency = "Rs"
    students = []

    def __init__(self, title, price):
        self.title = title
        self.price = price


py = Course("Python", 499)
sql = Course("SQL", 399)
print(py.currency, sql.currency, Course.currency)
Course.currency = "INR"
print(py.currency, sql.currency)
py.currency = "USD"
print(py.currency, sql.currency, Course.currency)
py.students.append("Lukas")
print(sql.students)
print(py.students is sql.students)
print(vars(py))
```

Run it and mark your wrong guesses. Look hard at the last three lines: what really lives inside `py`?

### 6 · Fix the broken method code
Lukas wrote four small files with methods. Files a, b and c crash; file d does **not** crash but gives a surprising answer. Fix them all, then put the repaired versions in one file.

```python
# file a
class Course:
    def __init__(self, title):
        self.title = title

    def describe():
        return "A course"


print(Course("Python").describe())
```
```python
# file b
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def from_dict(cls, data):
        return cls(data["title"], int(data["price"]))


sql = Course.from_dict({"title": "SQL", "price": "399"})
print(sql.title)
```
```python
# file c
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def is_free(self):
        return price == 0


print(Course("Python", 499).is_free())
```
```python
# file d
class Course:
    students = []

    def __init__(self, title):
        self.title = title


py = Course("Python")
sql = Course("SQL")
py.students.append("Lukas")
print(sql.students)
```

What Python says:

```text
a: TypeError: Course.describe() takes 0 positional arguments but 1 was given
b: TypeError: Course.from_dict() missing 1 required positional argument: 'data'
c: NameError: name 'price' is not defined. Did you mean: 'self.price'?
d: (no error) prints   ['Lukas']   even though Lukas joined only Python
```

**Goal after fixing all four** (one `Course` class that has all the repaired methods, then these checks):

```text
Python costs Rs 499
SQL 400
False True
[]
['Lukas']
```

### 7 · Courses from text
The allcsvideos admin page sends courses as text lines like `Python; Rs 1,499` (the title, a semicolon, then a price with `Rs` and commas). Write a class `Course` with `title` and `price` (a whole number) and add:

- a `@staticmethod` `price_from_text(text)` that turns `"Rs 1,499"` into the number `1499`
- a `@classmethod` `from_line(cls, line)` that splits a line at `;`, strips the title, uses `price_from_text` for the price and returns a new course
- a `@classmethod` `from_dict(cls, data)` for a row like `{"title": "Git", "price": "299"}` (the price arrives as text) 

Then:

1. print `Course.price_from_text("Rs 1,499")`
2. build courses from `["Python; Rs 499", "SQL; Rs 399", "Docker; Rs 449"]`, print each title and price, and the total
3. build a course from the row above and print its title and its price plus 1 (proving the price is a number)

**Expected output:**

```text
1499
Python 499
SQL 399
Docker 449
Total: Rs 1347
Git 300
```

## M08 · L03 Encapsulation and Properties

### 8 · A lesson that checks its minutes
Rahul says a lesson cannot last 0 minutes. Write a class `Lesson` with `title` and `minutes`, where:

- `minutes` is a **property** whose setter raises `ValueError(f"minutes must be at least 1, got {value}")` for anything below 1, and the check also runs when the lesson is first created (so `__init__` must go through the setter)
- `is_long` is a **read-only property** that is `True` when the minutes are above 60 (it calculates from the stored value)

Then:

1. build `Lesson("Classes", 45)` and print `is_long`
2. set `minutes` to 90 and print the minutes and `is_long` on one line
3. try to set `minutes` to 0; catch the error and print `Rejected:` plus the message; then print the minutes (still 90)
4. try to build `Lesson("Empty", -5)`; catch the error and print `Rejected:` plus the message
5. try `lesson.is_long = True`; catch the `AttributeError` and print `Cannot set:` plus the message

**Expected output:**

```text
False
90 True
Rejected: minutes must be at least 1, got 0
90
Rejected: minutes must be at least 1, got -5
Cannot set: property 'is_long' of 'Lesson' object has no setter
```

### 9 · Predict the output (underscore, double underscore, property)
**Write your guesses first.** A `Wallet` hides its pin behind a double underscore and its balance behind a property. Predict every line this file prints (it prints 8 lines). One line prints an error message; guess its exact words.

```python
class Wallet:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__pin = "4821"
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError(f"balance cannot be negative, got {value}")
        self._balance = value


wallet = Wallet("Priya", 500)
print(wallet.owner, wallet.balance)
wallet.balance = 700
print(wallet.balance)
try:
    wallet.balance = -1
except ValueError as error:
    print("Error:", error)
print(wallet.balance)
wallet._balance = -50
print(wallet.balance)
try:
    print(wallet.__pin)
except AttributeError as error:
    print("Error:", error)
print(wallet._Wallet__pin)
print(vars(wallet))
```

Run it and mark your wrong guesses. Remember that `vars(...)` shows the attributes an object really stores.

### 10 · Fix the broken property code
Asha's `Course` should guard its price with a property. Four files go wrong. Run each one and read what happens. Files a, b and c crash; file d does **not** crash but prints a price that should never be allowed. Fix them all, then put one repaired `Course` class in one file with the checks below.

```python
# file a
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self.price = value


course = Course("Python", 499)
```
```python
# file b
class Course:
    def __init__(self, title, price):
        self.title = title
        self._price = price

    @property
    def price(self):
        return self._price


course = Course("Python", 499)
print(course.price())
```
```python
# file c
class Course:
    def __init__(self, title, price):
        self.title = title
        self._price = price

    @property
    def price(self):
        return self._price


course = Course("Python", 499)
course.price = 399
```
```python
# file d
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
course._price = -500
print(course.price)
```

What Python says:

```text
a: RecursionError: maximum recursion depth exceeded
b: TypeError: 'int' object is not callable
c: AttributeError: property 'price' of 'Course' object has no setter
d: (no error) prints   -500
```

**Goal after fixing all four** (one `Course` class with the property, a working setter that checks for negatives, then these checks: print the price; set it to 399 and print it; try to set -500 inside `try`/`except ValueError` and print `Rejected:` plus the message; print the price again):

```text
499
399
Rejected: price cannot be negative, got -500
399
```

## M08 · L04 Inheritance and Composition

### 11 · People of allcsvideos
Meera wants one blueprint for all people of the platform. Write:

- a class `Person` with `__init__(self, name)` and `greet(self)` that returns `Hello, I am Lukas` style text
- a class `Student(Person)` whose `__init__(self, name, email)` calls `super().__init__(name)` and then stores the `email`
- a class `Instructor(Person)` whose `__init__(self, name, subject)` also calls `super().__init__(name)`, stores `subject`, and **overrides** `greet` so that it returns the parent's greeting followed by `, I teach Python` (use `super().greet()` and the stored subject)

Then:

1. build `lukas = Student("Lukas", "lukas@example.com")` and `meera = Instructor("Meera", "Python")`
2. loop over both in a list and print each `greet()`
3. print Lukas's email
4. print `isinstance(meera, Person)`, `isinstance(meera, Student)` and `type(meera) is Person` on one line
5. print `isinstance(lukas, Person)` and `isinstance(lukas, Instructor)` on one line

**Expected output:**

```text
Hello, I am Lukas
Hello, I am Meera, I teach Python
lukas@example.com
True False False
True False
```

### 12 · Predict the output (method lookup order and error families)
**Write your guesses first.** Two things happen in this file: a class with **two** parents, and a family of error classes. Predict every line this file prints (it prints 7 lines).

```python
class Person:
    def role(self):
        return "member"


class Student(Person):
    def role(self):
        return "learns"


class Instructor(Person):
    def role(self):
        return "teaches"


class TeachingAssistant(Student, Instructor):
    pass


class Visitor(Person):
    pass


priya = TeachingAssistant()
print(priya.role())
print([c.__name__ for c in TeachingAssistant.__mro__])
print(Visitor().role())
print(isinstance(priya, Instructor), isinstance(priya, Visitor))


class PaymentError(Exception):
    pass


class CardDeclinedError(PaymentError):
    pass


class UpiTimeoutError(PaymentError):
    pass


def pay(kind):
    if kind == "card":
        raise CardDeclinedError("card was declined")
    if kind == "upi":
        raise UpiTimeoutError("upi timed out")
    return "paid"


for kind in ["cash", "card", "upi"]:
    try:
        print(pay(kind))
    except CardDeclinedError as error:
        print("Declined:", error)
    except PaymentError as error:
        print("Other payment problem:", error)
```

Run it and mark your wrong guesses. For the first block, write the lookup order down before you call `role()`.

### 13 · Fix the broken inheritance code
Three files about the allcsvideos people and courses. Files a and b crash; file c does **not** crash but says something silly. Fix them all, then put the repaired versions in one file.

```python
# file a
class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, email):
        self.email = email


priya = Student("Priya", "priya@example.com")
print(priya.email)
print(priya.name)
```
```python
# file b
class Person:
    def __init__(self, name):
        self.name = name


class Instructor(Person):
    def __init__(self, name, subject):
        super().__init__()
        self.subject = subject


meera = Instructor("Meera", "Python")
```
```python
# file c
class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes


class Course(Lesson):
    pass


course = Course("Python Basics", 600)
print(isinstance(course, Lesson))
```

What Python says:

```text
a: AttributeError: 'Student' object has no attribute 'name'   (after printing the email)
b: TypeError: Person.__init__() missing 1 required positional argument: 'name'
c: (no error) prints   True   but a course is not a kind of lesson
```

**Goal after fixing all three** (for file c, a course should **have** lessons in a list, with `add(lesson)` and `total_minutes()` methods; add the lessons Variables 12 and Loops 18 and print `isinstance(basics, Lesson)` and the total):

```text
priya@example.com
Priya
Meera Python
False
30
```

## M08 · L05 Dunder Methods

### 14 · Predict the output (__str__ and __repr__)
**Write your guesses first.** `Course` has both `__str__` and `__repr__`; `Lesson` has only `__repr__`. Predict every line this file prints (it prints 9 lines). Decide for each line whether Python uses the friendly text or the developer text.

```python
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        return f"{self.title} (Rs {self.price})"

    def __repr__(self):
        return f"Course({self.title!r}, {self.price})"


class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes

    def __repr__(self):
        return f"Lesson({self.title!r}, {self.minutes})"


course = Course("Python Basics", 499)
lesson = Lesson("Loops", 18)
print(course)
print(repr(course))
print([course])
print(f"Now watching: {course}")
print(f"{course!r}")
print(lesson)
print(str(lesson))
print([lesson, lesson])
print("Lesson:", lesson)
```

Run it and mark your wrong guesses.

### 15 · Equal courses and sets
Two `Course` objects with the same title should count as the same course. Write a class `Course` with `title`, `price` and `lessons`, then add:

- `__repr__` returning text like `Course('Python Basics', 499)` (use `!r` for the title)
- `__eq__` that returns `NotImplemented` when `other` is not a `Course`, and otherwise compares the **title** only
- `__hash__` built from the same field, `hash(self.title)`, so a course can sit in a set or be a dictionary key

Then, with `first`, `twin` (`Course("Python Basics", 399, ["Intro"])`: same title, other price and lessons) and `other` (`Course("Loops Deep Dive", 299, ["while", "for"])`):

1. print `first == twin` and `first is twin`
2. print `first == other` and `first != other`
3. print `first == 5`
4. put `first`, `twin` and `other` in a set and print its size
5. make `sales = {first: 3}` and print `sales[twin]`
6. print `twin in sales` and `other in sales`

**Expected output:**

```text
True False
False True
False
2
3
True False
```

### 16 · A course that feels built-in
A `Course` should behave like a collection of its lessons. Write a class `Course` with `title`, `price` and `lessons` (a list of text), then add:

- `__str__` returning `Python Basics (Rs 499)` style text
- `__len__` (number of lessons), `__iter__` (loop over the lessons) and `__getitem__` (index and slice the lessons)
- `__lt__` comparing by `price`, so courses can be sorted

Build `basics` (Python Basics, Rs 499, lessons `Intro`, `Loops`, `Lists`), `loops` (Loops Deep Dive, Rs 299, `while`, `for`), `soon` (Coming Soon, Rs 0, no lessons) and `data` (Data Structures, Rs 899, `List`, `Dict`). Then:

1. print `len(basics)` and `len(loops)`
2. print `bool(basics)` and `bool(soon)`
3. loop over `basics` and print each lesson
4. print `"Loops" in basics` and `"Dict" in basics`
5. print `basics[0]`, `basics[-1]` and `basics[:2]` on one line
6. print `list(loops)`
7. loop over `sorted([basics, loops, data])` and print each course
8. print `min(basics, loops, data)` and then `max(...)` of the same three
9. sort the same three by title with `key=lambda c: c.title` and print them

**Expected output:**

```text
3 2
True False
Intro
Loops
Lists
True False
Intro Lists ['Intro', 'Loops']
['while', 'for']
Loops Deep Dive (Rs 299)
Python Basics (Rs 499)
Data Structures (Rs 899)
Loops Deep Dive (Rs 299)
Data Structures (Rs 899)
Data Structures (Rs 899)
Loops Deep Dive (Rs 299)
Python Basics (Rs 499)
```

### 17 · Fix the broken dunder code
Five files with special methods. Files a, c and d crash; file b prints something ugly, and file e prints a result that should not happen. Fix them all, then put one repaired `Course` class in one file with the checks below.

```python
# file a
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        return self.price


print(Course("Python Basics", 499))
```
```python
# file b
class Course:
    def __init__(self, title):
        self.title = title

    def __str_(self):
        return self.title


print(Course("Python Basics"))
```
```python
# file c
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)


course = Course("Python Basics", 499)
print(course == 5)
```
```python
# file d
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __eq__(self, other):
        return self.title == other.title


print(len({Course("Python Basics", 499)}))
```
```python
# file e
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __eq__(self, other):
        if not isinstance(other, Course):
            return NotImplemented
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)


basics = Course("Python Basics", 499)
seen = {basics}
print(basics in seen)
basics.title = "Python Advanced"
print(basics in seen)
```

What Python says:

```text
a: TypeError: __str__ returned non-string (type int)
b: (no error) prints   <__main__.Course object at 0x...>   (your number will differ)
c: AttributeError: 'int' object has no attribute 'title'
d: TypeError: cannot use 'Course' as a set element (unhashable type: 'Course')
e: (no error) prints   True   then   False   for the same object
```

**Goal after fixing all five** (one `Course` class with `title`, `price`, `__str__`, `__eq__` and `__hash__`; then: print a course; print `course == 5`; print the size of a set holding `basics` and a second course called `"Loops"`; print `basics in seen`; and for file e, instead of changing the title of an object that sits in a set, build a **new** `Course("Python Advanced", 499)` called `renamed` and print `renamed in seen`):

```text
Python Basics (Rs 499)
False
2
True
False
```

## M08 · L06 Dataclasses, Enums and Abstract Classes

### 18 · Students, statuses and reports
Build a small model of student progress using all three tools of this lesson.

1. An `Enum` called `Status` with `ACTIVE = "active"` and `PAUSED = "paused"`.
2. A **frozen** dataclass `Lesson` with `title: str` and `minutes: int`, and a `__post_init__` that raises `ValueError("minutes must be positive")` when `minutes` is 0 or less.
3. A dataclass `Student` with `name: str`, `status: Status = Status.ACTIVE` and `done: list` that starts empty for every student (use `field(default_factory=list)`).
4. An abstract class `Report` (inherit from `ABC`) with an `@abstractmethod` `render(self, student)`; and two subclasses: `ShortReport` returning `Asha: 2 lessons` style text, and `LongReport` returning `Asha (active) finished: Variables Loops` style text (loop over the lessons and build the text with an f-string).

Then:

1. build `asha = Student("Asha")` and `lukas = Student("Lukas", Status.PAUSED)`; add the lessons Variables (12) and Loops (15) to Asha's `done`
2. print `asha` and `lukas` as they are (the generated text)
3. loop over `Status` and print each `name` and `value`
4. render both reports for Asha, and the short report for Lukas
5. try to build `Lesson("Empty", 0)`; catch the `ValueError` and print `Rejected:` plus the message
6. try to build `Report()` itself; catch the `TypeError` and print `TypeError:` plus the message

**Expected output:**

```text
Student(name='Asha', status=<Status.ACTIVE: 'active'>, done=[Lesson(title='Variables', minutes=12), Lesson(title='Loops', minutes=15)])
Student(name='Lukas', status=<Status.PAUSED: 'paused'>, done=[])
ACTIVE active
PAUSED paused
Asha: 2 lessons
Asha (active) finished: Variables Loops
Lukas: 0 lessons
Rejected: minutes must be positive
TypeError: Can't instantiate abstract class Report without an implementation for abstract method 'render'
```

### 19 · Predict the output (dataclass and Enum)
**Write your guesses first.** A dataclass called `Lesson` and an Enum called `Level` share one file. Predict every line this file prints (it prints 15 lines). Several lines print the text of an error; guess its exact words too.

```python
from dataclasses import dataclass
from enum import Enum


class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


@dataclass
class Lesson:
    title: str
    minutes: int
    free: bool = False


print(Lesson("Variables", 12))
print(Lesson("Welcome", 3, True))
a = Lesson("Loops", 15, free=True)
b = Lesson("Loops", 15, True)
print(a == b, a is b)
a.minutes = 20
print(a == b, a)

try:
    done = {a, b}
except TypeError as error:
    print("TypeError:", error)

level = Level.INTERMEDIATE
print(level)
print(level.name, level.value)
print(Level(3), Level["BEGINNER"])
for item in Level:
    print(item.value, item.name)
print(len(Level))
print(level == Level.INTERMEDIATE, level == 2)

try:
    print(Level.BEGINNER < Level.ADVANCED)
except TypeError as error:
    print("TypeError:", error)

try:
    print(Level(9))
except ValueError as error:
    print("ValueError:", error)
```

Run it and mark your wrong guesses.

### 20 · Fix the broken dataclass and abstract code
Five files go wrong. Files a, b, c and d crash; file e does **not** crash, but it should have. Fix them all, then put the repaired versions in one file.

```python
# file a
from dataclasses import dataclass


@dataclass
class Lesson:
    title: str
    free: bool = False
    minutes: int
```
```python
# file b
from dataclasses import dataclass


@dataclass
class Course:
    title: str
    lessons: list = []
```
```python
# file c
from dataclasses import dataclass


@dataclass(frozen=True)
class Tag:
    name: str


tag = Tag("python")
tag.name = "python-3"
```
```python
# file d
from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class CardPayment(Payment):
    def charge(self, amount):
        print(f"Charged Rs {amount}")


CardPayment().pay(2499)
```
```python
# file e
from abc import abstractmethod


class Payment:
    @abstractmethod
    def pay(self, amount):
        pass


payment = Payment()
print("Created with no error")
```

What Python says:

```text
a: TypeError: non-default argument 'minutes' follows default argument 'free'
b: ValueError: mutable default <class 'list'> for field lessons is not allowed: use default_factory
c: dataclasses.FrozenInstanceError: cannot assign to field 'name'
d: TypeError: Can't instantiate abstract class CardPayment without an implementation for abstract method 'pay'
e: (no error) prints   Created with no error   but nobody checked the promise
```

**Goal after fixing all five** (for file c, make a **new** `Tag("python-3")` instead of changing the old one; for files d and e, a repaired `Payment` that really is abstract and a `CardPayment` that implements `pay`; then try to build `Payment()` itself inside `try`/`except TypeError`):

```text
Lesson(title='Variables', minutes=12, free=False)
Course(title='Python', lessons=['Variables'])
Course(title='SQL', lessons=[])
Tag(name='python') Tag(name='python-3')
Charged Rs 2499
TypeError: Can't instantiate abstract class Payment without an implementation for abstract method 'pay'
```


---

## Answers

Click an exercise to open its solution. Your code does not have to match line for line; it should produce the same output.


<details>
<summary><b>1 · The student class</b></summary>

**Hint.** Inside `__init__`, `self` is the new object, so `self.name = name` writes the name onto that one object. Call the class like a function, `Student("Lukas", "Frankfurt")`, and Python passes `self` for you. You change one attribute with `priya.city = ...`.

The class is the blueprint and each call builds one house. All three students have the same two attributes, but every object keeps its own values, so moving Priya does not touch Lukas or Sofia. `type(lukas) is Student` is `True` because `Student` is the class the object was built from.

`solutions/Ex01.py`, run with `python Ex01.py`:

```python
# Exercise 01 - The student class
class Student:
    def __init__(self, name, city):
        self.name = name
        self.city = city


lukas = Student("Lukas", "Frankfurt")
priya = Student("Priya", "Delhi")
sofia = Student("Sofia", "Madrid")

students = [lukas, priya, sofia]
for student in students:
    print(student.name, "lives in", student.city)

priya.city = "Mumbai"
print(priya.name, "moved to", priya.city)
print(lukas.city, sofia.city)
print(type(lukas) is Student)
```

Output (Python 3.14):

```text
Lukas lives in Frankfurt
Priya lives in Delhi
Sofia lives in Madrid
Priya moved to Mumbai
Frankfurt Madrid
True
```

</details>


<details>
<summary><b>2 · Predict the output (objects, labels and their own data)</b></summary>

**Hint.** `c = a` does not build a new lesson; it sticks a second label on the same object (the labels-on-boxes picture from Module 2 and Module 5). `twin` was built by a second call to `Lesson(...)`, so it is a different object even though its values match.

`c.minutes = 15` changes the one shared object, so `a.minutes` is 15 as well, and `c is a` is `True`. `b` and `twin` hold equal values but live in two boxes, so `b is twin` is `False`. `vars(b)` shows the data the object really carries: a dictionary of its attributes. Renaming `b.title` does not touch `twin`, because each object keeps its own data.

`solutions/Ex02.py`, run with `python Ex02.py`:

```python
# Exercise 02 - Predict the output (objects, labels and their own data)
class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes


a = Lesson("Variables", 12)
b = Lesson("Loops", 18)
c = a
c.minutes = 15
twin = Lesson("Loops", 18)

print(a.minutes, b.minutes)
print(c is a, b is twin)
print(type(a) is Lesson)
print(vars(b))
print(a.minutes + b.minutes)
b.title = "Loops 2"
print(twin.title, b.title)
print(b.minutes == twin.minutes)
```

Output (Python 3.14):

```text
15 18
True False
True
{'title': 'Loops', 'minutes': 18}
33
Loops Loops 2
True
```

</details>


<details>
<summary><b>3 · Fix the broken class code</b></summary>

**Hint.** Every method of a class gets the object as its **first** parameter, and it is called `self` by convention. In file a, `title = title` only sets a plain variable inside the function; nothing is written on the object. In file c, `self` is missing, so the first name (`title`) swallows the object and the two real arguments no longer fit. In file e the typo is in an assignment, and an assignment cannot fail: it quietly creates a brand new attribute.

Reading an attribute that does not exist is an error (file d, with a helpful "Did you mean"), but **writing** one never is, which is why file e prints the old 499 and says nothing. This is the same weakness as the misspelled dictionary key from the first lesson, only quieter. Count the arguments in the `TypeError` messages: Python counts `self` too, so `Course("SQL")` supplied only 2 of the 3 values `__init__` needs.

`solutions/Ex03.py`, run with `python Ex03.py`:

```python
# Exercise 03 - Fix the broken class code (all five repaired)
class Course:
    def __init__(self, title, price):
        self.title = title              # was: title = title  (no self.)
        self.price = price


course = Course("Python", 499)
print(course.title)

sql = Course("SQL", 399)                # was: Course("SQL")  (price missing)
print(sql.title, sql.price)


class Lesson:
    def __init__(self, title, minutes): # was: def __init__(title, minutes)  (no self)
        self.title = title
        self.minutes = minutes


lesson = Lesson("Variables", 12)
print(lesson.title, lesson.minutes)

print(course.price)                     # was: course.pricee  (typo)

course.price = 399                      # was: course.pricee = 399  (made a new attribute)
print(course.price)
```

Output (Python 3.14):

```text
Python
SQL 399
Variables 12
499
399
```

</details>


<details>
<summary><b>4 · Discounts and tax</b></summary>

**Hint.** `self.price` is data that belongs to one object, while `tax_percent` sits on the class and every object can read it through `self.tax_percent`. A method that only works something out should `return`; a method that changes the course assigns to `self.price`. `price_after` returns, `apply_discount` changes.

Step 2 shows that `price_after(20)` only calculates (399) and leaves `py.price` at 499. Step 3 then changes it for real. Changing the class attribute in step 5 changes the answer for every course that has not set its own. In step 6 the assignment `py.tax_percent = 0` creates a separate attribute on `py` only, which hides the class one for that object, so `py` pays no tax (399) and `sql` still uses the class value 5 (418).

`solutions/Ex04.py`, run with `python Ex04.py`:

```python
# Exercise 04 - Discounts and tax
class Course:
    tax_percent = 18

    def __init__(self, title, price):
        self.title = title
        self.price = price

    def describe(self):
        return f"{self.title} costs Rs {self.price}"

    def price_after(self, percent):
        return self.price * (100 - percent) // 100

    def apply_discount(self, percent):
        self.price = self.price_after(percent)

    def with_tax(self):
        return self.price * (100 + self.tax_percent) // 100


py = Course("Python", 499)
print(py.describe())
print(py.price_after(20), py.price)
py.apply_discount(20)
print(py.describe())
print(py.with_tax())

Course.tax_percent = 5
print(py.with_tax())

py.tax_percent = 0
sql = Course("SQL", 399)
print(py.with_tax(), sql.with_tax())
```

Output (Python 3.14):

```text
Python costs Rs 499
399 499
Python costs Rs 399
470
418
399 418
```

</details>


<details>
<summary><b>5 · Predict the output (class attributes)</b></summary>

**Hint.** Reading `py.currency` looks on `py` first, then on the class. Assigning to `py.currency` always writes on `py`, never on the class. A list stored on the class is **one** list that every object shares, like the mutable default from Module 4.

`Course.currency = "INR"` changes the one value both courses read. `py.currency = "USD"` puts a private `currency` on `py` that hides the class one, so `sql` and `Course` still say `INR`; `vars(py)` proves it by listing `currency` next to `title` and `price`. `py.students.append(...)` does not assign anything; it changes the single shared list, so `sql.students` shows `Lukas` too and `py.students is sql.students` is `True`. The fix is to create the list inside `__init__`, so every course gets its own.

`solutions/Ex05.py`, run with `python Ex05.py`:

```python
# Exercise 05 - Predict the output (class attributes)
class Course:
    currency = "Rs"
    students = []

    def __init__(self, title, price):
        self.title = title
        self.price = price


py = Course("Python", 499)
sql = Course("SQL", 399)
print(py.currency, sql.currency, Course.currency)
Course.currency = "INR"
print(py.currency, sql.currency)
py.currency = "USD"
print(py.currency, sql.currency, Course.currency)
py.students.append("Lukas")
print(sql.students)
print(py.students is sql.students)
print(vars(py))
```

Output (Python 3.14):

```text
Rs Rs Rs
INR INR
USD INR INR
['Lukas']
True
{'title': 'Python', 'price': 499, 'currency': 'USD'}
```

</details>


<details>
<summary><b>6 · Fix the broken method code</b></summary>

**Hint.** A normal method needs `self` as its first parameter: Python passes the object in without you writing it, so a method with no parameters gets one argument too many (file a). A method that starts from the class needs `@classmethod` on the line above it (file b). A bare name inside a method is a plain variable; the object's price is `self.price` (file c). For file d, the list must be created inside `__init__` as `self.students = []`.

File b shows what the decorator does: without it, `Course.from_dict(...)` treats your dictionary as the only argument and nothing is left for `data`. File d is the mutable default trap again, in class clothes: one list on the class belongs to everyone, so the repaired version builds a fresh list for each course and `sql.students` stays empty.

`solutions/Ex06.py`, run with `python Ex06.py`:

```python
# Exercise 06 - Fix the broken method code (all four repaired)
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price
        self.students = []                  # was: students = [] on the class (shared)

    def describe(self):                     # was: def describe():  (no self)
        return f"{self.title} costs Rs {self.price}"

    @classmethod                            # was: missing this line
    def from_dict(cls, data):
        return cls(data["title"], int(data["price"]))

    def is_free(self):
        return self.price == 0              # was: price == 0


py = Course("Python", 499)
print(py.describe())

sql = Course.from_dict({"title": "SQL", "price": "399"})
print(sql.title, sql.price + 1)

print(py.is_free(), Course("Intro", 0).is_free())

py.students.append("Lukas")
print(sql.students)
print(py.students)
```

Output (Python 3.14):

```text
Python costs Rs 499
SQL 400
False True
[]
['Lukas']
```

</details>


<details>
<summary><b>7 · Courses from text</b></summary>

**Hint.** A static method does not need the object or the class: it is just a helper that lives inside the class, so it has neither `self` nor `cls`. A class method receives the class as `cls`, and `cls(...)` builds a new object, so it works as a second way to create one. `line.split(";")` gives a list of two pieces, and `replace` can delete the `Rs` and the commas.

`price_from_text` is the same text clean-up you would write as a loose function, but keeping it in the class tells the reader what it is for. `from_line` and `from_dict` are called **alternative constructors**: the normal `Course("SQL", 799)` still works, and the class methods are extra doors that return the same kind of object. The `cls.price_from_text(...)` call inside `from_line` reaches the helper through the class.

`solutions/Ex07.py`, run with `python Ex07.py`:

```python
# Exercise 07 - Courses from text
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    @staticmethod
    def price_from_text(text):
        return int(text.replace("Rs", "").replace(",", ""))

    @classmethod
    def from_line(cls, line):
        title, price_text = line.split(";")
        return cls(title.strip(), cls.price_from_text(price_text))

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], int(data["price"]))


print(Course.price_from_text("Rs 1,499"))

lines = ["Python; Rs 499", "SQL; Rs 399", "Docker; Rs 449"]
courses = []
for line in lines:
    courses.append(Course.from_line(line))

total = 0
for course in courses:
    print(course.title, course.price)
    total += course.price
print("Total: Rs", total)

row = {"title": "Git", "price": "299"}
git = Course.from_dict(row)
print(git.title, git.price + 1)
```

Output (Python 3.14):

```text
1499
Python 499
SQL 399
Docker 449
Total: Rs 1347
Git 300
```

</details>


<details>
<summary><b>8 · A lesson that checks its minutes</b></summary>

**Hint.** Store the real value in `self._minutes` (a name with one underscore) and give the public name `minutes` a getter with `@property` and a setter with `@minutes.setter`. In `__init__` write `self.minutes = minutes` (without the underscore) so the setter runs. A property with no setter cannot be assigned to.

The one underscore is only a message to other programmers ("internal, please do not touch"); the property is what actually guards the door. Because `__init__` goes through the setter, a bad lesson cannot even be created (step 4). `is_long` has no data of its own: it is worked out every time it is read, so it can never go out of date. Step 5 shows the real Python 3.14 message when you assign to a property without a setter.

`solutions/Ex08.py`, run with `python Ex08.py`:

```python
# Exercise 08 - A lesson that checks its minutes
class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        if value < 1:
            raise ValueError(f"minutes must be at least 1, got {value}")
        self._minutes = value

    @property
    def is_long(self):
        return self._minutes > 60


lesson = Lesson("Classes", 45)
print(lesson.is_long)

lesson.minutes = 90
print(lesson.minutes, lesson.is_long)

try:
    lesson.minutes = 0
except ValueError as error:
    print("Rejected:", error)
print(lesson.minutes)

try:
    Lesson("Empty", -5)
except ValueError as error:
    print("Rejected:", error)

try:
    lesson.is_long = True
except AttributeError as error:
    print("Cannot set:", error)
```

Output (Python 3.14):

```text
False
90 True
Rejected: minutes must be at least 1, got 0
90
Rejected: minutes must be at least 1, got -5
Cannot set: property 'is_long' of 'Lesson' object has no setter
```

</details>


<details>
<summary><b>9 · Predict the output (underscore, double underscore, property)</b></summary>

**Hint.** A name that starts with two underscores (and does not end with two) is stored with the class name stuck in front of it, `_Wallet__pin`. A single underscore changes nothing at all: it is a request, not a lock. A setter only runs when you assign to the property name `balance`, not to `_balance`.

Python renames `__pin` inside the class to `_Wallet__pin`, so `wallet.__pin` from outside finds nothing and raises `AttributeError`, while `wallet._Wallet__pin` still works: name mangling is a speed bump to avoid accidents, not security. `wallet.balance = -1` is stopped by the setter, so the balance stays 700. But `wallet._balance = -50` walks around the property and writes straight onto the stored value, and the property then happily reads back -50. `vars(wallet)` shows all three stored names: `owner`, the mangled pin and `_balance`.

`solutions/Ex09.py`, run with `python Ex09.py`:

```python
# Exercise 09 - Predict the output (underscore, double underscore, property)
class Wallet:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__pin = "4821"
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError(f"balance cannot be negative, got {value}")
        self._balance = value


wallet = Wallet("Priya", 500)
print(wallet.owner, wallet.balance)
wallet.balance = 700
print(wallet.balance)
try:
    wallet.balance = -1
except ValueError as error:
    print("Error:", error)
print(wallet.balance)
wallet._balance = -50
print(wallet.balance)
try:
    print(wallet.__pin)
except AttributeError as error:
    print("Error:", error)
print(wallet._Wallet__pin)
print(vars(wallet))
```

Output (Python 3.14):

```text
Priya 500
700
Error: balance cannot be negative, got -1
700
-50
Error: 'Wallet' object has no attribute '__pin'
4821
{'owner': 'Priya', '_Wallet__pin': '4821', '_balance': -50}
```

</details>


<details>
<summary><b>10 · Fix the broken property code</b></summary>

**Hint.** In the setter, store the value in `self._price` (with the underscore). Writing `self.price = value` inside the setter calls the setter again, forever. A property is read like a plain attribute, with no brackets. A property needs its own `@price.setter` before assignment works. To use the guard you must assign to `course.price`, never to `course._price`.

File a loops because every `self.price = ...` goes through the setter, which assigns to `self.price`, which goes through the setter... until Python gives up with `RecursionError`. File b: `course.price` already **is** the number 499, so `course.price()` tries to call a number. File d shows the limit of the underscore convention: nothing stops you from writing `_price`, so the rule is to only do it from inside the class.

`solutions/Ex10.py`, run with `python Ex10.py`:

```python
# Exercise 10 - Fix the broken property code (all four repaired)
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
        self._price = value             # was: self.price = value  (calls itself forever)


course = Course("Python", 499)
print(course.price)                     # was: course.price()  (no brackets on a property)

course.price = 399                      # was a crash in a version with no setter
print(course.price)

try:
    course.price = -500                 # was: course._price = -500  (skips the check)
except ValueError as error:
    print("Rejected:", error)
print(course.price)
```

Output (Python 3.14):

```text
499
399
Rejected: price cannot be negative, got -500
399
```

</details>


<details>
<summary><b>11 · People of allcsvideos</b></summary>

**Hint.** `class Student(Person):` means "a student is a kind of person". A child's own `__init__` replaces the parent's, so call `super().__init__(name)` to still run the parent's part. `super().greet()` runs the parent's version of a method that you have overridden.

The loop in step 2 is the point of inheritance: the same call `person.greet()` runs different code depending on which kind of person it is. `isinstance(meera, Person)` is `True` because every instructor is a person, while `isinstance(meera, Student)` is `False`. `type(meera) is Person` is `False` because `type` reports the exact class (`Instructor`) and ignores parents; use `isinstance` when you mean "is a kind of".

`solutions/Ex11.py`, run with `python Ex11.py`:

```python
# Exercise 11 - People of allcsvideos
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I am {self.name}"


class Student(Person):
    def __init__(self, name, email):
        super().__init__(name)
        self.email = email


class Instructor(Person):
    def __init__(self, name, subject):
        super().__init__(name)
        self.subject = subject

    def greet(self):
        return super().greet() + f", I teach {self.subject}"


lukas = Student("Lukas", "lukas@example.com")
meera = Instructor("Meera", "Python")

for person in [lukas, meera]:
    print(person.greet())

print(lukas.email)
print(isinstance(meera, Person), isinstance(meera, Student), type(meera) is Person)
print(isinstance(lukas, Person), isinstance(lukas, Instructor))
```

Output (Python 3.14):

```text
Hello, I am Lukas
Hello, I am Meera, I teach Python
lukas@example.com
True False False
True False
```

</details>


<details>
<summary><b>12 · Predict the output (method lookup order and error families)</b></summary>

**Hint.** Python looks for a method in the class first, then follows the **method resolution order** (`__mro__`), a list that ends with `object`. For `TeachingAssistant(Student, Instructor)` the parents are tried left to right. In the `try` block, the first `except` that matches wins, and an `except` for a parent class also catches its children.

`TeachingAssistant` has no `role` of its own, so Python walks `TeachingAssistant`, `Student`, `Instructor`, `Person`, `object` and stops at `Student`: "learns" (this four-corners shape is called a diamond). `Visitor` has no `role` either and gets the one from `Person`. `isinstance(priya, Instructor)` is `True` because the second parent counts too. In the payment loop, `CardDeclinedError` is caught by the specific `except` first; `UpiTimeoutError` does not match it, so it falls to the `PaymentError` line, which catches every child of `PaymentError`. For `"cash"` nothing is raised and the function returns `paid`.

`solutions/Ex12.py`, run with `python Ex12.py`:

```python
# Exercise 12 - Predict the output (method lookup order and error families)
class Person:
    def role(self):
        return "member"


class Student(Person):
    def role(self):
        return "learns"


class Instructor(Person):
    def role(self):
        return "teaches"


class TeachingAssistant(Student, Instructor):
    pass


class Visitor(Person):
    pass


priya = TeachingAssistant()
print(priya.role())
print([c.__name__ for c in TeachingAssistant.__mro__])
print(Visitor().role())
print(isinstance(priya, Instructor), isinstance(priya, Visitor))


class PaymentError(Exception):
    pass


class CardDeclinedError(PaymentError):
    pass


class UpiTimeoutError(PaymentError):
    pass


def pay(kind):
    if kind == "card":
        raise CardDeclinedError("card was declined")
    if kind == "upi":
        raise UpiTimeoutError("upi timed out")
    return "paid"


for kind in ["cash", "card", "upi"]:
    try:
        print(pay(kind))
    except CardDeclinedError as error:
        print("Declined:", error)
    except PaymentError as error:
        print("Other payment problem:", error)
```

Output (Python 3.14):

```text
learns
['TeachingAssistant', 'Student', 'Instructor', 'Person', 'object']
member
True False
paid
Declined: card was declined
Other payment problem: upi timed out
```

</details>


<details>
<summary><b>13 · Fix the broken inheritance code</b></summary>

**Hint.** If a child defines its own `__init__`, the parent's `__init__` does **not** run by itself. Call `super().__init__(...)` and pass along everything the parent asks for. For file c ask yourself "is a course a kind of lesson, or does a course have lessons?" A "has" relation is **composition**: the course keeps its lessons in a list as an attribute.

File a never set `name` because the parent's `__init__` was skipped, and file b called it without the one thing it needs. File c is the classic mix-up: `Course(Lesson)` makes the code run, but `isinstance(course, Lesson)` says `True`, which is nonsense. A course is built **from** lessons, so it stores them (`self.lessons`) and adds up their minutes. Use inheritance for "is a", composition for "has a".

`solutions/Ex13.py`, run with `python Ex13.py`:

```python
# Exercise 13 - Fix the broken inheritance code (all three repaired)
class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, email):
        super().__init__(name)          # was: missing, so self.name was never set
        self.email = email


priya = Student("Priya", "priya@example.com")
print(priya.email)
print(priya.name)


class Instructor(Person):
    def __init__(self, name, subject):
        super().__init__(name)          # was: super().__init__()  (name not passed up)
        self.subject = subject


meera = Instructor("Meera", "Python")
print(meera.name, meera.subject)


class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes


class Course:                           # was: class Course(Lesson)  (a course is not a lesson)
    def __init__(self, title):
        self.title = title
        self.lessons = []

    def add(self, lesson):
        self.lessons.append(lesson)

    def total_minutes(self):
        total = 0
        for lesson in self.lessons:
            total += lesson.minutes
        return total


basics = Course("Python Basics")
basics.add(Lesson("Variables", 12))
basics.add(Lesson("Loops", 18))
print(isinstance(basics, Lesson))
print(basics.total_minutes())
```

Output (Python 3.14):

```text
priya@example.com
Priya
Meera Python
False
30
```

</details>


<details>
<summary><b>14 · Predict the output (__str__ and __repr__)</b></summary>

**Hint.** `print(x)`, `str(x)` and an f-string use `__str__` (the friendly text). Inside a list, with `!r` in an f-string, and for `repr(x)`, Python uses `__repr__` (the developer text). If a class has only `__repr__`, `str()` falls back to it.

Lines 1 and 4 show the friendly `Python Basics (Rs 499)`, because `print` and an f-string ask for `str`. A list never calls `__str__` on what it holds; it always shows the `repr` of each item, which is why line 3 shows `Course('Python Basics', 499)`, and line 5, an f-string with `!r`, asks for the `repr` on purpose. `Lesson` has no `__str__`, so `print(lesson)` and `str(lesson)` both fall back to its `__repr__`. A good `__repr__` looks like the code that would rebuild the object, and `!r` in the f-string puts quotes around text.

`solutions/Ex14.py`, run with `python Ex14.py`:

```python
# Exercise 14 - Predict the output (__str__ and __repr__)
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        return f"{self.title} (Rs {self.price})"

    def __repr__(self):
        return f"Course({self.title!r}, {self.price})"


class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes

    def __repr__(self):
        return f"Lesson({self.title!r}, {self.minutes})"


course = Course("Python Basics", 499)
lesson = Lesson("Loops", 18)
print(course)
print(repr(course))
print([course])
print(f"Now watching: {course}")
print(f"{course!r}")
print(lesson)
print(str(lesson))
print([lesson, lesson])
print("Lesson:", lesson)
```

Output (Python 3.14):

```text
Python Basics (Rs 499)
Course('Python Basics', 499)
[Course('Python Basics', 499)]
Now watching: Python Basics (Rs 499)
Course('Python Basics', 499)
Lesson('Loops', 18)
Lesson('Loops', 18)
[Lesson('Loops', 18), Lesson('Loops', 18)]
Lesson: Lesson('Loops', 18)
```

</details>


<details>
<summary><b>15 · Equal courses and sets</b></summary>

**Hint.** `==` calls `__eq__`. Return `NotImplemented` (not `False`) for a type you do not know, and Python will give a sensible answer. Whenever you define `__eq__` you must also define `__hash__`, and the hash should be built from the same field that `__eq__` compares: `hash(self.title)`.

`first is twin` stays `False`: they are two objects, and `==` now asks the question you taught it: same title? The price and lessons differ and do not matter. `!=` comes for free from `__eq__`. Returning `NotImplemented` makes `first == 5` come out `False` instead of crashing. Without `__hash__` Python marks the class unhashable (that exact `TypeError` is in Exercise 17), because equal objects must have equal hashes. The set keeps 2 items since `first` and `twin` collapse into one, and `sales[twin]` finds `first`'s value because both hash and `==` agree.

`solutions/Ex15.py`, run with `python Ex15.py`:

```python
# Exercise 15 - Equal courses and sets
class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons

    def __repr__(self):
        return f"Course({self.title!r}, {self.price})"

    def __eq__(self, other):
        if not isinstance(other, Course):
            return NotImplemented
        return self.title == other.title

    def __hash__(self):
        return hash(self.title)


first = Course("Python Basics", 499, ["Intro", "Loops"])
twin = Course("Python Basics", 399, ["Intro"])
other = Course("Loops Deep Dive", 299, ["while", "for"])

print(first == twin, first is twin)
print(first == other, first != other)
print(first == 5)

seen = {first, twin, other}
print(len(seen))

sales = {first: 3}
print(sales[twin])
print(twin in sales, other in sales)
```

Output (Python 3.14):

```text
True False
False True
False
2
3
True False
```

</details>


<details>
<summary><b>16 · A course that feels built-in</b></summary>

**Hint.** `len(x)` calls `x.__len__()`, a `for` loop calls `x.__iter__()` (return `iter(self.lessons)`), and `x[i]` calls `x.__getitem__(i)`. `sorted`, `min` and `max` only need `<`, so `__lt__` is enough. Inside `__lt__`, compare one number from each course.

With `__len__`, an object with no lessons is also falsy, so `bool(soon)` is `False` (empty things are falsy, as with lists). `in` works without a method of its own because Python falls back to looping with `__iter__`. Slices reach `__getitem__` too, and give back a list slice. The `key=` version in step 9 shows that `__lt__` is only the **default** order: you can still sort by something else whenever you like.

`solutions/Ex16.py`, run with `python Ex16.py`:

```python
# Exercise 16 - A course that feels built-in
class Course:
    def __init__(self, title, price, lessons):
        self.title = title
        self.price = price
        self.lessons = lessons

    def __str__(self):
        return f"{self.title} (Rs {self.price})"

    def __len__(self):
        return len(self.lessons)

    def __iter__(self):
        return iter(self.lessons)

    def __getitem__(self, index):
        return self.lessons[index]

    def __lt__(self, other):
        return self.price < other.price


basics = Course("Python Basics", 499, ["Intro", "Loops", "Lists"])
loops = Course("Loops Deep Dive", 299, ["while", "for"])
soon = Course("Coming Soon", 0, [])
data = Course("Data Structures", 899, ["List", "Dict"])

print(len(basics), len(loops))
print(bool(basics), bool(soon))
for lesson in basics:
    print(lesson)
print("Loops" in basics, "Dict" in basics)
print(basics[0], basics[-1], basics[:2])
print(list(loops))

for course in sorted([basics, loops, data]):
    print(course)
print(min(basics, loops, data))
print(max(basics, loops, data))

by_title = sorted([basics, loops, data], key=lambda c: c.title)
for course in by_title:
    print(course)
```

Output (Python 3.14):

```text
3 2
True False
Intro
Loops
Lists
True False
Intro Lists ['Intro', 'Loops']
['while', 'for']
Loops Deep Dive (Rs 299)
Python Basics (Rs 499)
Data Structures (Rs 899)
Loops Deep Dive (Rs 299)
Data Structures (Rs 899)
Data Structures (Rs 899)
Loops Deep Dive (Rs 299)
Python Basics (Rs 499)
```

</details>


<details>
<summary><b>17 · Fix the broken dunder code</b></summary>

**Hint.** `__str__` must return text, so build it with an f-string. The name is exactly two underscores, `str`, two underscores. In `__eq__`, check `isinstance(other, Course)` first and `return NotImplemented` otherwise. If you define `__eq__` you must also define `__hash__` to put objects in sets. Never change the field that feeds `__hash__` after the object is in a set or used as a dictionary key.

File b shows why a spelling mistake in a dunder name is dangerous: Python does not complain, it just never calls it, and falls back to the ugly default. File d is the rule from the lesson: defining `__eq__` quietly removes the default hash. File e is the quiet one: the hash was filed under the title `Python Basics`, you changed the title, and now the set looks in the wrong drawer, so the very same object is "not in" its own set. That is why hashes should come from fields that never change; the repaired version builds a new course for the new title, and a new course is correctly not found.

`solutions/Ex17.py`, run with `python Ex17.py`:

```python
# Exercise 17 - Fix the broken dunder code (all five repaired)
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):                  # was: return self.price  (a number, not text)
        return f"{self.title} (Rs {self.price})"

    def __eq__(self, other):            # was: no isinstance check (first == 5 crashed)
        if not isinstance(other, Course):
            return NotImplemented
        return self.title == other.title

    def __hash__(self):                 # was: missing, so a set of courses crashed
        return hash(self.title)


course = Course("Python Basics", 499)
print(course)                           # was: def __str_  (one underscore short)
print(course == 5)

basics = Course("Python Basics", 499)
seen = {basics, Course("Loops", 299)}
print(len(seen))

print(basics in seen)
renamed = Course("Python Advanced", 499)  # was: basics.title = "Python Advanced" on an object inside a set
print(renamed in seen)
```

Output (Python 3.14):

```text
Python Basics (Rs 499)
False
2
True
False
```

</details>


<details>
<summary><b>18 · Students, statuses and reports</b></summary>

**Hint.** Put `@dataclass` above the class and write the fields as `name: type` lines; Python writes `__init__`, `__repr__` and `__eq__` for you. A list default needs `field(default_factory=list)`, imported from `dataclasses`. `__post_init__` runs right after the generated `__init__`. A class that inherits from `ABC` and has an `@abstractmethod` cannot be built directly.

The dataclass prints itself as `Student(name='Asha', status=<Status.ACTIVE: 'active'>, ...)` without a single line of `__repr__` code. `default_factory=list` makes a **new** list per student (a plain `= []` is rejected, as in Exercise 20), so Lukas's `done` is empty although Asha's is not. The frozen `Lesson` cannot be changed after creation, and the check in `__post_init__` means a lesson with 0 minutes can never exist. `Report` is only a promise: every subclass must supply `render`, and building `Report()` itself fails with the real message you can read in the output.

`solutions/Ex18.py`, run with `python Ex18.py`:

```python
# Exercise 18 - Students, statuses and reports
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class Status(Enum):
    ACTIVE = "active"
    PAUSED = "paused"


@dataclass(frozen=True)
class Lesson:
    title: str
    minutes: int

    def __post_init__(self):
        if self.minutes <= 0:
            raise ValueError("minutes must be positive")


@dataclass
class Student:
    name: str
    status: Status = Status.ACTIVE
    done: list = field(default_factory=list)


class Report(ABC):
    @abstractmethod
    def render(self, student):
        pass


class ShortReport(Report):
    def render(self, student):
        return f"{student.name}: {len(student.done)} lessons"


class LongReport(Report):
    def render(self, student):
        text = f"{student.name} ({student.status.value}) finished:"
        for lesson in student.done:
            text = f"{text} {lesson.title}"
        return text


asha = Student("Asha")
lukas = Student("Lukas", Status.PAUSED)
asha.done.append(Lesson("Variables", 12))
asha.done.append(Lesson("Loops", 15))

print(asha)
print(lukas)
for status in Status:
    print(status.name, status.value)
for report in [ShortReport(), LongReport()]:
    print(report.render(asha))
print(ShortReport().render(lukas))

try:
    Lesson("Empty", 0)
except ValueError as error:
    print("Rejected:", error)

try:
    Report()
except TypeError as error:
    print("TypeError:", error)
```

Output (Python 3.14):

```text
Student(name='Asha', status=<Status.ACTIVE: 'active'>, done=[Lesson(title='Variables', minutes=12), Lesson(title='Loops', minutes=15)])
Student(name='Lukas', status=<Status.PAUSED: 'paused'>, done=[])
ACTIVE active
PAUSED paused
Asha: 2 lessons
Asha (active) finished: Variables Loops
Lukas: 0 lessons
Rejected: minutes must be positive
TypeError: Can't instantiate abstract class Report without an implementation for abstract method 'render'
```

</details>


<details>
<summary><b>19 · Predict the output (dataclass and Enum)</b></summary>

**Hint.** A dataclass writes `__repr__` and `__eq__` that look at **all** the fields (by value, not by identity). A plain dataclass that defines `__eq__` is not hashable. An Enum member prints as `Level.INTERMEDIATE`; `.name` is the label and `.value` the data. Members are compared with `==` to other members, and they are not numbers.

The generated `repr` lists every field, including the default `free=False`. `a == b` is `True` because all three fields match, but once `a.minutes` changes to 20 they differ. Putting `a` and `b` in a set fails, because the class has `__eq__` but no hash (the fix is `frozen=True`, see Exercise 18). For the Enum: `Level(3)` looks a member up by value and `Level["BEGINNER"]` by name, `for item in Level` walks them in order, and `len(Level)` counts three. `level == 2` is `False` because a member is not the number 2, and `<` between two members is a `TypeError`: compare `.value` when you need an order. `Level(9)` fails with a `ValueError` because no member has that value.

`solutions/Ex19.py`, run with `python Ex19.py`:

```python
# Exercise 19 - Predict the output (dataclass and Enum)
from dataclasses import dataclass
from enum import Enum


class Level(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


@dataclass
class Lesson:
    title: str
    minutes: int
    free: bool = False


print(Lesson("Variables", 12))
print(Lesson("Welcome", 3, True))
a = Lesson("Loops", 15, free=True)
b = Lesson("Loops", 15, True)
print(a == b, a is b)
a.minutes = 20
print(a == b, a)

try:
    done = {a, b}
except TypeError as error:
    print("TypeError:", error)

level = Level.INTERMEDIATE
print(level)
print(level.name, level.value)
print(Level(3), Level["BEGINNER"])
for item in Level:
    print(item.value, item.name)
print(len(Level))
print(level == Level.INTERMEDIATE, level == 2)

try:
    print(Level.BEGINNER < Level.ADVANCED)
except TypeError as error:
    print("TypeError:", error)

try:
    print(Level(9))
except ValueError as error:
    print("ValueError:", error)
```

Output (Python 3.14):

```text
Lesson(title='Variables', minutes=12, free=False)
Lesson(title='Welcome', minutes=3, free=True)
True False
False Lesson(title='Loops', minutes=20, free=True)
TypeError: cannot use 'Lesson' as a set element (unhashable type: 'Lesson')
Level.INTERMEDIATE
INTERMEDIATE 2
Level.ADVANCED Level.BEGINNER
1 BEGINNER
2 INTERMEDIATE
3 ADVANCED
3
True False
TypeError: '<' not supported between instances of 'Level' and 'Level'
ValueError: 9 is not a valid Level
```

</details>


<details>
<summary><b>20 · Fix the broken dataclass and abstract code</b></summary>

**Hint.** In a dataclass, fields without a default must come before fields with a default (file a). A list default needs `field(default_factory=list)` (file b). A frozen dataclass cannot be changed, so build a new object (file c). A subclass must define every abstract method with exactly the same name (file d). `@abstractmethod` only works when the class inherits from `ABC` (file e).

Files a and b are both guards that the dataclass runs while the class is being defined, so the errors appear even before you create an object. File d is a typo in a method name (`charge` instead of `pay`), now caught the moment you build the object instead of deep inside the program. File e is the quiet one: `@abstractmethod` without `ABC` is just a label, so the class builds happily. Make it `class Payment(ABC)` and `Payment()` fails with the message at the end of the goal output.

`solutions/Ex20.py`, run with `python Ex20.py`:

```python
# Exercise 20 - Fix the broken dataclass and abstract code (all five repaired)
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Lesson:
    title: str
    minutes: int                        # was: put after "free: bool = False"
    free: bool = False


print(Lesson("Variables", 12))


@dataclass
class Course:
    title: str
    lessons: list = field(default_factory=list)   # was: lessons: list = []


python = Course("Python")
sql = Course("SQL")
python.lessons.append("Variables")
print(python)
print(sql)


@dataclass(frozen=True)
class Tag:
    name: str


tag = Tag("python")
renamed = Tag("python-3")               # was: tag.name = "python-3"  (frozen)
print(tag, renamed)


class Payment(ABC):                     # was: class Payment:  (no ABC)
    @abstractmethod
    def pay(self, amount):
        pass


class CardPayment(Payment):
    def pay(self, amount):              # was: def charge(self, amount)
        print(f"Charged Rs {amount}")


CardPayment().pay(2499)

try:
    Payment()
except TypeError as error:
    print("TypeError:", error)
```

Output (Python 3.14):

```text
Lesson(title='Variables', minutes=12, free=False)
Course(title='Python', lessons=['Variables'])
Course(title='SQL', lessons=[])
Tag(name='python') Tag(name='python-3')
Charged Rs 2499
TypeError: Can't instantiate abstract class Payment without an implementation for abstract method 'pay'
```

</details>


---

**Score yourself:** 16-20 working programs means you are ready for the domain model build and Module 09. Under 12, rewatch the lesson named above the exercises you missed. Exercises 3, 6, 10, 13, 17 and 20 (reading errors and wrong output) and Exercises 2, 5, 9, 12, 14 and 19 (predicting) are the best practice for every module that follows.

## What next

In **Module 09 · Writing Pythonic Code** you will make objects you can loop over in a lazy way: iterators and generators, then closures and decorators that wrap functions, and context managers like the `with` blocks you used for files. The `__iter__` method from Exercise 16 is the door to all of it.
