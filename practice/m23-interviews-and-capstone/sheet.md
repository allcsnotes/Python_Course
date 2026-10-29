# Module 23 · Final Practice Sheet: 50 Interview Questions and 10 Build-It-Yourself Tasks

This is the last sheet of the course. **Part 1** is fifty questions that Python interviewers really ask, each with a model answer you can say out loud and a small program that proves it. **Part 2** is ten programs you build yourself, from a 30-line function to a service with a database and a cache. Everything uses what you learned in Modules 1 to 22.

## The 40 most-asked questions

Module 23, lesson one (*The Python Gotchas*) promised the full list of **the forty most-asked questions, each with a model answer**. They are **Q1 to Q40** in this sheet.
- **Q1 to Q18** are the eighteen questions from lesson one, in the same order and with the same wording as on its screen (Q1 to Q9 had a spoken answer, Q10 to Q18 were quick-fire). Each answer starts with the short line from the video, then goes deeper.
- **Q19 to Q40** are twenty-two more, grouped by topic.
- **G1 to G10** are the **ten gotchas** from lesson one, with the same code. Together with Q1 to Q40, that makes the **50 questions**.

If you are short of time, do Q1 to Q18 first, then the gotchas, then Q19 to Q40.

**How to work:**
- Use **Python 3.14** (check with `python --version`; on Mac or Linux the command may be `python3`).
- For Part 1, read a question, answer it **out loud in 30 seconds** (the interview is spoken, not typed), and only then open the answer. For code questions, predict the output first, then compare.
- Every program in Part 1 is a small file in the folder **`solutions/`**, named `Q01.py` to `Q40.py`, and `G01_default.py` to `G10_gil.py` for the gotchas. Every one was run with Python 3.14, and the output pasted here is the real output (where a traceback shows a file path, the folder part is shortened).
- A few programs use packages (pytest, pydantic, FastAPI, SQLAlchemy, psycopg, argon2-cffi, Redis, Hypothesis, uvicorn, httpx). Make a virtual environment inside the folder, as in Module 7: `python -m venv .venv`, activate it, and `pip install pytest hypothesis fastapi httpx sqlalchemy "psycopg[binary]" argon2-cffi redis uvicorn pydantic-settings`. Nothing is installed globally. Run `pytest` from inside `solutions/`: the small `pytest.ini` there lets each test import its own module. If Python prints a `StarletteDeprecationWarning` about `httpx`, it is only a warning; the outputs here were run with `python -W ignore`.
- A few programs need **Docker** (running): Postgres for Q34 to Q36 and tasks 9 and 10, Redis for Q37 and task 10. Start them once, and remove them at the end:

```text
docker run -d --name m23p04-pg -e POSTGRES_USER=practice -e POSTGRES_PASSWORD=practice -e POSTGRES_DB=practice -p 23604:5432 postgres:17
docker run -d --name m23p04-redis -p 23404:6379 redis:8
...
docker rm -f -v m23p04-pg m23p04-redis
```

- The cast is the usual one: Asha, Lukas, Priya and Meera, with **Rahul** as the interviewer. Money is written as **Rs**, in whole rupees.
- **Timing numbers change from machine to machine** (and from run to run). Where an output shows seconds, look at the *shape* (which is faster, and roughly by how much), not the exact digits. The same goes for the exact count in the race condition (Q17).
- Each question names the lesson where the course taught it, for example M05-L06 means Module 5, lesson 6. Where a question needs one small thing the course did not show, the answer says so.

---

# Part 1 · 50 Interview Questions

## All questions by topic

Pick a topic, answer the questions out loud, then open the answer in the next section. **Q** = one of the 40 most-asked; **G** = one of the ten gotchas. The **L01** column says where lesson one showed it.

### Language basics

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q11 | Is Python compiled or interpreted? | M01-L04 (what happens when you run Python) | question 11 |
| Q12 | try, except, else, finally? | M06-L03 (exceptions) | question 12 |
| Q14 | Does Python check type hints? | M10-L01 (type hints) | question 14 |
| Q19 | What is the difference between mutable and immutable objects? Give examples. | M05-L06 (names, objects and mutability) |  |
| Q20 | What counts as false in Python? When is `if x:` wrong and `if x is None:` right? | M02-L04 (True, False and None) |  |
| G3 | What is the difference between `is` and `==`? | M05-L06 (`is` and `==`) | gotcha 3 |
| G7 | Why does `0.1 + 0.2 == 0.3` give `False`? What do `//`, `%` and `round()` do? | M02-L02 (numbers) | gotcha 7 |

### Data structures

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q1 | What is the difference between a list and a tuple? | M05-L01 (lists) | question 1 |
| Q8 | Why must dictionary keys be hashable? | M05-L03 (dictionaries) | question 8 |
| Q21 | What is the difference between `sorted()` and `.sort()`? What does "stable" mean? | M05-L01 (lists: sort and sorted) |  |
| G4 | Explain shallow copy against deep copy. | M05-L06 (copying: `copy`, `deepcopy`, and the grid trap) | gotcha 4 |
| G5 | What goes wrong if you remove items from a list while looping over it? | M05-L03 (dictionary changed size) | gotcha 5 |
| G6 | What happens when you run `+=` on a list inside a tuple? | M05-L02 (tuples) | gotcha 6 |

### Functions, closures and decorators

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q2 | What is a decorator? | M09-L03 (closures and decorators) | question 2 |
| Q6 | What are *args and **kwargs? | M04-L03 (args and kwargs) | question 6 |
| Q22 | Explain scope: what can a function see? When do you need `global` and `nonlocal`? | M04-L04 (scope) |  |
| Q23 | How do you write a decorator that takes arguments, such as `@retry(times=3)`? | M09-L03 (decorators) |  |
| Q24 | How do recursion and the recursion limit work? How does `functools.cache` help? | M04-L05 (recursion and lambdas, the recursion limit) |  |
| G1 | What is the mutable default argument trap? | M04-L02 (parameters) | gotcha 1 |
| G2 | What does a list of lambdas made in a loop give when you call them? How do you fix it? | M09-L03 (closures, pitfall three) | gotcha 2 |

### Object-oriented programming

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q9 | What are instance, class and static methods? | M08-L02 (methods) | question 9 |
| Q15 | Data class or normal class? | M08-L06 (dataclasses, enums and abstract classes) | question 15 |
| Q25 | What is the MRO? How does `super()` work with multiple inheritance? | M08-L04 (inheritance and composition, lookup order, `super()`) |  |
| Q26 | What do `__repr__`, `__str__`, `__eq__` and `__hash__` do? How are they connected? | M08-L05 (dunder methods) |  |
| Q27 | What is a property? Why not make every attribute private with getters and setters? | M08-L03 (encapsulation and properties) |  |
| G8 | What is the difference between a class attribute and an instance attribute? | M08-L02 (attributes and methods) | gotcha 8 |

### Iterators and generators

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q3 | What is a generator, and why use one? | M09-L02 (generators) | question 3 |
| Q7 | What does a with statement do? | M09-L04 (context managers) | question 7 |
| Q28 | What is the difference between an iterable and an iterator? | M09-L01 (iterables and iterators) |  |

### Memory, the GIL and performance

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q5 | How does Python free memory? | M11-L02 (memory and garbage collection) | question 5 |
| Q29 | How do you find out why code is slow, and what do you try first? | M11-L04 (measuring and improving speed) |  |
| G9 | What does `__slots__` do? | M10-L03 (TypedDict, slots, NamedTuple and pattern matching) | gotcha 9 |
| G10 | What is the GIL? Do Python threads speed up CPU work? | M11-L03 (the GIL and free-threaded Python) | gotcha 10 |

### Concurrency

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q4 | Threads, processes or async? | M12-L01 (CPU-bound against IO-bound) | question 4 |
| Q17 | What is a race condition? | M12-L02 (threads, locks and races) | question 17 |

### Testing

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q16 | Fixture or mock? | M13-L02 (fixtures and parametrize) | question 16 |
| Q30 | What makes a good test? How do coverage and property-based tests help? | M13-L01 (first tests) |  |

### Packaging and project structure

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q10 | What does `if __name__ == "__main__"` do? | M07-L01 (splitting code into modules) | question 10 |
| Q13 | Why a virtual environment? | M07-L03 (virtual environments and uv projects) | question 13 |

### Web and backend

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q31 | How does FastAPI validate input? What is `Depends`, and how do you replace a dependency in tests? | M15-L03 (pydantic models) |  |
| Q32 | Which status codes would you return, and how do you make a POST safe to retry? | M15-L02 (parameters, bodies and responses) |  |
| Q33 | Should an endpoint be `def` or `async def`? | M15-L06 (async endpoints, background tasks and docs) |  |

### Databases and caching

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q34 | What is the N+1 query problem and how do you fix it? | M16-L03 (relationships and the N+1 problem) |  |
| Q35 | What is a transaction? What do ACID and rollback mean? | M16-L04 (migrations with Alembic and transactions) |  |
| Q36 | What is an index? When does it help and what does it cost? | M16-L01 (SQL and PostgreSQL) |  |
| Q37 | What is cache-aside? How do you keep a cache from serving stale data? | M18-L01 (Redis and caching) |  |

### Security

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q18 | How do you store passwords? | M17-L01 (passwords done right) | question 18 |
| Q38 | What is SQL injection and how do you prevent it? | M17-L04 (input attacks and secrets) |  |

### Deployment and operations

| # | Question | Taught in | L01 |
|---|---|---|---|
| Q39 | How do you package a Python service in Docker, and how do you configure it per environment? | M19-L01 (Docker for Python apps) |  |
| Q40 | What do you log and measure in production? What is a request ID? | M14-L03 (logging the right way) |  |

---

## Answers

Click a question to open its answer. Say your own answer first. A good answer has a short rule, one example, and the trap to avoid.

### Q1 to Q18 · The eighteen from lesson one

<details>
<summary><b>Q1 · What is the difference between a list and a tuple?</b> <i>(Data structures)</i></summary>

**Taught in:** M05-L01 (lists); M05-L02 (tuples and unpacking); M23-L01 question 1.

**In one breath (lesson one):** A list can change, a tuple cannot. Because a tuple cannot change, it can be a dictionary key, as long as everything inside it can be hashed. I use a tuple for a small fixed record, and a list for a collection that grows.

**Fuller answer.** A list can grow, shrink and change; a tuple cannot. Because a tuple cannot change, it can be a dictionary key or a set member, as long as everything inside it is hashable. I use a tuple for a small fixed record (a seat `("A", 1)`, a point `(3, 4)`) and a list for a collection that grows. Tuples also give clean unpacking: `first, *middle, last = items`, and swapping with `a, b = b, a`.

`solutions/Q01.py`:

```python
# Q01 - List vs tuple
seats = {("A", 1): "Asha", ("A", 2): "Lukas"}   # tuples can be dict keys
print(seats[("A", 2)])
try:
    {["A", 1]: "Priya"}
except TypeError as error:
    print("TypeError:", error)

city, country = "Frankfurt", "Germany"           # packing and unpacking
city, country = country, city                    # swap, no temp variable
print(city, country)

first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)
```

Run it: `python Q01.py`.

Output (Python 3.14):

```text
Lukas
TypeError: cannot use 'list' as a dict key (unhashable type: 'list')
Germany Frankfurt
1 [2, 3, 4] 5
```

**Rahul's follow-up:** *Is a tuple always hashable?* No. `([1], 2)` holds a list, and hashing it raises `TypeError`. A tuple is hashable only when all its items are.

</details>


<details>
<summary><b>Q2 · What is a decorator?</b> <i>(Functions, closures and decorators)</i></summary>

**Taught in:** M09-L03 (closures and decorators); M23-L01 question 2.

**In one breath (lesson one):** A function that takes a function and returns a new one, usually a wrapper that adds behavior before or after the call. The @ sign above a def is shorthand for `name = decorator(name)`. I put functools.wraps on the wrapper, to keep the original name.

**Fuller answer.** A decorator is a function that takes a function and returns a new one, usually a wrapper that adds behaviour before or after the call. The line `@timed` above a `def` is shorthand for `name = timed(name)`. The wrapper takes `*args, **kwargs` so it works for any function, and I put `@functools.wraps(func)` on it, which copies the original `__name__` and docstring. Without `wraps`, every decorated function is called `wrapper`, which confuses logs, tracebacks and tools.

`solutions/Q02.py`:

```python
# Q02 - A decorator that keeps the original name
import functools
import time

def timed_plain(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

def timed(func):
    @functools.wraps(func)          # copies __name__, __doc__ and more
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

@timed_plain
def a():
    "Adds."
    return 1

@timed
def b():
    "Adds."
    return 1

print(a.__name__, a.__doc__)
print(b.__name__, b.__doc__)
b()
```

Run it: `python Q02.py`.

Output (Python 3.14):

```text
wrapper None
b Adds.
b took 0.000s
```

**Rahul's follow-up:** *Why does the wrapper return the result of `func(...)`?* Otherwise the decorated function would always return `None`. A common bug.

</details>


<details>
<summary><b>Q3 · What is a generator, and why use one?</b> <i>(Iterators and generators)</i></summary>

**Taught in:** M09-L02 (generators); M23-L01 question 3.

**In one breath (lesson one):** A function with yield. It makes one value at a time, when you ask, so it uses almost no memory, even for a huge or endless stream. The price: you can walk through it only once.

**Fuller answer.** A generator is a function with `yield`. Calling it does not run the body; it gives you an iterator. Each `next()` runs the body until the next `yield`, hands out one value and pauses with its local variables intact. It makes one value at a time, so it needs almost no memory, even for a huge or endless stream: in the example the list of a million squares takes about 8 MB and the generator 208 bytes. The price is that you can walk through it only once. Generators chain well into pipelines: read lines, parse, filter, count.

`solutions/Q03.py`:

```python
# Q03 - Generators
import sys

def squares(limit):
    for n in range(limit):
        yield n * n                 # pauses here, resumes on the next call

gen = squares(3)
print(next(gen), next(gen), next(gen))
print(list(squares(5)))

as_list = [n * n for n in range(1_000_000)]
as_gen = (n * n for n in range(1_000_000))
print("list bytes:", sys.getsizeof(as_list), "| generator bytes:", sys.getsizeof(as_gen))
print(sum(as_gen))                  # still gives the full answer, one item at a time
print(sum(as_gen))                  # but a generator can be used only once

def first_words(lines):             # a lazy pipeline stage
    for line in lines:
        yield line.split()[0]

print(list(first_words(["python is fun", "sql is old", "rust is new"])))
```

Run it: `python Q03.py`.

Output (Python 3.14):

```text
0 1 4
[0, 1, 4, 9, 16]
list bytes: 8448728 | generator bytes: 208
333332833333500000
0
['python', 'sql', 'rust']
```

**Rahul's follow-up:** *What does `yield from` do?* It hands every item of another iterable out, one by one, in a single line (module nine, lesson two).

</details>


<details>
<summary><b>Q4 · Threads, processes or async?</b> <i>(Concurrency)</i></summary>

**Taught in:** M12-L01 (CPU-bound against IO-bound); M12-L02 (threads); M12-L03 (processes); M12-L04 and M12-L05 (asyncio); M23-L01 question 4.

**In one breath (lesson one):** First I ask what the program waits for. If it waits for the network or a disk, threads or async help. If it computes, then with the normal GIL, processes help. And I measure before I choose.

**Fuller answer.** First ask what the program waits for. If it waits for the network or a disk (IO-bound), threads or asyncio let other work run meanwhile: ten half-second waits finish in half a second. If it computes (CPU-bound), the GIL means processes are the answer. asyncio is the cheapest for thousands of waits, but it needs `await`-able libraries. One blocking call such as `time.sleep` or a slow library call inside an `async def` stops *every* task, as the example shows (1.5 s instead of 0.3 s). Fix it with an async version or `asyncio.to_thread`. And I measure before I choose.

`solutions/Q04.py`:

```python
# Q04 - Threads, processes or asyncio? And what freezes an event loop
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def wait_io(_):                     # IO-bound: waiting for the network
    time.sleep(0.5)

def burn(n):                        # CPU-bound: calculating
    return sum(i * i for i in range(n))

async def wait_async(_):
    await asyncio.sleep(0.5)

async def many():
    await asyncio.gather(*(wait_async(i) for i in range(10)))

async def blocking_one(_):
    time.sleep(0.3)                 # BAD inside async: nobody else can run

async def thread_one(_):
    await asyncio.to_thread(time.sleep, 0.3)    # fix: hand it to a worker thread

async def five(fn):
    await asyncio.gather(*(fn(i) for i in range(5)))

def timed(label, fn):
    start = time.perf_counter()
    fn()
    print(f"{label:<34}{time.perf_counter() - start:5.2f}s")

if __name__ == "__main__":
    timed("10 waits, one after another", lambda: [wait_io(i) for i in range(10)])
    with ThreadPoolExecutor(10) as pool:
        timed("10 waits, 10 threads", lambda: list(pool.map(wait_io, range(10))))
    timed("10 waits, asyncio.gather", lambda: asyncio.run(many()))
    with ProcessPoolExecutor(4) as pool:
        list(pool.map(burn, [10] * 4))          # warm up the workers first
        timed("4 CPU jobs, 4 processes", lambda: list(pool.map(burn, [3_000_000] * 4)))
    timed("4 CPU jobs, one process", lambda: [burn(3_000_000) for _ in range(4)])
    timed("5 x time.sleep inside async", lambda: asyncio.run(five(blocking_one)))
    timed("5 x asyncio.to_thread", lambda: asyncio.run(five(thread_one)))
```

Run it: `python Q04.py`.

Output (Python 3.14):

```text
10 waits, one after another        5.04s
10 waits, 10 threads               0.51s
10 waits, asyncio.gather           0.50s
4 CPU jobs, 4 processes            0.32s
4 CPU jobs, one process            0.89s
5 x time.sleep inside async        1.53s
5 x asyncio.to_thread              0.31s
```

**Rahul's follow-up:** *How do you limit how many requests run at once in asyncio?* An `asyncio.Semaphore` (module twelve, lesson five).

</details>


<details>
<summary><b>Q5 · How does Python free memory?</b> <i>(Memory, the GIL and performance)</i></summary>

**Taught in:** M11-L02 (memory and garbage collection); M23-L01 question 5.

**In one breath (lesson one):** By reference counting: an object is freed the moment its last pointer goes. A cycle collector catches objects that only point at each other. And a leak is something that still points at an object, like a cache that only grows.

**Fuller answer.** CPython counts references. An object is freed the moment its last reference goes (`del`, or the label moves on). Reference counting cannot free objects that only point at each other, so a cycle collector runs now and then (`gc.collect()` runs it on demand). A "leak" in Python is usually something that still points at an object: a cache or list that only grows, a global, a forgotten callback. A `weakref` points at an object without keeping it alive. `tracemalloc` shows where memory goes.

`solutions/Q05.py`:

```python
# Q05 - Reference counting and the cycle collector
import gc
import sys
import weakref

class Box:
    pass

box = Box()
print(sys.getrefcount(box) - 1)     # minus the temporary reference of the call
other = box
print(sys.getrefcount(box) - 1)
del other
print(sys.getrefcount(box) - 1)

alive = weakref.ref(box)
del box                             # count hits 0: freed at once
print("alive after del:", alive() is not None)

a, b = Box(), Box()
a.other, b.other = b, a             # a cycle: counts can never reach 0
probe = weakref.ref(a)
del a, b
print("alive after del (cycle):", probe() is not None)
gc.collect()
print("alive after gc.collect():", probe() is not None)
```

Run it: `python Q05.py`.

Output (Python 3.14):

```text
1
2
1
alive after del: False
alive after del (cycle): True
alive after gc.collect(): False
```

**Rahul's follow-up:** *How would you find a leak?* Take two `tracemalloc` snapshots a while apart and compare them to see which lines allocate memory that never goes away.

</details>


<details>
<summary><b>Q6 · What are *args and **kwargs?</b> <i>(Functions, closures and decorators)</i></summary>

**Taught in:** M04-L03 (args and kwargs); M23-L01 question 6.

**In one breath (lesson one):** In a definition, *args collects extra positional values into a tuple, and **kwargs collects extra named values into a dictionary. In a call, the stars do the opposite: they unpack.

**Fuller answer.** In a definition, `*args` collects extra positional values into a tuple and `**kwargs` collects extra named values into a dictionary. In a call, the stars do the opposite: `f(*args, **kwargs)` unpacks a tuple and a dictionary into arguments. Parameters after a `*` can only be given by name (keyword-only), and a `/` marks the ones before it as positional-only; these two small markers are an extra beyond the lesson, and the example shows both.

`solutions/Q06.py`:

```python
# Q06 - *args, **kwargs, keyword-only and positional-only
def enroll(student, /, course, *tags, level="beginner", **extra):
    return student, course, tags, level, extra

print(enroll("Asha", "Python"))
print(enroll("Asha", "Python", "video", "live", level="advanced", city="Pune"))

args = ("Lukas", "SQL")
kwargs = {"level": "intermediate"}
print(enroll(*args, **kwargs))       # unpack a tuple and a dict into a call

try:
    enroll(student="Asha", course="Python")
except TypeError as error:
    print("TypeError:", error)
```

Run it: `python Q06.py`.

Output (Python 3.14):

```text
('Asha', 'Python', (), 'beginner', {})
('Asha', 'Python', ('video', 'live'), 'advanced', {'city': 'Pune'})
('Lukas', 'SQL', (), 'intermediate', {})
TypeError: enroll() missing 1 required positional argument: 'student'
```

**Rahul's follow-up:** *Where do you use `*args, **kwargs` in practice?* In decorators and wrappers that must pass any call straight through to the wrapped function (module nine, lesson three).

</details>


<details>
<summary><b>Q7 · What does a with statement do?</b> <i>(Iterators and generators)</i></summary>

**Taught in:** M09-L04 (context managers); M23-L01 question 7.

**In one breath (lesson one):** It runs setup when the block starts, and cleanup when the block ends, even if an error happens. Files, locks and database sessions use it, and you can write your own with `__enter__` and `__exit__`.

**Fuller answer.** `with` runs setup when the block starts and cleanup when it ends, *even if an error happens*. Files, locks and database sessions use it. You write your own in two ways: a class with `__enter__` and `__exit__`, or a generator function marked `@contextlib.contextmanager` with `try: yield ... finally: cleanup`. If `__exit__` returns a true value it swallows the error; normally it returns `False`. `contextlib.suppress` is the short way to ignore one named error.

`solutions/Q07.py`:

```python
# Q07 - Context managers
from contextlib import contextmanager, suppress

class Timer:
    def __enter__(self):
        print("start")
        return self
    def __exit__(self, exc_type, exc, tb):
        print("stop, error was:", exc_type.__name__ if exc_type else None)
        return False                # False: do not swallow the error

with Timer():
    print("working")

try:
    with Timer():
        1 / 0
except ZeroDivisionError:
    print("the error still came out")

@contextmanager
def tag(name):
    print(f"<{name}>")
    try:
        yield
    finally:                        # runs even when the body fails
        print(f"</{name}>")

with tag("p"):
    print("hello")

with suppress(FileNotFoundError):
    open("no-such-file.txt")
print("carried on")
```

Run it: `python Q07.py`.

Output (Python 3.14):

```text
start
working
stop, error was: None
start
stop, error was: ZeroDivisionError
the error still came out
<p>
hello
</p>
carried on
```

**Rahul's follow-up:** *Why is `with open(...)` better than calling `close()` yourself?* If an error happens before `close()`, the file stays open. `with` always closes it.

</details>


<details>
<summary><b>Q8 · Why must dictionary keys be hashable?</b> <i>(Data structures)</i></summary>

**Taught in:** M05-L03 (dictionaries); M05-L04 (sets); M09-L05 (hashable); M23-L01 question 8.

**In one breath (lesson one):** A dictionary finds a key through its hash, a number made from the value. If the value could change, the number would change, and Python would look in the wrong place. So lists cannot be keys, but tuples of numbers and text can.

**Fuller answer.** A dictionary finds a value through the *hash* of its key, a number made from the key's value, so a lookup takes the same short time whatever the size (average constant time). If a key could change, its hash would change and Python would look in the wrong place, so lists cannot be keys, but tuples of numbers and text can. Since Python 3.7, a dictionary keeps insertion order. A set uses the same hash idea with keys only: fast `in` tests, removing duplicates, and the operations `&`, `|`, `-` and `^`. `list(dict.fromkeys(items))` removes duplicates *and* keeps the order.

`solutions/Q08.py`:

```python
# Q08 - How dicts and sets work
scores = {"Asha": 90, "Lukas": 72}
scores["Priya"] = 85
print(list(scores))                 # insertion order is guaranteed
print(scores.get("Meera"), scores.get("Meera", 0))
try:
    scores["Meera"]
except KeyError as error:
    print("KeyError:", error)

counts = {}
for word in "to be or not to be".split():
    counts[word] = counts.get(word, 0) + 1
print(counts)

print({**scores, "Lukas": 80} | {"Mia": 60})   # merge, last one wins
print(hash("abc") == hash("abc"), hash((1, 2)) == hash((1, 2)))

# sets: the same hash idea, keys only
import timeit

names = ["Asha", "Lukas", "Asha", "Priya", "Lukas"]
print(list(dict.fromkeys(names)))   # remove duplicates, keep the order
python = {"Asha", "Lukas", "Priya"}
sql = {"Priya", "Meera"}
print(python & sql, sorted(python | sql), sorted(python - sql), sorted(python ^ sql))

big_list = list(range(100_000))
big_set = set(big_list)
t_list = timeit.timeit(lambda: 99_999 in big_list, number=200)
t_set = timeit.timeit(lambda: 99_999 in big_set, number=200)
print("set lookup is faster:", t_set < t_list)
```

Run it: `python Q08.py`.

Output (Python 3.14):

```text
['Asha', 'Lukas', 'Priya']
None 0
KeyError: 'Meera'
{'to': 2, 'be': 2, 'or': 1, 'not': 1}
{'Asha': 90, 'Lukas': 80, 'Priya': 85, 'Mia': 60}
True True
['Asha', 'Lukas', 'Priya']
{'Priya'} ['Asha', 'Lukas', 'Meera', 'Priya'] ['Asha', 'Lukas'] ['Asha', 'Lukas', 'Meera']
set lookup is faster: True
```

**Rahul's follow-up:** *What is the time cost of `x in a_list` against `x in a_set`?* The list checks items one by one (linear time). The set hashes once (average constant time). That difference grows with the data.

</details>


<details>
<summary><b>Q9 · What are instance, class and static methods?</b> <i>(Object-oriented programming)</i></summary>

**Taught in:** M08-L02 (methods); M09-L03 (`classmethod` as a decorator); M23-L01 question 9.

**In one breath (lesson one):** An instance method gets self, one object. A class method gets cls, the class itself, and is often a second way to build an object. A static method gets neither: it is a plain function that lives in the class.

**Fuller answer.** An instance method gets `self`, the one object. A class method, marked `@classmethod`, gets `cls`, the class itself, and is often a second way to build an object (`Course.from_text("SQL,399")`). Because it receives `cls`, a subclass that inherits it builds an object of the subclass. A static method gets neither: it is a plain function that happens to live in the class because it belongs with it.

`solutions/Q09.py`:

```python
# Q09 - Instance, class and static methods
class Course:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def describe(self):             # needs the object
        return f"{self.title} costs Rs {self.price}"

    @classmethod
    def from_text(cls, text):       # needs the class: an alternative constructor
        title, price = text.split(",")
        return cls(title, int(price))

    @staticmethod
    def is_valid_price(price):      # needs neither
        return price >= 0

print(Course.from_text("SQL,399").describe())
print(Course.is_valid_price(-5))

class Premium(Course):
    pass

print(type(Premium.from_text("Rust,999")).__name__)   # cls follows the subclass
```

Run it: `python Q09.py`.

Output (Python 3.14):

```text
SQL costs Rs 399
False
Premium
```

**Rahul's follow-up:** *When would you pick a module-level function over a static method?* Almost always. A static method adds nothing a plain function does not, except grouping.

</details>


<details>
<summary><b>Q10 · What does `if __name__ == "__main__"` do?</b> <i>(Packaging and project structure)</i></summary>

**Taught in:** M07-L01 (splitting code into modules); M07-L02 (packages, circular imports); M23-L01 question 10.

**In one breath (lesson one):** It runs code only when the file is started directly, not when it is imported.

**Fuller answer.** When a file is run directly, Python sets its `__name__` to `"__main__"`. When it is imported, `__name__` is the module's name. The guard therefore runs code only when the file is started directly, not when it is imported. A circular import is two modules that import each other at the top: the second `import` meets a half-built module and fails with `cannot import name ... (most likely due to a circular import)`. Fix it by moving shared code into a third module, or by importing inside the function that needs it; best of all, rethink which module should depend on which.

`solutions/Q10.py`:

```python
# Q10 - __name__ == "__main__" and circular imports
import sys
import tempfile
from pathlib import Path

print("this file's __name__ is", __name__)

def main():
    print("main() runs only when the file is run directly")

if __name__ == "__main__":
    main()

with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    (root / "orders.py").write_text("from billing import charge\ndef place(): return charge()\n")
    (root / "billing.py").write_text("from orders import place\ndef charge(): return 'charged'\n")
    (root / "billing_ok.py").write_text("def charge():\n    from orders_ok import place   # imported when needed\n    return 'charged'\n")
    (root / "orders_ok.py").write_text("from billing_ok import charge\ndef place(): return charge()\n")
    sys.path.insert(0, folder)
    try:
        import orders
    except ImportError as error:
        print("ImportError:", str(error).split(" (")[0])
    import orders_ok
    print("fixed:", orders_ok.place())
```

Run it: `python Q10.py`.

Output (Python 3.14):

```text
this file's __name__ is __main__
main() runs only when the file is run directly
ImportError: cannot import name 'place' from partially initialized module 'orders'
fixed: charged
```

**Rahul's follow-up:** *How do you run a package's module with its imports intact?* Use `python -m package.module` from the project root, so Python sets up the package path.

</details>


<details>
<summary><b>Q11 · Is Python compiled or interpreted?</b> <i>(Language basics)</i></summary>

**Taught in:** M01-L04 (what happens when you run Python); M11-L04; M23-L01 quick-fire 11.

**In one breath (lesson one):** Both. It compiles to bytecode, and a virtual machine runs the bytecode.

**Fuller answer.** Both. CPython first compiles your source into bytecode, a list of small instructions for a virtual machine, and then the virtual machine runs those instructions one by one. That is why Python needs no separate compile step from you, and why imported modules leave `.pyc` files in `__pycache__`. "Interpreted" is about the second step. Other implementations, such as PyPy, add a just-in-time compiler.

`solutions/Q11.py`:

```python
# Q11 - Compiled or interpreted?
import dis

source = "total = price * 2 + tax"
code = compile(source, "<demo>", "exec")      # step 1: source text -> bytecode
print(type(code).__name__, code.co_names)
dis.dis(code)                                 # step 2 happens in the virtual machine
exec(code, {"price": 100, "tax": 18})         # the VM runs the bytecode
```

Run it: `python Q11.py`.

Output (Python 3.14):

```text
code ('price', 'tax', 'total')
  0           RESUME                   0

  1           LOAD_NAME                0 (price)
              LOAD_SMALL_INT           2
              BINARY_OP                5 (*)
              LOAD_NAME                1 (tax)
              BINARY_OP                0 (+)
              STORE_NAME               2 (total)
              LOAD_CONST               1 (None)
              RETURN_VALUE
```

**Rahul's follow-up:** *Why is Python slower than C?* Each bytecode instruction is run by the virtual machine, which must check types at run time. The price is flexibility. When speed matters you measure first, then use better algorithms, NumPy or a process pool (module eleven).

</details>


<details>
<summary><b>Q12 · try, except, else, finally?</b> <i>(Language basics)</i></summary>

**Taught in:** M06-L03 (exceptions); M06-L04 (raising and designing errors); M23-L01 quick-fire 12.

**In one breath (lesson one):** Except handles the error. Else runs when there was none. Finally always runs.

**Fuller answer.** `try` holds the code that may fail. `except` handles a named error. `else` runs only when the `try` block had no error, which keeps the success path out of the protected block. `finally` always runs, even after a `return` or an unhandled error, so it is the place for cleanup. To turn one error into another without losing the story, write `raise NewError(...) from error`; the original stays on `__cause__`.

`solutions/Q12.py`:

```python
# Q12 - try, except, else, finally
def parse(text):
    try:
        number = int(text)
    except ValueError:
        print("  except: not a number")
        return None
    else:
        print("  else: no error happened")
        return number
    finally:
        print("  finally: always runs")

print(parse("42"))
print(parse("forty-two"))

def which():
    try:
        return "from try"
    finally:
        print("  finally still runs before the function returns")

print(which())

try:
    try:
        1 / 0
    except ZeroDivisionError as error:
        raise ValueError("bad input") from error      # keep the original as the cause
except ValueError as error:
    print(repr(error), "| cause:", repr(error.__cause__))
```

Run it: `python Q12.py`.

Output (Python 3.14):

```text
  else: no error happened
  finally: always runs
42
  except: not a number
  finally: always runs
None
  finally still runs before the function returns
from try
ValueError('bad input') | cause: ZeroDivisionError('division by zero')
```

**Rahul's follow-up:** *Should you write a bare `except:`?* No. It also catches `KeyboardInterrupt` and hides real bugs. Catch the specific errors you can handle, and let the rest travel up.

</details>


<details>
<summary><b>Q13 · Why a virtual environment?</b> <i>(Packaging and project structure)</i></summary>

**Taught in:** M07-L03 (virtual environments and uv projects); M07-L04 (PyPI); M23-L01 question 13.

**In one breath (lesson one):** Each project gets its own packages and versions, so projects never fight.

**Fuller answer.** Each project gets its own folder of installed packages and its own versions, so project A can use version 1 of a library while project B uses version 2, and nothing is installed globally. A virtual environment is just a folder with its own Python and its own `site-packages`; the example shows that a fresh one holds only `pip`. A lock file (`uv.lock`) records the exact versions of every package, direct and indirect, so a teammate or the CI server installs exactly what you tested.

`solutions/Q13.py`:

```python
# Q13 - Why a virtual environment
import subprocess
import sys
import tempfile
from pathlib import Path

print("running in a venv:", sys.prefix != sys.base_prefix)

with tempfile.TemporaryDirectory() as folder:
    env = Path(folder) / "demo-env"
    subprocess.run([sys.executable, "-m", "venv", str(env)], check=True)
    python = env / "bin" / "python"
    check = "import sys, importlib.metadata as m; print(sys.prefix != sys.base_prefix, sorted(d.name for d in m.distributions()))"
    out = subprocess.run([python, "-c", check], capture_output=True, text=True, check=True)
    print("fresh venv  :", out.stdout.strip())
    print("has its own site-packages:", (env / "lib").exists())
```

Run it: `python Q13.py`.

Output (Python 3.14):

```text
running in a venv: True
fresh venv  : True ['pip']
has its own site-packages: True
```

**Rahul's follow-up:** *What goes in version control: the `.venv` folder or the lock file?* The lock file and `pyproject.toml`. The virtual environment is rebuilt from them, so it goes in `.gitignore`.

</details>


<details>
<summary><b>Q14 · Does Python check type hints?</b> <i>(Language basics)</i></summary>

**Taught in:** M10-L01 (type hints); M10-L02 (pyright); M15-L03 (pydantic); M23-L01 quick-fire 14.

**In one breath (lesson one):** No. A checker like pyright does, before the program runs. Pydantic and FastAPI use them while it runs.

**Fuller answer.** Not at run time. Python stores the hints and ignores them, so `double("ha")` runs and returns `"haha"`. A checker such as pyright reads them *before* the program runs and finds mistakes without running the code. Libraries such as pydantic and FastAPI read the hints *while* the program runs, to validate and convert input.

`solutions/Q14.py`:

```python
# Q14 - Does Python check type hints?
from pydantic import TypeAdapter, ValidationError


def double(x: int) -> int:
    return x * 2

print(double("ha"))                 # no error: Python ignores hints while running
print(double.__annotations__)       # they are just stored

try:                                # pydantic USES hints, at run time
    TypeAdapter(int).validate_python("abc")
except ValidationError as error:
    print("pydantic:", error.errors()[0]["msg"])

print(TypeAdapter(int).validate_python("42") + 1)   # and converts safe text for you
```

Run it: `python Q14.py`.

Output (Python 3.14):

```text
haha
{'x': <class 'int'>, 'return': <class 'int'>}
pydantic: Input should be a valid integer, unable to parse string as an integer
43
```

**Rahul's follow-up:** *Then why write hints at all?* They document intent, power the editor's autocomplete and the checker, and catch a whole class of bugs in CI before users see them.

</details>


<details>
<summary><b>Q15 · Data class or normal class?</b> <i>(Object-oriented programming)</i></summary>

**Taught in:** M08-L06 (dataclasses, enums and abstract classes); M23-L01 quick-fire 15.

**In one breath (lesson one):** A data class writes init, repr and eq for you, so it suits a class that mostly holds data.

**Fuller answer.** A dataclass writes `__init__`, `__repr__` and `__eq__` for you from the field list, so it suits a class that mostly holds data. `frozen=True` makes objects unchangeable (and hashable), `slots=True` saves memory, and a mutable default needs `field(default_factory=list)`. An abstract class (`ABC` with `@abstractmethod`) is a contract: it cannot be created itself, and a subclass must implement every abstract method before it can be created. That moves a missing method from a surprise at run time to an error at the moment of creation.

`solutions/Q15.py`:

```python
# Q15 - Dataclasses and abstract classes
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Lesson:
    title: str
    minutes: int = 10
    tags: tuple = ()

@dataclass
class Course:
    title: str
    lessons: list[Lesson] = field(default_factory=list)   # never = []

l = Lesson("Loops", 20)
print(l, l == Lesson("Loops", 20))
try:
    l.minutes = 5
except Exception as error:
    print(type(error).__name__ + ":", error)

class Payment(ABC):
    @abstractmethod
    def pay(self, amount): ...

class Card(Payment):
    def pay(self, amount):
        print(f"Charged Rs {amount}")

Card().pay(499)
try:
    Payment()
except TypeError as error:
    print("TypeError:", error)
```

Run it: `python Q15.py`.

Output (Python 3.14):

```text
Lesson(title='Loops', minutes=20, tags=()) True
FrozenInstanceError: cannot assign to field 'minutes'
Charged Rs 499
TypeError: Can't instantiate abstract class Payment without an implementation for abstract method 'pay'
```

**Rahul's follow-up:** *Dataclass or `NamedTuple`?* A `NamedTuple` is immutable, tuple-like and light (module ten, lesson three). A dataclass is more flexible: methods, defaults, optional mutability.

</details>


<details>
<summary><b>Q16 · Fixture or mock?</b> <i>(Testing)</i></summary>

**Taught in:** M13-L02 (fixtures and parametrize); M13-L03 (mocking).

**In one breath (lesson one):** A fixture prepares what a test needs. A mock replaces something the test must not really call.

**Fuller answer.** A fixture *prepares* what a test needs: a database, a client, a sample object. A test asks for it by naming it as a parameter, and pytest builds it fresh for each test, so tests do not leak state into each other. `@pytest.mark.parametrize` runs one test for many input rows, and each row is reported as its own test. A mock *replaces* something the test must not really call (sending an email, charging a card, calling a slow API). The classic mistake: `service.py` did `from mailer import send_email`, so `service` now holds its *own* name `send_email`. Patching `mailer.send_email` changes the original but not the copy `service` uses. Patch the name where it is *used*: `patch("service.send_email")`, and check the call with `assert_called_once_with(...)`. `monkeypatch.setattr` does the same job with automatic undo.

`solutions/test_Q16_fixtures.py`:

```python
# Q16 (fixtures) - Fixtures and parametrize
import pytest


def final_price(price, percent):
    if not 0 <= percent <= 100:
        raise ValueError("percent must be 0..100")
    return price - price * percent // 100


@pytest.fixture
def catalogue():
    # built fresh for every test that asks for it
    return {"Python": 499, "SQL": 399}


@pytest.mark.parametrize(
    "price, percent, expected",
    [(500, 0, 500), (500, 10, 450), (500, 100, 0), (399, 50, 200)],
)
def test_final_price(price, percent, expected):
    assert final_price(price, percent) == expected


@pytest.mark.parametrize("percent", [-1, 101])
def test_bad_percent(percent):
    with pytest.raises(ValueError, match="0..100"):
        final_price(500, percent)


def test_fixture_is_fresh(catalogue):
    catalogue["Rust"] = 999
    assert len(catalogue) == 3


def test_fixture_is_fresh_again(catalogue):
    assert len(catalogue) == 2      # the Rust course from the test above is gone
```

`solutions/Q16_app/mailer.py`:

```python
def send_email(to, text):
    raise RuntimeError("the real mail server must not be called in tests")
```

`solutions/Q16_app/service.py`:

```python
from Q16_app.mailer import send_email      # the name now lives HERE too


def welcome(student):
    send_email(student, "Welcome to allcsvideos")
    return "sent"
```

`solutions/test_Q16_mock.py`:

```python
# Q16 (mock) - Mocking: patch the name where it is LOOKED UP
from unittest.mock import patch

import pytest

from Q16_app import service


def test_patching_the_wrong_place_does_not_help():
    # service already holds its own reference, so this patch changes nothing for it
    with patch("Q16_app.mailer.send_email") as fake:
        with pytest.raises(RuntimeError):
            service.welcome("asha@example.com")
        fake.assert_not_called()


def test_patch_where_it_is_used():
    with patch("Q16_app.service.send_email") as fake:
        assert service.welcome("asha@example.com") == "sent"
    fake.assert_called_once_with("asha@example.com", "Welcome to allcsvideos")


def test_monkeypatch_does_the_same(monkeypatch):
    sent = []
    monkeypatch.setattr(service, "send_email", lambda to, text: sent.append(to))
    service.welcome("lukas@example.com")
    assert sent == ["lukas@example.com"]
```

Run it: `python -m pytest test_Q16_fixtures.py test_Q16_mock.py -v` (from inside `solutions/`, with the virtual environment active).

Output (Python 3.14):

```text
test_Q16_fixtures.py::test_final_price[500-0-500] PASSED
test_Q16_fixtures.py::test_final_price[500-10-450] PASSED
test_Q16_fixtures.py::test_final_price[500-100-0] PASSED
test_Q16_fixtures.py::test_final_price[399-50-200] PASSED
test_Q16_fixtures.py::test_bad_percent[-1] PASSED
test_Q16_fixtures.py::test_bad_percent[101] PASSED
test_Q16_fixtures.py::test_fixture_is_fresh PASSED
test_Q16_fixtures.py::test_fixture_is_fresh_again PASSED
test_Q16_mock.py::test_patching_the_wrong_place_does_not_help PASSED
test_Q16_mock.py::test_patch_where_it_is_used PASSED
test_Q16_mock.py::test_monkeypatch_does_the_same PASSED
============================== 11 passed in 1.03s ==============================
```

**Rahul's follow-up:** *What is the risk of too many mocks?* The test then checks your mock, not your code. Prefer real objects and fakes for your own logic, and mock only the edges.

</details>


<details>
<summary><b>Q17 · What is a race condition?</b> <i>(Concurrency)</i></summary>

**Taught in:** M12-L02 (threads, locks and races); M16-L04 (row locks in a database); M23-L01 question 17.

**In one breath (lesson one):** The result depends on thread timing, for example when two threads read, change and write the same number. Avoid sharing, or use a lock or a queue.

**Fuller answer.** A race condition is when the result depends on thread timing, for example two threads that both read a number, add one, and write it back: one update is lost. In the example, 200 deposits can finish with less than 200, and the exact number changes from run to run. Prevention: do not share changeable data; use a lock (`with lock:`) around the read-change-write step; hand work over through a `queue.Queue`; or let the database do it atomically (`UPDATE ... SET n = n + 1`, or a row lock with `SELECT ... FOR UPDATE`).

`solutions/Q17.py`:

```python
# Q17 - A race condition and a Lock
import threading
import time

balance = 0
lock = threading.Lock()

def deposit_unsafe():
    global balance
    current = balance               # read
    time.sleep(0)                   # another thread may run here
    balance = current + 1           # write: may overwrite someone else's update

def deposit_safe():
    global balance
    with lock:                      # only one thread inside at a time
        current = balance
        time.sleep(0)
        balance = current + 1

def run(worker):
    global balance
    balance = 0
    threads = [threading.Thread(target=worker) for _ in range(200)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return balance

print("unsafe, expected 200:", run(deposit_unsafe))
print("safe,   expected 200:", run(deposit_safe))
```

Run it: `python Q17.py`.

Output (Python 3.14):

```text
unsafe, expected 200: 199
safe,   expected 200: 200
```

**Rahul's follow-up:** *Does the GIL protect you from races?* No. Threads can switch between the read and the write. The GIL only protects the interpreter's own internals.

</details>


<details>
<summary><b>Q18 · How do you store passwords?</b> <i>(Security)</i></summary>

**Taught in:** M17-L01 (passwords done right); M23-L01 question 18.

**In one breath (lesson one):** As a slow, salted hash. Never as plain text, and never with a fast hash.

**Fuller answer.** As a slow, salted hash, made with a password-hashing algorithm such as argon2 (or bcrypt), never plain text and never a fast hash such as SHA-256. The salt is random per password, so two users with the same password get different hashes, and precomputed tables are useless. The slowness is deliberate: it makes every guess expensive for an attacker. You verify by hashing the login attempt with the stored salt and parameters, never by decrypting. Never log passwords either.

`solutions/Q18.py`:

```python
# Q18 - Storing passwords: hash, salt, slow on purpose
import hashlib
import time

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

password = "correct horse battery staple"

print("sha256 is fast and unsalted:", hashlib.sha256(password.encode()).hexdigest()[:16], "...")
print("same input, same hash      :", hashlib.sha256(password.encode()).hexdigest()
      == hashlib.sha256(password.encode()).hexdigest())

ph = PasswordHasher()
first, second = ph.hash(password), ph.hash(password)
print("argon2 starts with         :", first.split("$")[1], "|", first.split("$")[2])
print("same password, two hashes  :", first != second)   # a random salt each time

print("right password verifies    :", ph.verify(first, password))
try:
    ph.verify(first, "wrong guess")
except VerifyMismatchError:
    print("wrong password             : VerifyMismatchError")

start = time.perf_counter()
ph.hash(password)
print("one hash took a noticeable time:", time.perf_counter() - start > 0.005)
```

Run it: `python Q18.py`.

Output (Python 3.14):

```text
sha256 is fast and unsalted: c4bbcb1fbec99d65 ...
same input, same hash      : True
argon2 starts with         : argon2id | v=19
same password, two hashes  : True
right password verifies    : True
wrong password             : VerifyMismatchError
one hash took a noticeable time: True
```

**Rahul's follow-up:** *What if the hashing parameters change later?* The stored string records them. Verify with the old ones, and re-hash with the new ones after a successful login (`check_needs_rehash`).

</details>


### Q19 to Q40 · Twenty-two more

**Language basics**

<details>
<summary><b>Q19 · What is the difference between mutable and immutable objects? Give examples.</b> <i>(Language basics)</i></summary>

**Taught in:** M05-L06 (names, objects and mutability); M02-L01 (variables as labels).

**Model answer.** A mutable object can be changed in place after it is made; an immutable one cannot. Lists, dictionaries and sets are mutable. Numbers, strings, tuples, frozensets, bytes and `None` are immutable. When you "change" an immutable value, such as `name += " Rao"`, Python builds a new object and moves the label onto it. When you change a mutable one, such as `team += [...]`, every label on that object sees the change. One more detail: a tuple is immutable, but it can hold a list, and that list can still change.

`solutions/Q19.py`:

```python
# Q19 - Mutable and immutable
name = "Asha"
before = id(name)
name += " Rao"                      # builds a NEW string
print(name, id(name) == before)

team = ["Lukas", "Priya"]
before = id(team)
team += ["Meera"]                   # changes the SAME list
print(team, id(team) == before)

point = (3, 4)
try:
    point[0] = 9
except TypeError as error:
    print("TypeError:", error)

# an immutable tuple can still hold a mutable list
pair = ("Asha", ["python"])
pair[1].append("sql")
print(pair)
```

Run it: `python Q19.py`.

Output (Python 3.14):

```text
Asha Rao False
['Lukas', 'Priya', 'Meera'] True
TypeError: 'tuple' object does not support item assignment
('Asha', ['python', 'sql'])
```

**Rahul's follow-up:** *Does immutable mean the variable cannot be reassigned?* No. The variable is only a label, and you can always move it to another object. Immutable means the *object* cannot be changed in place.

</details>


<details>
<summary><b>Q20 · What counts as false in Python? When is `if x:` wrong and `if x is None:` right?</b> <i>(Language basics)</i></summary>

**Taught in:** M02-L04 (True, False and None); M03-L02 (comparing and combining).

**Model answer.** These are falsy: `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `()`, `None` and `False`. Everything else is truthy. `if not x` mixes "nothing was given" with "a valid empty or zero value was given". In the example, a discount of `0` is a real answer, but `if not discount` treats it as missing and applies 10 percent. When `None` means "not provided", test `is None`.

`solutions/Q20.py`:

```python
# Q20 - Truthiness and None
falsy = [0, 0.0, "", [], {}, set(), (), None, False]
print([bool(x) for x in falsy])

def final_price(price, discount=None):
    if not discount:                # BUG: treats 0 like "no discount given"
        discount = 10
    return price - price * discount // 100

def final_price_fixed(price, discount=None):
    if discount is None:            # only None means "not given"
        discount = 10
    return price - price * discount // 100

print(final_price(500, 0), final_price_fixed(500, 0))
print(final_price(500), final_price_fixed(500))
```

Run it: `python Q20.py`.

Output (Python 3.14):

```text
[False, False, False, False, False, False, False, False, False]
450 500
450 450
```

**Rahul's follow-up:** *Is `"0"` truthy?* Yes. It is a non-empty string. Only the empty string is falsy.

</details>


**Data structures**

<details>
<summary><b>Q21 · What is the difference between `sorted()` and `.sort()`? What does "stable" mean?</b> <i>(Data structures)</i></summary>

**Taught in:** M05-L01 (lists: sort and sorted).

**Model answer.** `sorted(x)` returns a *new* list and works on any iterable. `x.sort()` sorts the list in place and returns `None`, a common beginner bug when someone writes `x = x.sort()`. `key=` takes a function that gives the value to compare, and `reverse=True` flips the order. Python's sort is stable: items that compare equal keep their original order. That lets you sort twice (name first, then score), or sort once with a tuple key such as `(-score, name)`.

`solutions/Q21.py`:

```python
# Q21 - sorted, sort and stability
students = [("Priya", 85), ("Lukas", 72), ("Asha", 85), ("Meera", 72)]
print(sorted(students, key=lambda s: s[1]))          # ties keep original order
print(sorted(students, key=lambda s: (-s[1], s[0])))  # score high-to-low, then name

names = ["lukas", "Asha", "priya", "Meera"]
print(sorted(names), sorted(names, key=str.lower))

result = names.sort()
print(result, names)                # .sort() changes the list and returns None
```

Run it: `python Q21.py`.

Output (Python 3.14):

```text
[('Lukas', 72), ('Meera', 72), ('Priya', 85), ('Asha', 85)]
[('Asha', 85), ('Priya', 85), ('Lukas', 72), ('Meera', 72)]
['Asha', 'Meera', 'lukas', 'priya'] ['Asha', 'lukas', 'Meera', 'priya']
None ['Asha', 'Meera', 'lukas', 'priya']
```

**Rahul's follow-up:** *How do you sort case-insensitively?* `sorted(names, key=str.lower)`. The key function is called once per item, not once per comparison.

</details>


**Functions, closures and decorators**

<details>
<summary><b>Q22 · Explain scope: what can a function see? When do you need `global` and `nonlocal`?</b> <i>(Functions, closures and decorators)</i></summary>

**Taught in:** M04-L04 (scope); M09-L03 (`nonlocal` in closures).

**Model answer.** Python looks a name up in this order: Local, Enclosing function, Global, Built-in (LEGB). Reading a global from inside a function works. But if the function *assigns* to the name anywhere, Python treats it as local for the whole function, so reading it before the assignment raises `UnboundLocalError`. `global` rebinds a module-level name; `nonlocal` rebinds a name in the enclosing function, which is how a closure keeps a counter. I prefer passing values in and returning values out.

`solutions/Q22.py`:

```python
# Q22 - Scope: LEGB, global and nonlocal
students = 0

def bad():
    students += 1                   # assignment makes it local to bad()

try:
    bad()
except UnboundLocalError as error:
    print("UnboundLocalError:", error)

def make_counter():
    count = 0
    def step():
        nonlocal count              # rebind the enclosing variable
        count += 1
        return count
    return step

step = make_counter()
print(step(), step(), step())
```

Run it: `python Q22.py`.

Output (Python 3.14):

```text
UnboundLocalError: cannot access local variable 'students' where it is not associated with a value
1 2 3
```

**Rahul's follow-up:** *Why is a global variable a poor choice for shared state?* Any function can change it, so bugs are hard to trace, and tests cannot easily reset it.

</details>


<details>
<summary><b>Q23 · How do you write a decorator that takes arguments, such as `@retry(times=3)`?</b> <i>(Functions, closures and decorators)</i></summary>

**Taught in:** M09-L03 (decorators); M09-B05 (the decorator toolkit); M18-L04 (retries).

**Model answer.** You need three layers. The outer function takes the settings and returns the real decorator. The decorator takes the function and returns the wrapper. The wrapper runs on every call. Read `@retry(times=3)` as two steps: `retry(times=3)` runs first and gives back a decorator, and *that* decorates the function. Retry only the errors you expect, wait longer each time, and re-raise the last error when you give up.

`solutions/Q23.py`:

```python
# Q23 - A decorator that takes arguments
import functools

def retry(times, exceptions=(Exception,)):      # layer 1: the settings
    def decorator(func):                        # layer 2: the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):           # layer 3: each call
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    print(f"attempt {attempt} failed: {error}")
                    if attempt == times:
                        raise
        return wrapper
    return decorator

calls = {"n": 0}

@retry(times=3, exceptions=(ConnectionError,))
def fetch():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("network down")
    return "ok"

print(fetch())
```

Run it: `python Q23.py`.

Output (Python 3.14):

```text
attempt 1 failed: network down
attempt 2 failed: network down
ok
```

**Rahul's follow-up:** *What should a good retry decorator not retry?* Errors that will fail again, such as bad input (a 4xx answer), and operations that are not idempotent unless you made them so (module eighteen).

</details>


<details>
<summary><b>Q24 · How do recursion and the recursion limit work? How does `functools.cache` help?</b> <i>(Functions, closures and decorators)</i></summary>

**Taught in:** M04-L05 (recursion and lambdas, the recursion limit); M09-L05 (`functools.cache`).

**Model answer.** A recursive function calls itself with a smaller problem and needs a base case. Python allows about 1000 nested calls, then raises `RecursionError`, so a deep problem needs a loop or an explicit stack. Plain Fibonacci repeats the same sub-problems (21,891 calls for `fib(20)`). `@functools.cache` remembers each answer, so `fib(80)` needs only 81 calls. A cached function must be *pure* (same input, same answer) and take hashable arguments.

`solutions/Q24.py`:

```python
# Q24 - Recursion, the limit and functools.cache
import functools
import sys

calls = 0
def fib(n):
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)

fib(20)
print("plain calls:", calls)

cached_calls = 0
@functools.cache
def fib_fast(n):
    global cached_calls
    cached_calls += 1
    return n if n < 2 else fib_fast(n - 1) + fib_fast(n - 2)

print(fib_fast(80), "cached calls:", cached_calls)
print(fib_fast.cache_info())

print("limit:", sys.getrecursionlimit())
def forever(n):
    return forever(n + 1)
try:
    forever(0)
except RecursionError as error:
    print("RecursionError:", error)
```

Run it: `python Q24.py`.

Output (Python 3.14):

```text
plain calls: 21891
23416728348467685 cached calls: 81
CacheInfo(hits=78, misses=81, maxsize=None, currsize=81)
limit: 1000
RecursionError: maximum recursion depth exceeded
```

**Rahul's follow-up:** *Could you raise the limit with `sys.setrecursionlimit`?* You can, but a very deep recursion can crash the interpreter. Prefer an iterative solution.

</details>


**Object-oriented programming**

<details>
<summary><b>Q25 · What is the MRO? How does `super()` work with multiple inheritance?</b> <i>(Object-oriented programming)</i></summary>

**Taught in:** M08-L04 (inheritance and composition, lookup order, `super()`).

**Model answer.** The method resolution order (MRO) is the list of classes Python searches, in order, for a method; you see it with `Class.__mro__`. Python builds it with the C3 rule: a class comes before its parents, and the order of the parents you wrote is kept. `super()` does *not* mean "my parent". It means "the next class after me in the MRO". In a diamond, every class calls `super().hello()` once, so the shared base `Person` appears exactly once. I prefer composition (an object that *has* another) unless the "is a" relation is clear.

`solutions/Q25.py`:

```python
# Q25 - MRO and super()
class Person:
    def hello(self):
        return ["Person"]

class Student(Person):
    def hello(self):
        return ["Student"] + super().hello()

class Mentor(Person):
    def hello(self):
        return ["Mentor"] + super().hello()

class StudentMentor(Student, Mentor):
    def hello(self):
        return ["StudentMentor"] + super().hello()

print([c.__name__ for c in StudentMentor.__mro__])
print(StudentMentor().hello())      # Person appears once: super() follows the MRO
```

Run it: `python Q25.py`.

Output (Python 3.14):

```text
['StudentMentor', 'Student', 'Mentor', 'Person', 'object']
['StudentMentor', 'Student', 'Mentor', 'Person']
```

**Rahul's follow-up:** *Inheritance or composition?* Start with composition. Inheritance couples a child to its parent's details; use it when the child truly *is* a kind of the parent.

</details>


<details>
<summary><b>Q26 · What do `__repr__`, `__str__`, `__eq__` and `__hash__` do? How are they connected?</b> <i>(Object-oriented programming)</i></summary>

**Taught in:** M08-L05 (dunder methods); M08-L06 (dataclasses write them for you).

**Model answer.** `__repr__` is for developers: unambiguous, ideally something you could type back in. `__str__` is for users, used by `print`. If only `__repr__` exists, `print` uses it. `__eq__` defines `==`. Rule: objects that compare equal must have the same hash. So if you define `__eq__`, define `__hash__` from the same fields (or Python sets `__hash__` to `None` and the class becomes unhashable, so it cannot go into a set or be a dictionary key). Dataclasses generate all of this.

`solutions/Q26.py`:

```python
# Q26 - __repr__, __str__, __eq__ and __hash__
class Course:
    def __init__(self, title, price):
        self.title, self.price = title, price

    def __repr__(self):                       # for developers
        return f"Course({self.title!r}, {self.price})"

    def __str__(self):                        # for users
        return f"{self.title} (Rs {self.price})"

    def __eq__(self, other):
        return (self.title, self.price) == (other.title, other.price)

    def __hash__(self):                       # equal objects must hash alike
        return hash((self.title, self.price))

a, b = Course("Python", 499), Course("Python", 499)
print(a, [a], repr(a))
print(a == b, a is b, len({a, b}))

class NoHash:
    def __eq__(self, other):
        return True

try:
    {NoHash()}
except TypeError as error:
    print("TypeError:", error)
```

Run it: `python Q26.py`.

Output (Python 3.14):

```text
Python (Rs 499) [Course('Python', 499)] Course('Python', 499)
True False 1
TypeError: cannot use 'NoHash' as a set element (unhashable type: 'NoHash')
```

**Rahul's follow-up:** *What happens to a set if you change a field that feeds `__hash__`?* The object sits in the wrong slot and lookups fail. Hash only fields that never change, or make the class frozen.

</details>


<details>
<summary><b>Q27 · What is a property? Why not make every attribute private with getters and setters?</b> <i>(Object-oriented programming)</i></summary>

**Taught in:** M08-L03 (encapsulation and properties).

**Model answer.** A property lets you run code when an attribute is read or written, while the caller still writes `lesson.minutes = 90`. You use it to validate (reject negative minutes), to compute a value (`hours` from `minutes`), or to make something read-only. Python does not need Java-style getters and setters from day one: start with a plain attribute, and add a property later without changing any caller. A leading underscore (`_minutes`) is only a polite signal that the name is internal.

`solutions/Q27.py`:

```python
# Q27 - Properties
class Lesson:
    def __init__(self, title, minutes):
        self.title = title
        self.minutes = minutes      # goes through the setter below

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value):
        if value <= 0:
            raise ValueError("minutes must be positive")
        self._minutes = value

    @property
    def hours(self):                # computed, read-only
        return round(self._minutes / 60, 2)

lesson = Lesson("Loops", 90)
print(lesson.minutes, lesson.hours)
for bad in (lambda: setattr(lesson, "minutes", -5), lambda: setattr(lesson, "hours", 2)):
    try:
        bad()
    except (ValueError, AttributeError) as error:
        print(type(error).__name__ + ":", error)
```

Run it: `python Q27.py`.

Output (Python 3.14):

```text
90 1.5
ValueError: minutes must be positive
AttributeError: property 'hours' of 'Lesson' object has no setter
```

**Rahul's follow-up:** *How do you make an attribute read-only?* Define a property with no setter. Assigning then raises `AttributeError`, as the last output line shows.

</details>


**Iterators and generators**

<details>
<summary><b>Q28 · What is the difference between an iterable and an iterator?</b> <i>(Iterators and generators)</i></summary>

**Taught in:** M09-L01 (iterables and iterators).

**Model answer.** An iterable is anything you can loop over: it has `__iter__`, which returns an iterator. An iterator remembers its place and has `__next__`, which gives the next item and raises `StopIteration` at the end. A `for` loop calls `iter()` once, then `next()` again and again until `StopIteration`. A list is iterable but not an iterator; you can loop over it many times. An iterator is used up once it is exhausted, and `iter(iterator)` returns the iterator itself.

`solutions/Q28.py`:

```python
# Q28 - Iterable vs iterator
lessons = ["Variables", "Loops", "Functions"]     # iterable: can give an iterator
it = iter(lessons)                                # iterator: remembers its place
print(next(it), next(it))
print(list(it))                                   # what is left
print(list(it))                                   # exhausted: empty
try:
    next(it)
except StopIteration:
    print("StopIteration")

class Countdown:
    def __init__(self, start):
        self.n = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.n == 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

print(list(Countdown(3)))
print(iter(it) is it, iter(lessons) is lessons)   # iterators return themselves
```

Run it: `python Q28.py`.

Output (Python 3.14):

```text
Variables Loops
['Functions']
[]
StopIteration
[3, 2, 1]
True False
```

**Rahul's follow-up:** *Why does a second `list(it)` give `[]`?* The iterator already reached the end. Make a fresh one with `iter(...)` on the original iterable.

</details>


**Memory, the GIL and performance**

<details>
<summary><b>Q29 · How do you find out why code is slow, and what do you try first?</b> <i>(Memory, the GIL and performance)</i></summary>

**Taught in:** M11-L04 (measuring and improving speed); M20-L03 (finding slow code); M20-L04 (making it faster).

**Model answer.** Measure first, because guessing is usually wrong. `timeit` compares two small snippets fairly (take the best of several repeats). `cProfile` shows which functions use the time. Then fix the biggest cost in this order: a better algorithm or data structure (a set instead of a list for lookups), less repeated work (caching, fewer queries), vectorised or compiled helpers (NumPy), and only then parallelism. Do not trust folklore either: the example times `+=` against `join` for building text, and on this machine the gap is small, because CPython optimises `+=` on strings.

`solutions/Q29.py`:

```python
# Q29 - Measuring before optimising
import cProfile
import pstats
import timeit

def concat(n):
    out = ""
    for i in range(n):
        out += str(i)
    return out

def join(n):
    return "".join(str(i) for i in range(n))

print(concat(1000) == join(1000))
for name, fn in (("concat", concat), ("join", join)):
    best = min(timeit.repeat(lambda: fn(20_000), number=20, repeat=5))
    print(f"{name}: best of 5 = {best:.4f}s")

profiler = cProfile.Profile()
profiler.runcall(concat, 200_000)
stats = pstats.Stats(profiler)
stats.sort_stats("cumulative")
rows = sorted(stats.stats.items(), key=lambda kv: -kv[1][3])[:1]
print("profiled calls:", stats.total_calls > 0, "| top entry:", rows[0][0][2])
```

Run it: `python Q29.py`.

Output (Python 3.14):

```text
True
concat: best of 5 = 0.0283s
join: best of 5 = 0.0281s
profiled calls: True | top entry: concat
```

**Rahul's follow-up:** *Why take the *best* of several runs?* Other programs on the machine only ever make a run slower, so the minimum is the closest to the true cost.

</details>


**Testing**

<details>
<summary><b>Q30 · What makes a good test? How do coverage and property-based tests help?</b> <i>(Testing)</i></summary>

**Taught in:** M13-L01 (first tests); M13-L04 (coverage and property-based testing); M13-L05 (TDD).

**Model answer.** A good test checks one behaviour, has a name that says what it checks, covers the edges (empty, zero, one, the maximum, bad input), is fast, and does not depend on other tests or on the clock. Coverage tells you which lines never ran; it cannot tell you that the checked lines are *right*, so 100 percent is not a goal by itself. A property-based test (Hypothesis) states a rule that must hold for any input, such as "normalising twice equals normalising once", and the library tries many generated inputs, shrinking a failure to the smallest example.

`solutions/test_Q30.py`:

```python
# Q30 - What makes a good test (edge cases, one behaviour per test, properties)
from hypothesis import given, strategies as st


def normalize(text):
    return " ".join(text.split())


def test_collapses_spaces():
    assert normalize("  hello   world ") == "hello world"


def test_empty_and_blank():
    assert normalize("") == ""
    assert normalize("   \t\n ") == ""


@given(st.text())
def test_idempotent(text):
    once = normalize(text)
    assert normalize(once) == once          # a property: doing it twice changes nothing


@given(st.text())
def test_no_double_spaces(text):
    assert "  " not in normalize(text)
```

Run it: `python -m pytest test_Q30.py -v` (from inside `solutions/`, with the virtual environment active).

Output (Python 3.14):

```text
test_Q30.py::test_collapses_spaces PASSED
test_Q30.py::test_empty_and_blank PASSED
test_Q30.py::test_idempotent PASSED
test_Q30.py::test_no_double_spaces PASSED
============================== 4 passed in 2.64s ===============================
```

**Rahul's follow-up:** *When would you write the test first?* When the requirement is clear and the interface is not: TDD (module thirteen, lesson five) makes you design the call before the code.

</details>


**Web and backend**

<details>
<summary><b>Q31 · How does FastAPI validate input? What is `Depends`, and how do you replace a dependency in tests?</b> <i>(Web and backend)</i></summary>

**Taught in:** M15-L03 (pydantic models); M15-L05 (dependencies, routers and middleware); M15-B08.

**Model answer.** You describe the body as a pydantic model with types and rules (`Field(min_length=2)`, `gt=0`). FastAPI checks the request against it before your function runs and, if it fails, answers `422` with a list of every problem and its location, so your code only ever sees valid data. `Depends(get_db)` says "call this function and hand me the result"; it is how a database session, the current user or settings reach an endpoint. In tests you swap it with `app.dependency_overrides[get_db] = lambda: fake`, so no real database is needed.

`solutions/Q31.py`:

```python
# Q31 - FastAPI: pydantic validation, Depends and overriding a dependency in tests
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class EnrollIn(BaseModel):
    student: str = Field(min_length=2)
    course_id: int = Field(gt=0)


def get_db():
    return {"name": "real database"}


Db = Annotated[dict, Depends(get_db)]


@app.post("/enrollments", status_code=201)
def enroll(body: EnrollIn, db: Db):
    return {"db": db["name"], "student": body.student, "course_id": body.course_id}


client = TestClient(app)

ok = client.post("/enrollments", json={"student": "Asha", "course_id": 1})
print(ok.status_code, ok.json())

bad = client.post("/enrollments", json={"student": "A", "course_id": 0})
print(bad.status_code)
for problem in bad.json()["detail"]:
    print(" ", problem["loc"], "->", problem["msg"])

app.dependency_overrides[get_db] = lambda: {"name": "fake test database"}
print(client.post("/enrollments", json={"student": "Lukas", "course_id": 2}).json())
```

Run it: `python Q31.py`.

Output (Python 3.14):

```text
201 {'db': 'real database', 'student': 'Asha', 'course_id': 1}
422
  ['body', 'student'] -> String should have at least 2 characters
  ['body', 'course_id'] -> Input should be greater than 0
{'db': 'fake test database', 'student': 'Lukas', 'course_id': 2}
```

**Rahul's follow-up:** *Which status code means "the data is the wrong shape" and which "the data is valid but conflicts"?* `422` for validation, `409` for a conflict such as a duplicate.

</details>


<details>
<summary><b>Q32 · Which status codes would you return, and how do you make a POST safe to retry?</b> <i>(Web and backend)</i></summary>

**Taught in:** M15-L02 (parameters, bodies and responses); M15-L04 (errors done right); M18-L02 and M18-L04 (idempotency, retries).

**Model answer.** `201` for a created resource (with a `Location` header), `200` for a read or an update, `204` for a delete with no body, `404` for a missing resource, `409` for a conflict, `422` for invalid input, `401` for not logged in and `403` for logged in but not allowed. A network can fail after the server finished, so clients retry. A `POST` is not idempotent by itself, so the client sends an `Idempotency-Key`; the server stores the key with the result, and a retry with the same key gets the same answer instead of a second record. In the example the retry returns `200` and only one enrollment is stored.

`solutions/Q32.py`:

```python
# Q32 - Status codes, and an idempotency key for POST
from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.testclient import TestClient

app = FastAPI()
enrollments = {}                     # id -> record
seen_keys = {}                      # Idempotency-Key -> id


@app.post("/enrollments", status_code=201)
def create(student: str, course_id: int, response: Response,
           idempotency_key: str | None = Header(default=None)):
    if idempotency_key in seen_keys:            # same request again: same answer
        response.status_code = 200
        return enrollments[seen_keys[idempotency_key]]
    for record in enrollments.values():
        if (record["student"], record["course_id"]) == (student, course_id):
            raise HTTPException(409, "already enrolled")
    new_id = len(enrollments) + 1
    enrollments[new_id] = {"id": new_id, "student": student, "course_id": course_id}
    if idempotency_key:
        seen_keys[idempotency_key] = new_id
    return enrollments[new_id]


@app.get("/enrollments/{enrollment_id}")
def read(enrollment_id: int):
    if enrollment_id not in enrollments:
        raise HTTPException(404, "no such enrollment")
    return enrollments[enrollment_id]


client = TestClient(app)
key = {"Idempotency-Key": "abc-123"}
params = {"student": "Asha", "course_id": 1}

print("first  POST :", client.post("/enrollments", params=params, headers=key).status_code)
print("retry  POST :", client.post("/enrollments", params=params, headers=key).status_code)
print("new key POST:", client.post("/enrollments", params=params, headers={"Idempotency-Key": "zzz"}).status_code)
print("GET found   :", client.get("/enrollments/1").status_code)
print("GET missing :", client.get("/enrollments/99").status_code)
print("bad input   :", client.post("/enrollments", params={"student": "Asha", "course_id": "x"}).status_code)
print("enrollments stored:", len(enrollments))
```

Run it: `python Q32.py`.

Output (Python 3.14):

```text
first  POST : 201
retry  POST : 200
new key POST: 409
GET found   : 200
GET missing : 404
bad input   : 422
enrollments stored: 1
```

**Rahul's follow-up:** *What does idempotent mean for `PUT` and `DELETE`?* Doing it once or five times leaves the same final state.

</details>


<details>
<summary><b>Q33 · Should an endpoint be `def` or `async def`?</b> <i>(Web and backend)</i></summary>

**Taught in:** M15-L06 (async endpoints, background tasks and docs); M12-L04 and M12-L05 (asyncio).

**Model answer.** FastAPI runs a plain `def` endpoint in a worker thread, so a blocking call inside it is fine and other requests keep flowing. It runs an `async def` endpoint directly on the event loop, so you must only `await` non-blocking things inside it. One blocking call there, such as `time.sleep` or a synchronous database driver, freezes the whole server. In the measurement, ten parallel requests took about 0.4 s for the `def` endpoint, about 4 s for the `async def` that blocks, and about 0.4 s for the `async def` that awaits. Rule: use `async def` only with async libraries; otherwise use `def`.

`solutions/Q33_server.py`:

```python
import time
import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get("/sync-sleep")
def sync_sleep():                   # plain def: FastAPI runs it in a worker thread
    time.sleep(0.4)
    return {"ok": True}


@app.get("/async-blocking")
async def async_blocking():         # async def + a blocking call: freezes the loop
    time.sleep(0.4)
    return {"ok": True}


@app.get("/async-correct")
async def async_correct():          # async def + await: the loop stays free
    await asyncio.sleep(0.4)
    return {"ok": True}
```

`solutions/Q33.py`:

```python
# Q33 - def or async def for an endpoint? Measured against a real server.
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

PORT = 23743
server = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "Q33_server:app", "--port", str(PORT), "--log-level", "error"]
)
try:
    for _ in range(50):             # wait until the server answers
        try:
            httpx.get(f"http://127.0.0.1:{PORT}/async-correct")
            break
        except httpx.ConnectError:
            time.sleep(0.1)

    def burst(path):
        start = time.perf_counter()
        with ThreadPoolExecutor(10) as pool:
            list(pool.map(lambda _: httpx.get(f"http://127.0.0.1:{PORT}{path}"), range(10)))
        return time.perf_counter() - start

    for path in ("/sync-sleep", "/async-blocking", "/async-correct"):
        print(f"10 parallel requests to {path:<16}{burst(path):.2f}s")
finally:
    server.terminate()
    server.wait()
```

Run it: `python Q33.py` (it starts `Q33_server.py` with uvicorn on port 23743 and stops it again).

Output (Python 3.14):

```text
10 parallel requests to /sync-sleep     0.43s
10 parallel requests to /async-blocking 4.06s
10 parallel requests to /async-correct  0.41s
```

**Rahul's follow-up:** *Where do slow jobs such as sending email belong?* In a background task or a queue worker (module eighteen), not in the request.

</details>


**Databases and caching**

<details>
<summary><b>Q34 · What is the N+1 query problem and how do you fix it?</b> <i>(Databases and caching)</i></summary>

**Taught in:** M16-L03 (relationships and the N+1 problem); M20-L04 (making it faster).

**Model answer.** You load N parents with one query, then touch a related collection on each one, and the ORM quietly runs one extra query per parent: N+1 queries. With 20 courses the example runs 21 queries instead of 2. It is invisible in code and slow in production, because each query pays a network round trip. Fix it by loading the related rows up front: `selectinload` (a second query with `IN (...)`) or `joinedload` (one join). Find it by counting queries in a test, or by watching the logs.

`solutions/Q34.py`:

```python
# Q34 - The N+1 query problem (Postgres in Docker, SQLAlchemy 2)
from sqlalchemy import ForeignKey, create_engine, event, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload

URL = "postgresql+psycopg://practice:practice@localhost:23604/practice"
engine = create_engine(URL)


class Base(DeclarativeBase):
    pass


class Course(Base):
    __tablename__ = "q34_course"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="course")


class Lesson(Base):
    __tablename__ = "q34_lesson"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    course_id: Mapped[int] = mapped_column(ForeignKey("q34_course.id"))
    course: Mapped[Course] = relationship(back_populates="lessons")


queries = []
@event.listens_for(engine, "before_cursor_execute")
def count(conn, cursor, statement, params, context, executemany):
    queries.append(statement)


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
with Session(engine) as db:
    db.add_all([Course(title=f"Course {i}", lessons=[Lesson(title=f"L{j}") for j in range(3)])
                for i in range(20)])
    db.commit()

def total_lessons(options=()):
    queries.clear()
    with Session(engine) as db:
        courses = db.scalars(select(Course).options(*options)).all()
        total = sum(len(course.lessons) for course in courses)
    return total, len(queries)

print("lazy loading  : lessons, queries =", total_lessons())
print("selectinload  : lessons, queries =", total_lessons([selectinload(Course.lessons)]))
Base.metadata.drop_all(engine)
```

Run it: `python Q34.py` (needs the Postgres container from "How to work").

Output (Python 3.14):

```text
lazy loading  : lessons, queries = (60, 21)
selectinload  : lessons, queries = (60, 2)
```

**Rahul's follow-up:** *How would you notice it in production?* A slow endpoint whose trace shows many near-identical short queries (module twenty).

</details>


<details>
<summary><b>Q35 · What is a transaction? What do ACID and rollback mean?</b> <i>(Databases and caching)</i></summary>

**Taught in:** M16-L04 (migrations with Alembic and transactions).

**Model answer.** A transaction groups several statements into one all-or-nothing unit. If every statement succeeds, you `COMMIT`; if any fails, a `ROLLBACK` undoes all of them. The example moves Rs 200 between two wallets: the first transfer works, the Rs 900 transfer breaks a `CHECK` rule and rolls back, and the balances stay as they were. ACID names the guarantees: Atomic (all or nothing), Consistent (rules such as `CHECK` and foreign keys hold), Isolated (concurrent transactions do not see each other's half-done work) and Durable (committed data survives a crash).

`solutions/Q35.py`:

```python
# Q35 - Transactions: all or nothing (Postgres in Docker)
import psycopg

URL = "postgresql://practice:practice@localhost:23604/practice"

with psycopg.connect(URL, autocommit=True) as setup:
    setup.execute("DROP TABLE IF EXISTS q35_wallet")
    setup.execute("CREATE TABLE q35_wallet (name text PRIMARY KEY, rupees int CHECK (rupees >= 0))")
    setup.execute("INSERT INTO q35_wallet VALUES ('Asha', 500), ('Lukas', 100)")

def balances():
    with psycopg.connect(URL) as conn:
        return dict(conn.execute("SELECT name, rupees FROM q35_wallet ORDER BY name").fetchall())

def transfer(sender, receiver, amount):
    with psycopg.connect(URL) as conn:          # one transaction: commit on success, rollback on error
        conn.execute("UPDATE q35_wallet SET rupees = rupees - %s WHERE name = %s", (amount, sender))
        conn.execute("UPDATE q35_wallet SET rupees = rupees + %s WHERE name = %s", (amount, receiver))

print("start      :", balances())
transfer("Asha", "Lukas", 200)
print("after 200  :", balances())
try:
    transfer("Asha", "Lukas", 900)              # the first UPDATE breaks the CHECK
except psycopg.errors.CheckViolation as error:
    print("failed     :", type(error).__name__)
print("after fail :", balances(), "(nothing half-done)")

with psycopg.connect(URL, autocommit=True) as setup:
    setup.execute("DROP TABLE q35_wallet")
```

Run it: `python Q35.py` (needs the Postgres container from "How to work").

Output (Python 3.14):

```text
start      : {'Asha': 500, 'Lukas': 100}
after 200  : {'Asha': 300, 'Lukas': 300}
failed     : CheckViolation
after fail : {'Asha': 300, 'Lukas': 300} (nothing half-done)
```

**Rahul's follow-up:** *How do two people avoid booking the last seat?* Lock the row (`SELECT ... FOR UPDATE`) inside the transaction, then check the count (module sixteen, lesson four; build task nine).

</details>


<details>
<summary><b>Q36 · What is an index? When does it help and what does it cost?</b> <i>(Databases and caching)</i></summary>

**Taught in:** M16-L01 (SQL and PostgreSQL); M20-L03 and M20-L04 (finding slow code, `EXPLAIN`).

**Model answer.** An index is a sorted side structure that lets the database jump to matching rows instead of reading the whole table. It helps `WHERE`, `JOIN` and `ORDER BY` on columns that are selective. It costs disk space and slows every write, because the index must be updated too. Prove it, do not guess: `EXPLAIN ANALYZE`. In the example, finding one student in 300,000 rows changes from a sequential scan that reads all rows and throws away about 150,000 of them in each worker to an index scan that takes a tiny fraction of the time. Primary keys and unique constraints already have an index; foreign key columns usually need one added.

`solutions/Q36.py`:

```python
# Q36 - Indexes, proved with EXPLAIN ANALYZE (Postgres in Docker)
import psycopg

URL = "postgresql://practice:practice@localhost:23604/practice"

with psycopg.connect(URL, autocommit=True) as conn:
    conn.execute("DROP TABLE IF EXISTS q36_enrollment")
    conn.execute("CREATE TABLE q36_enrollment (id serial PRIMARY KEY, student_id int, course_id int)")
    conn.execute("""INSERT INTO q36_enrollment (student_id, course_id)
                    SELECT n % 50000, n % 40 FROM generate_series(1, 300000) n""")
    conn.execute("ANALYZE q36_enrollment")

    def plan(label):
        rows = conn.execute("EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF) "
                            "SELECT * FROM q36_enrollment WHERE student_id = 4242").fetchall()
        lines = [r[0] for r in rows]
        print(label)
        for line in lines:
            if "Scan" in line or "Execution" in line or "Rows Removed" in line:
                print("  ", line.strip())

    plan("without an index:")
    conn.execute("CREATE INDEX q36_student_idx ON q36_enrollment (student_id)")
    conn.execute("ANALYZE q36_enrollment")
    plan("with an index:")
    conn.execute("DROP TABLE q36_enrollment")
```

Run it: `python Q36.py` (needs the Postgres container from "How to work").

Output (Python 3.14):

```text
without an index:
   ->  Parallel Seq Scan on q36_enrollment (actual rows=3 loops=2)
   Rows Removed by Filter: 149997
   Execution Time: 8.773 ms
with an index:
   Bitmap Heap Scan on q36_enrollment (actual rows=6 loops=1)
   ->  Bitmap Index Scan on q36_student_idx (actual rows=6 loops=1)
   Execution Time: 0.034 ms
```

**Rahul's follow-up:** *When will the database ignore your index?* When the query returns a large part of the table (a scan is cheaper), when the column is wrapped in a function, or when the statistics say the table is tiny.

</details>


<details>
<summary><b>Q37 · What is cache-aside? How do you keep a cache from serving stale data?</b> <i>(Databases and caching)</i></summary>

**Taught in:** M18-L01 (Redis and caching); M20-L04 (making it faster).

**Model answer.** With cache-aside, the application owns the cache logic. On a read it looks in the cache first. On a *hit* it uses the cached value. On a *miss* it reads the database, stores the answer in the cache with an expiry (a TTL), and returns it. The danger is stale data: if you change the database and forget the cache, readers keep getting the old value (the example prints the old price of Rs 499 after the price became Rs 399). So every write also *invalidates* (deletes) the cached key, and the TTL is the safety net that fixes whatever you forget. Cache only what is read often and changes rarely, and remember that a cached function or value must not depend on who is asking.

`solutions/Q37.py`:

```python
# Q37 - Cache-aside and invalidation (Redis in Docker)
import json
import time

import redis

cache = redis.Redis(host="localhost", port=23404, db=7, decode_responses=True)
database = {1: {"title": "Python", "price": 499}}      # stands in for Postgres
reads = {"database": 0}


def read_from_database(course_id):
    reads["database"] += 1
    return database[course_id]


def get_course(course_id, ttl=60):
    key = f"q37:course:{course_id}"
    cached = cache.get(key)                         # 1. look in the cache
    if cached is not None:
        return json.loads(cached), "hit"
    course = read_from_database(course_id)          # 2. miss: ask the database
    cache.set(key, json.dumps(course), ex=ttl)      # 3. remember it, with an expiry
    return course, "miss"


def update_price(course_id, price):
    database[course_id]["price"] = price
    cache.delete(f"q37:course:{course_id}")         # invalidate, or readers see the old price


cache.delete("q37:course:1")
print(get_course(1))
print(get_course(1))
print("database reads so far:", reads["database"])

database[1]["price"] = 399                          # change the database but forget the cache...
print("stale:", get_course(1))                      # ...and readers get the old price
update_price(1, 399)                                # the right way
print("fresh:", get_course(1))

print(get_course(1, ttl=1)[1], end=" ")             # the TTL is the safety net
cache.expire("q37:course:1", 1)
time.sleep(1.2)
print(get_course(1)[1], "(after the 1 second expiry)")
cache.delete("q37:course:1")
```

Run it: `python Q37.py` (needs the Redis container from "How to work").

Output (Python 3.14):

```text
({'title': 'Python', 'price': 499}, 'miss')
({'title': 'Python', 'price': 499}, 'hit')
database reads so far: 1
stale: ({'title': 'Python', 'price': 499}, 'hit')
fresh: ({'title': 'Python', 'price': 399}, 'miss')
hit miss (after the 1 second expiry)
```

**Rahul's follow-up:** *What is a cache stampede?* When a popular key expires, many requests miss at once and all hit the database together. Remedies: a short lock so one request rebuilds the value, or a little random jitter in the TTLs.

</details>


**Security**

<details>
<summary><b>Q38 · What is SQL injection and how do you prevent it?</b> <i>(Security)</i></summary>

**Taught in:** M17-L04 (input attacks and secrets); M17-L03 (authorisation and the OWASP API top 10).

**Model answer.** SQL injection is when user input is pasted into the text of a query, so the input can change the query. The input `x' OR '1'='1` turns `WHERE name = 'x'` into a test that is always true and returns every row. The fix is *parameterised queries*: write `WHERE name = ?` (or `%s`, `:name`) and pass the value separately, so the database always treats it as data. ORMs and query builders do this for you; be careful with raw SQL and string formatting. Also give the application's database user only the permissions it needs.

`solutions/Q38.py`:

```python
# Q38 - SQL injection and the fix (standard library sqlite3)
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE users (name TEXT, role TEXT)")
db.executemany("INSERT INTO users VALUES (?, ?)", [("asha", "admin"), ("lukas", "student")])

def find_unsafe(name):
    return db.execute(f"SELECT name, role FROM users WHERE name = '{name}'").fetchall()

def find_safe(name):
    return db.execute("SELECT name, role FROM users WHERE name = ?", (name,)).fetchall()

attack = "x' OR '1'='1"
print("unsafe, attacker input:", find_unsafe(attack))     # leaks every row
print("safe,   attacker input:", find_safe(attack))        # just a strange name: no match
print("safe,   honest input  :", find_safe("lukas"))
```

Run it: `python Q38.py`.

Output (Python 3.14):

```text
unsafe, attacker input: [('asha', 'admin'), ('lukas', 'student')]
safe,   attacker input: []
safe,   honest input  : [('lukas', 'student')]
```

**Rahul's follow-up:** *Authentication against authorisation?* Authentication asks "who are you?" (a login gives `401` if missing). Authorisation asks "may you do this?" (`403` if not).

</details>


**Deployment and operations**

<details>
<summary><b>Q39 · How do you package a Python service in Docker, and how do you configure it per environment?</b> <i>(Deployment and operations)</i></summary>

**Taught in:** M19-L01 (Docker for Python apps); M19-L02 (configuration the 12-factor way); M19-L04 (running in production).

**Model answer.** Start from a slim Python image, install the dependencies, copy the code, and run as a normal user (`USER app`), never as root, so an attacker who breaks in has little power. Do not bake settings into the image: read them from environment variables (the 12-factor idea), with `pydantic-settings` giving typed values, defaults for development and validation at start-up. The same image then runs in testing and production, with only the environment changed. Secrets come from the environment or a secret store, never from the repository.

`solutions/Q39_docker/Dockerfile`:

```dockerfile
FROM python:3.14-slim
RUN useradd --create-home --uid 10001 app
WORKDIR /home/app
RUN pip install --no-cache-dir pydantic-settings
COPY settings.py .
USER app
CMD ["python", "settings.py"]
```

`solutions/Q39_docker/settings.py`:

```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://localhost/dev"
    debug: bool = False
    workers: int = 2


settings = Settings()
print(settings)
```

`solutions/Q39.sh`:

```sh
#!/bin/sh
# Q39 - A non-root container configured by environment variables
cd "$(dirname "$0")/Q39_docker"
docker build -q -t m23p04-app:1 . >/dev/null
echo "--- who am I inside?"
docker run --rm --entrypoint id m23p04-app:1 -un
echo "--- defaults"
docker run --rm m23p04-app:1
echo "--- production values from the environment"
docker run --rm -e DEBUG=false -e WORKERS=8 -e DATABASE_URL=postgresql://db/prod m23p04-app:1
docker rmi -f m23p04-app:1 >/dev/null
```

Run it: `sh Q39.sh` (needs Docker; it builds the image `m23p04-app:1` and removes it afterwards).

Output (Python 3.14):

```text
--- who am I inside?
app
--- defaults
database_url='postgresql://localhost/dev' debug=False workers=2
--- production values from the environment
database_url='postgresql://db/prod' debug=False workers=8
```

**Rahul's follow-up:** *Why a slim image?* Less to download and a smaller attack surface, with fewer tools for an attacker to use.

</details>


<details>
<summary><b>Q40 · What do you log and measure in production? What is a request ID?</b> <i>(Deployment and operations)</i></summary>

**Taught in:** M14-L03 (logging the right way); M20-L01 (health checks, metrics and dashboards); M20-L02 (tracing).

**Model answer.** Logs say what happened, metrics say how much and how fast (request rate, error rate, latency percentiles), traces follow one request across services, and a health endpoint tells the platform whether to send traffic. Write logs as structured JSON so a tool can filter them, with a level and a *request ID* on every line: a unique ID made at the start of a request and stored in a `contextvars.ContextVar`, so every log line of that request, from any function, carries the same ID, and one request can be found in thousands of lines. (`contextvars` is a small extra here.) Never log passwords, tokens or full card numbers.

`solutions/Q40.py`:

```python
# Q40 - Structured logs with a request ID
import contextvars
import json
import logging
import sys

request_id = contextvars.ContextVar("request_id", default="-")


class JsonFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "request_id": request_id.get(),
            "logger": record.name,
        })


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
log = logging.getLogger("api")
log.addHandler(handler)
log.setLevel(logging.INFO)


def handle(rid):
    request_id.set(rid)             # every log line in this request now carries it
    log.info("enrollment started")
    log.warning("slow query, %d ms", 850)

handle("req-7f3a")
handle("req-91bc")
```

Run it: `python Q40.py`.

Output (Python 3.14):

```text
{"level": "INFO", "message": "enrollment started", "request_id": "req-7f3a", "logger": "api"}
{"level": "WARNING", "message": "slow query, 850 ms", "request_id": "req-7f3a", "logger": "api"}
{"level": "INFO", "message": "enrollment started", "request_id": "req-91bc", "logger": "api"}
{"level": "WARNING", "message": "slow query, 850 ms", "request_id": "req-91bc", "logger": "api"}
```

**Rahul's follow-up:** *Why not use `print` in a service?* No levels, no structure, no destination control, and no request context.

</details>


### G1 to G10 · The ten gotchas

The same code as on the screen in lesson one. For each one: predict the output, then run it, then say the interview line.

<details>
<summary><b>G1 · What is the mutable default argument trap?</b> <i>(Functions, closures and decorators)</i></summary>

**Taught in:** M04-L02 (parameters); M05-L06; M08-L02 (with classes); M08-L06 (dataclasses); M23-L01 gotcha 1.

**Model answer.** A default value is created *once*, when Python reads the `def` line, not on each call. A mutable default such as `tags=[]` is therefore shared by every call that does not pass its own list: the second call starts with the first call's items. The fix: use `None` as the default and create the list inside the function (`if tags is None: tags = []`). Dataclasses refuse the trap and ask for `field(default_factory=list)`.

`solutions/G01_default.py`:

```python
# Gotcha 1 - the mutable default (the same code as lesson one of this module)
def add(name, students=[]):
    students.append(name)
    return students


def add_fixed(name, students=None):
    if students is None:
        students = []
    students.append(name)
    return students


print(add("Lukas"))
print(add("Priya"))
print(add_fixed("Lukas"))
print(add_fixed("Priya"))
```

Run it: `python G01_default.py`.

Output (Python 3.14):

```text
['Lukas']
['Lukas', 'Priya']
['Lukas']
['Priya']
```

**Rahul's follow-up:** *Can a mutable default ever be useful?* Rarely, as a deliberate shared cache. If you do it, say so in a comment, because the next reader will think it is a bug.

</details>


<details>
<summary><b>G2 · What does a list of lambdas made in a loop give when you call them? How do you fix it?</b> <i>(Functions, closures and decorators)</i></summary>

**Taught in:** M09-L03 (closures, pitfall three); M09-L05 (`functools.partial`); M23-L01 gotcha 2.

**Model answer.** Every function says hello to the *last* name: `['Hello, Meera', 'Hello, Meera', 'Hello, Meera']`. This is *late binding*. A closure remembers the *variable* `name`, not the value it had when the function was made, and Python looks the name up when the function runs, after the loop ended on Meera. Fixes: give each function its own value with a default argument (`lambda name=name: ...`), build the function inside another function call, or use `functools.partial`.

`solutions/G02_late.py`:

```python
# Gotcha 2 - late binding in closures (the same code as lesson one of this module)
names = ["Lukas", "Priya", "Meera"]

late = []
for name in names:
    late.append(lambda: "Hello, " + name)

fixed = []
for name in names:
    fixed.append(lambda name=name: "Hello, " + name)

print([f() for f in late])
print([f() for f in fixed])
```

Run it: `python G02_late.py`.

Output (Python 3.14):

```text
['Hello, Meera', 'Hello, Meera', 'Hello, Meera']
['Hello, Lukas', 'Hello, Priya', 'Hello, Meera']
```

**Rahul's follow-up:** *Does the same happen with a `def` inside a loop?* Yes. `def` and `lambda` both create closures that look the name up later.

</details>


<details>
<summary><b>G3 · What is the difference between `is` and `==`?</b> <i>(Language basics)</i></summary>

**Taught in:** M05-L06 (`is` and `==`); M11-L01 (small-number cache); M23-L01 gotcha 3.

**Model answer.** `==` asks "do these two have equal contents?" and can be changed by a class through `__eq__`. `is` asks "are these the very same object?" and cannot be changed. I use `==` for values and `is` only for `None` (`if discount is None`). CPython keeps ready-made objects for the small whole numbers from -5 to 256 and for some short strings, so `is` can look like it works on them, but that is an implementation detail and I never depend on it.

`solutions/G03_is.py`:

```python
# Gotcha 3 - is against == (the same code as lesson one of this module)
a = int("100")
b = int("100")
c = int("1000")
d = int("1000")
print(a == b, a is b)
print(c == d, c is d)

x = [1, 2]
y = [1, 2]
print(x == y, x is y)
```

Run it: `python G03_is.py`.

Output (Python 3.14):

```text
True True
True False
True False
```

**Rahul's follow-up:** *Why `is None` and not `== None`?* `None` exists once, so `is` is the exact test, and nobody can fool it. A class can define an `__eq__` that says "equal" to anything, but nobody can change what `is` means.

</details>


<details>
<summary><b>G4 · Explain shallow copy against deep copy.</b> <i>(Data structures)</i></summary>

**Taught in:** M05-L06 (copying: `copy`, `deepcopy`, and the grid trap); M23-L01 gotcha 4.

**Model answer.** A shallow copy (`.copy()`, `list(x)`, `x[:]`, `copy.copy`) copies only the outer container, so both containers still point at the *same* inner objects. A deep copy (`copy.deepcopy`) copies everything inside too, at a higher cost. In the example, after `batches[0].append("Meera")`, the shallow copy shows Meera and the deep copy does not. Plain assignment (`alias = batches`) copies nothing; it is a second label. And `[[0] * 3] * 3` repeats one row three times, so setting the first seat of one row sets it in all three; build the rows with a comprehension instead.

`solutions/G04_copy.py`:

```python
# Gotcha 4 - shallow against deep copy (the same code as lesson one of this module)
import copy

batches = [["Lukas", "Priya"], ["Asha"]]
shallow = batches.copy()
deep = copy.deepcopy(batches)
batches[0].append("Meera")
print(shallow[0])
print(deep[0])

grid = [[0] * 3] * 3
grid[0][0] = 1
print(grid)
```

Run it: `python G04_copy.py`.

Output (Python 3.14):

```text
['Lukas', 'Priya', 'Meera']
['Lukas', 'Priya']
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
```

**Rahul's follow-up:** *When is a shallow copy enough?* When the items inside are immutable (numbers, strings, tuples of those). Then nothing shared can change.

</details>


<details>
<summary><b>G5 · What goes wrong if you remove items from a list while looping over it?</b> <i>(Data structures)</i></summary>

**Taught in:** M05-L03 (dictionary changed size); M05-L05 (comprehensions); M23-L01 gotcha 5.

**Model answer.** The loop walks by position. When you remove an item, the list closes up, so the next item moves into the position the loop already passed, and the loop silently skips it. Lists give no error, which is worse. A dictionary does raise `RuntimeError: dictionary changed size during iteration`. The fix: build a new list with a comprehension, loop over a copy, or assign into the slice (`items[:] = [...]`) when the same list object must be kept.

`solutions/G05_loop.py`:

```python
# Gotcha 5 - changing a list while looping (the same code as lesson one of this module)
lessons = ["intro", "demo 1", "demo 2", "demo 3", "wrap-up"]
for item in lessons:
    if item.startswith("demo"):
        lessons.remove(item)
print(lessons)

lessons = ["intro", "demo 1", "demo 2", "demo 3", "wrap-up"]
kept = [item for item in lessons if not item.startswith("demo")]
print(kept)
```

Run it: `python G05_loop.py`.

Output (Python 3.14):

```text
['intro', 'demo 2', 'wrap-up']
['intro', 'wrap-up']
```

**Rahul's follow-up:** *How do you delete keys from a dictionary safely?* Loop over `list(d)` or `list(d.items())`, or build a new dictionary with a dict comprehension.

</details>


<details>
<summary><b>G6 · What happens when you run `+=` on a list inside a tuple?</b> <i>(Data structures)</i></summary>

**Taught in:** M05-L02 (tuples); M05-L06 (a tuple can hold a list); M23-L01 gotcha 6 (the hook).

**Model answer.** Both things happen. `+=` on a list first changes the list in place, which works because lists are mutable. Then Python assigns the result back into `t[2]`, which fails because a tuple does not support item assignment. So you get a `TypeError`, *and* the list has changed. To avoid the error, call `t[2].extend([5, 6])`.

`solutions/G06_hook.py`:

```python
# Gotcha 6 - plus-equals inside a tuple (the hook) (the same code as lesson one of this module)
row = (1, [2, 3])
try:
    row[1] += [4]
except TypeError as error:
    print("error:", error)
print(row)
```

`solutions/G06_tuple.py`:

```python
# Gotcha 6 - plus-equals inside a tuple, step by step (the same code as lesson one of this module)
row = (1, [2, 3])
inner = row[1]
inner += [4]
print(row)
row[1] = inner
```

Run it: `python G06_hook.py` and `python G06_tuple.py`.

Output (Python 3.14):

```text
error: 'tuple' object does not support item assignment
(1, [2, 3, 4])
```

```text
(1, [2, 3, 4])
Traceback (most recent call last):
  File "G06_tuple.py", line 6, in <module>
    row[1] = inner
    ~~~^^^
TypeError: 'tuple' object does not support item assignment
```

**Rahul's follow-up:** *So is a tuple really immutable?* The tuple cannot swap what it holds, but a mutable object inside it can still change itself.

</details>


<details>
<summary><b>G7 · Why does `0.1 + 0.2 == 0.3` give `False`? What do `//`, `%` and `round()` do?</b> <i>(Language basics)</i></summary>

**Taught in:** M02-L02 (numbers); M23-L01 gotcha 7.

**Model answer.** Floats are stored in binary, and 0.1 has no exact binary form, so `0.1 + 0.2` is `0.30000000000000004`. I compare floats with `math.isclose`, and keep money in whole units (whole rupees, as allcsvideos does) or in `Decimal`. Floor division `//` rounds *down*, so `-7 // 2` is `-4`, and `%` takes the sign of the right-hand number, so `-7 % 3` is `2`. Together they always satisfy `a == a // b * b + a % b`. `round()` sends an exact tie to the even neighbour (banker's rounding): `round(0.5)` is `0`, `round(1.5)` is `2`, `round(2.5)` is `2`.

`solutions/G07_numbers.py`:

```python
# Gotcha 7 - numbers (the same code as lesson one of this module)
import math

print(-7 // 2)
print(-7 % 3)
print(round(0.5), round(1.5), round(2.5))
print(0.1 + 0.2 == 0.3)
print(math.isclose(0.1 + 0.2, 0.3))
```

Run it: `python G07_numbers.py`.

Output (Python 3.14):

```text
-4
2
0 2 2
False
True
```

**Rahul's follow-up:** *How would you store the price Rs 499.50?* As a whole number of the smallest unit (49950 paise) or as a `Decimal("499.50")`, never as `499.5` in a float, because totals of floats drift.

</details>


<details>
<summary><b>G8 · What is the difference between a class attribute and an instance attribute?</b> <i>(Object-oriented programming)</i></summary>

**Taught in:** M08-L02 (attributes and methods); M23-L01 gotcha 8.

**Model answer.** A class attribute lives on the class and every object reads the same one. An instance attribute, set in `__init__` through `self`, belongs to one object. *Appending* to a shared list changes it for everybody (the example's `sql.students` shows Lukas, who joined only Python). But `c.total += 1` on a number reads the class value, adds one and *assigns* the answer to the object, which creates a new instance attribute `c.total` and leaves `Counter.total` at 0. Per-object data belongs in `__init__`.

`solutions/G08_attrs.py`:

```python
# Gotcha 8 - class and instance attributes (the same code as lesson one of this module)
class Course:
    students = []


python = Course()
sql = Course()
python.students.append("Lukas")
print(sql.students)


class Counter:
    total = 0


c = Counter()
c.total += 1
print(c.total, Counter.total)
```

Run it: `python G08_attrs.py`.

Output (Python 3.14):

```text
['Lukas']
1 0
```

**Rahul's follow-up:** *How would you change the tax for every course?* Assign on the class: `Course.tax_percent = 5`. Objects that have their own `tax_percent` keep theirs.

</details>


<details>
<summary><b>G9 · What does `__slots__` do?</b> <i>(Memory, the GIL and performance)</i></summary>

**Taught in:** M10-L03 (TypedDict, slots, NamedTuple and pattern matching); M23-L01 gotcha 9.

**Model answer.** An ordinary object keeps its attributes in a hidden dictionary, so any new name is accepted, even a typo: the example's `a.pirce = 90` went straight in. `__slots__ = ("price",)` gives the class exactly those places and removes the dictionary, so `b.pirce = 90` is an `AttributeError`, and Python even suggests "Did you mean: 'price'?". It also saves memory per object (module ten, lesson three, measured it). The price is flexibility: you cannot add other attributes, and multiple inheritance with slots needs care. Dataclasses offer `slots=True`.

`solutions/G09_slots.py`:

```python
# Gotcha 9 - __slots__ (the same code as lesson one of this module)
class Plain:
    def __init__(self, price):
        self.price = price


class Slim:
    __slots__ = ("price",)

    def __init__(self, price):
        self.price = price


a = Plain(100)
a.pirce = 90
print(a.__dict__)
b = Slim(100)
b.pirce = 90
```

Run it: `python G09_slots.py`.

Output (Python 3.14):

```text
{'price': 100, 'pirce': 90}
Traceback (most recent call last):
  File "G09_slots.py", line 18, in <module>
    b.pirce = 90
    ^^^^^^^
AttributeError: 'Slim' object has no attribute 'pirce' and no __dict__ for setting new attributes. Did you mean: 'price'?
```

**Rahul's follow-up:** *When is it worth it?* When you create very many small objects. Otherwise the saving is small and the restriction is annoying.

</details>


<details>
<summary><b>G10 · What is the GIL? Do Python threads speed up CPU work?</b> <i>(Memory, the GIL and performance)</i></summary>

**Taught in:** M11-L03 (the GIL and free-threaded Python); M12-L02 (threads); M23-L01 gotcha 10.

**Model answer.** In the normal build of CPython, the Global Interpreter Lock lets only one thread run Python code at a time. So threads do *not* speed up computing: in the example, four workers take about as long as one. Threads do help when the work is *waiting* (network, disk), because a waiting thread lets go of the lock. For computing, use processes (`ProcessPoolExecutor`), as module twelve, lesson three showed. Python 3.14 also ships an optional free-threaded build without the lock, which module eleven measured.

`solutions/G10_gil.py`:

```python
# Gotcha 10 - the GIL (the same code as lesson one of this module)
import sys
import time
from concurrent.futures import ThreadPoolExecutor


def count(n):
    while n:
        n -= 1


def timed(workers, total=120_000_000):
    start = time.perf_counter()
    with ThreadPoolExecutor(workers) as pool:
        for _ in range(workers):
            pool.submit(count, total // workers)
    return time.perf_counter() - start


print("GIL on:", sys._is_gil_enabled())
print(f"1 worker:  {timed(1):.2f} s")
print(f"4 workers: {timed(4):.2f} s")
```

Run it: `python G10_gil.py`.

Output (Python 3.14):

```text
GIL on: True
1 worker:  5.08 s
4 workers: 3.31 s
```

*Timing note: wall-clock time is noisy when other programs share the CPU, so the example also prints CPU time and "cores busy".*

**Rahul's follow-up:** *Why not just remove the GIL?* The free-threaded build does exactly that, but it needs thread-safe versions of everything and slows single-threaded code a little, so it is still a choice, not the default.

</details>


---

**Score yourself:** answer ten questions out loud without looking. If you can give the rule, the example and the trap for at least eight of them, you are ready for the screening round. Re-read the lesson named under any question you could not answer, then say the answer again out loud.

---

# Part 2 · 10 Build-It-Yourself Tasks

Each task has a story, requirements, hints and a reference solution with tests. **Write your own solution, and your own tests, before you open the hints.** The tasks grow from small to large. The tests of the reference solutions all pass; the output is pasted below each one.

**Suggested way to work:** make a folder `task01/`, write the tests *first* from the requirements (module 13, lesson 5), watch them fail, then write the code until they pass. Run with `python -m pytest -v`. For tasks 9 and 10, start the containers from "How to work" first.

| # | Task | Size | Skills | Taught in |
|---|---|---|---|---|
| 1 | Word statistics | small | strings, `re`, `Counter`, sorting with a key | M02-L03, M05-L03, M05-L05, M09-L05 |
| 2 | A retry decorator | small | decorators with arguments, `functools.wraps`, injecting a dependency to test fast | M09-L03, M09-B05, M18-L04 |
| 3 | An LRU cache | small | classes, dunder methods, `OrderedDict`, O(1) operations | M08-L05, M09-L05 |
| 4 | A lazy log analyser | small-medium | generators, pipelines, `heapq`, `Counter`, files read line by line | M09-L01, M09-L02, M06-L01, M06-B03 |
| 5 | A rate limiter | medium | `deque`, sliding window, an injectable clock, test design | M18-L04, M09-L05 |
| 6 | A cart with discount rules | medium | dataclasses, abstract classes, composition, whole-rupee arithmetic | M08-L04, M08-L06, M13-B07 |
| 7 | An async link checker | medium | asyncio, `gather`, `Semaphore`, `wait_for`, retries | M12-L04, M12-L05, M12-B06 |
| 8 | A course catalogue API | medium-large | FastAPI, pydantic, status codes, pagination, dependency overrides in tests | M15-L01 to M15-L06, M15-B08 |
| 9 | Enrollments in Postgres | large | SQLAlchemy 2, constraints, transactions, `SELECT ... FOR UPDATE`, avoiding N+1 | M16-L01 to M16-L05, M20-L04 |
| 10 | A short-link service with a cache | largest | FastAPI + Postgres + Redis: cache-aside, invalidation, idempotency, rate limit, counters | M15, M16, M18-L01, M18-L04, M19-L02 |

## Task 1 · Word statistics (small)

*Priya wants to know which words appear most in the lesson notes of allcsvideos.*

**Skills:** strings, `re`, `Counter`, sorting with a key. **Taught in:** M02-L03, M05-L03, M05-L05, M09-L05.

**Requirements**

- `words(text)` returns the lower-case words, with punctuation removed (keep apostrophes and digits inside words).
- `top_words(text, n=3)` returns the `n` most common words as `(word, count)` pairs, ignoring a set of stop words (`a`, `the`, `is`, ...).
- Ties are broken alphabetically, so the answer is always the same.
- A negative `n` raises `ValueError`; empty text gives an empty list.
- `longest_word(text)` returns the longest word, or `None` for no words.

<details>
<summary><b>Hints for task 1</b></summary>

- `re.findall(r"[a-z0-9']+", text.lower())` does the splitting.
- `Counter` counts. Sort the items with `key=lambda item: (-item[1], item[0])` to get count first, then name.
- `max(words, key=len, default=None)`.

</details>

<details>
<summary><b>Reference solution for task 1</b></summary>

The files are in `solutions/T01_word_stats/`. From inside `solutions/`, run `python -m pytest T01_word_stats -v`.

`solutions/T01_word_stats/word_stats.py`:

```python
"""Task 1 - word statistics for a block of text."""
import re
from collections import Counter

STOP_WORDS = frozenset({"a", "an", "and", "the", "is", "of", "to", "in", "it", "for", "on"})

_WORD = re.compile(r"[a-z0-9']+")


def words(text: str) -> list[str]:
    """Lower-case words with punctuation removed."""
    return _WORD.findall(text.lower())


def top_words(text: str, n: int = 3, stop_words=STOP_WORDS) -> list[tuple[str, int]]:
    """The n most common words, ignoring stop words.

    Ties are broken alphabetically so the result is always the same.
    """
    if n < 0:
        raise ValueError("n must not be negative")
    counts = Counter(w for w in words(text) if w not in stop_words)
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:n]


def longest_word(text: str) -> str | None:
    found = words(text)
    return max(found, key=len, default=None)   # first of the longest wins
```

`solutions/T01_word_stats/test_t01.py`:

```python
import pytest

from word_stats import longest_word, top_words, words


def test_words_lowercases_and_strips_punctuation():
    assert words("Hello, World! It's 2026.") == ["hello", "world", "it's", "2026"]


def test_top_words_counts_and_ignores_stop_words():
    text = "Python is fun. The fun of Python is learning Python."
    assert top_words(text, 2) == [("python", 3), ("fun", 2)]


def test_ties_are_alphabetical():
    assert top_words("y x z y x z", 3) == [("x", 2), ("y", 2), ("z", 2)]


def test_empty_text_and_zero():
    assert top_words("") == []
    assert top_words("x y", 0) == []


def test_negative_n_is_an_error():
    with pytest.raises(ValueError):
        top_words("x", -1)


def test_longest_word():
    assert longest_word("a bb ccc dd eee") == "ccc"
    assert longest_word("") is None
```

Test output (Python 3.14):

```text
T01_word_stats/test_t01.py::test_words_lowercases_and_strips_punctuation PASSED
T01_word_stats/test_t01.py::test_top_words_counts_and_ignores_stop_words PASSED
T01_word_stats/test_t01.py::test_ties_are_alphabetical PASSED
T01_word_stats/test_t01.py::test_empty_text_and_zero PASSED
T01_word_stats/test_t01.py::test_negative_n_is_an_error PASSED
T01_word_stats/test_t01.py::test_longest_word PASSED
============================== 6 passed in 2.20s ===============================
```

</details>


## Task 2 · A retry decorator (small)

*Lukas's code calls a flaky payment gateway. He wants `@retry(...)` above the function.*

**Skills:** decorators with arguments, `functools.wraps`, injecting a dependency to test fast. **Taught in:** M09-L03, M09-B05, M18-L04.

**Requirements**

- `@retry(times=3, delay=0.1, factor=2.0, exceptions=(Exception,), sleep=time.sleep)`.
- Call the function up to `times` times. Wait `delay`, then `delay * factor`, and so on, between tries.
- Retry only the listed exceptions; any other error travels straight out.
- After the last failed try, re-raise the last error, and do not sleep after it.
- Keep the function's `__name__` and docstring.
- `times < 1` raises `ValueError` when the decorator is created.
- The `sleep` parameter lets the tests run instantly.

<details>
<summary><b>Hints for task 2</b></summary>

- Three layers: settings, then the function, then each call.
- Loop `for attempt in range(1, times + 1)`; on the last attempt re-raise with a bare `raise`.
- A test passes `sleep=slept.append` and then checks the list of waits.

</details>

<details>
<summary><b>Reference solution for task 2</b></summary>

The files are in `solutions/T02_retry/`. From inside `solutions/`, run `python -m pytest T02_retry -v`.

`solutions/T02_retry/retry.py`:

```python
"""Task 2 - a retry decorator with exponential backoff."""
import functools
import time


def retry(times: int = 3, delay: float = 0.1, factor: float = 2.0,
          exceptions=(Exception,), sleep=time.sleep):
    """Call the function up to `times` times.

    Waits delay, delay*factor, delay*factor**2 ... between tries and re-raises
    the last error. `sleep` can be replaced in tests so they run instantly.
    """
    if times < 1:
        raise ValueError("times must be at least 1")

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
                    sleep(wait)
                    wait *= factor
        return wrapper
    return decorator
```

`solutions/T02_retry/test_t02.py`:

```python
import pytest

from retry import retry


class Flaky:
    def __init__(self, failures, error=ConnectionError):
        self.failures, self.error, self.calls = failures, error, 0

    def __call__(self):
        self.calls += 1
        if self.calls <= self.failures:
            raise self.error("down")
        return "ok"


def test_succeeds_first_time_without_sleeping():
    slept = []
    func = retry(sleep=slept.append)(Flaky(0))
    assert func() == "ok" and slept == []


def test_retries_with_growing_waits():
    slept = []
    flaky = Flaky(2)
    func = retry(times=4, delay=1, factor=3, sleep=slept.append)(flaky)
    assert func() == "ok"
    assert flaky.calls == 3 and slept == [1, 3]


def test_gives_up_and_reraises_the_last_error():
    slept = []
    flaky = Flaky(10)
    with pytest.raises(ConnectionError):
        retry(times=3, sleep=slept.append)(flaky)()
    assert flaky.calls == 3 and len(slept) == 2     # no sleep after the final failure


def test_other_errors_are_not_retried():
    flaky = Flaky(5, error=KeyError)
    with pytest.raises(KeyError):
        retry(times=3, exceptions=(ConnectionError,), sleep=lambda s: None)(flaky)()
    assert flaky.calls == 1


def test_keeps_the_name_and_docstring():
    @retry()
    def fetch():
        "Fetch data."
    assert fetch.__name__ == "fetch" and fetch.__doc__ == "Fetch data."


def test_times_must_be_positive():
    with pytest.raises(ValueError):
        retry(times=0)
```

Test output (Python 3.14):

```text
T02_retry/test_t02.py::test_succeeds_first_time_without_sleeping PASSED
T02_retry/test_t02.py::test_retries_with_growing_waits PASSED
T02_retry/test_t02.py::test_gives_up_and_reraises_the_last_error PASSED
T02_retry/test_t02.py::test_other_errors_are_not_retried PASSED
T02_retry/test_t02.py::test_keeps_the_name_and_docstring PASSED
T02_retry/test_t02.py::test_times_must_be_positive PASSED
============================== 6 passed in 1.53s ===============================
```

</details>


## Task 3 · An LRU cache (small)

*Meera wants a cache that keeps only the most recently used results, with constant-time `get` and `put`.*

**Skills:** classes, dunder methods, `OrderedDict`, O(1) operations. **Taught in:** M08-L05, M09-L05.

**Requirements**

- `LRUCache(capacity)` with `get(key, default=None)`, `put(key, value)`, `len(cache)`, `key in cache`, and `keys()` (least to most recently used).
- `get` and `put` both count as "using" a key. `in` does not.
- When `put` makes the cache bigger than `capacity`, drop the least recently used key.
- Keep `hits` and `misses` counters that `get` updates.
- `capacity < 1` raises `ValueError`.

<details>
<summary><b>Hints for task 3</b></summary>

- `collections.OrderedDict` has `move_to_end(key)` and `popitem(last=False)`.
- Write `__len__` and `__contains__`.
- Try your design with a capacity of 2 and the sequence put a, put b, get a, put c on paper first.

</details>

<details>
<summary><b>Reference solution for task 3</b></summary>

The files are in `solutions/T03_lru_cache/`. From inside `solutions/`, run `python -m pytest T03_lru_cache -v`.

`solutions/T03_lru_cache/lru.py`:

```python
"""Task 3 - a least-recently-used cache with O(1) get and put."""
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self._data: OrderedDict = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key, default=None):
        if key not in self._data:
            self.misses += 1
            return default
        self.hits += 1
        self._data.move_to_end(key)             # most recently used goes last
        return self._data[key]

    def put(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = value
        if len(self._data) > self.capacity:
            self._data.popitem(last=False)      # drop the least recently used

    def __len__(self):
        return len(self._data)

    def __contains__(self, key):               # does not count as a use
        return key in self._data

    def keys(self):
        """Keys from least to most recently used."""
        return list(self._data)
```

`solutions/T03_lru_cache/test_t03.py`:

```python
import pytest

from lru import LRUCache


def test_basic_get_put():
    cache = LRUCache(2)
    cache.put("a", 1)
    assert cache.get("a") == 1
    assert cache.get("zzz") is None
    assert cache.get("zzz", 0) == 0


def test_evicts_least_recently_used():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")                  # a is now fresh, b is the oldest
    cache.put("c", 3)
    assert "b" not in cache and "a" in cache and "c" in cache
    assert cache.keys() == ["a", "c"]


def test_put_existing_key_updates_and_refreshes():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    cache.put("c", 3)
    assert cache.get("a") == 10 and "b" not in cache
    assert len(cache) == 2


def test_hit_and_miss_counters():
    cache = LRUCache(1)
    cache.put("a", 1)
    cache.get("a"); cache.get("a"); cache.get("b")
    assert (cache.hits, cache.misses) == (2, 1)


def test_contains_does_not_refresh():
    cache = LRUCache(2)
    cache.put("a", 1); cache.put("b", 2)
    assert "a" in cache
    cache.put("c", 3)               # a was only looked at with `in`, so it goes
    assert "a" not in cache


def test_capacity_must_be_positive():
    with pytest.raises(ValueError):
        LRUCache(0)
```

Test output (Python 3.14):

```text
T03_lru_cache/test_t03.py::test_basic_get_put PASSED
T03_lru_cache/test_t03.py::test_evicts_least_recently_used PASSED
T03_lru_cache/test_t03.py::test_put_existing_key_updates_and_refreshes PASSED
T03_lru_cache/test_t03.py::test_hit_and_miss_counters PASSED
T03_lru_cache/test_t03.py::test_contains_does_not_refresh PASSED
T03_lru_cache/test_t03.py::test_capacity_must_be_positive PASSED
============================== 6 passed in 1.93s ===============================
```

</details>


## Task 4 · A lazy log analyser (small-medium)

*Rahul hands Asha an access log that is too big to load. Each line looks like `GET /courses 200 12` (method, path, status, milliseconds).*

**Skills:** generators, pipelines, `heapq`, `Counter`, files read line by line. **Taught in:** M09-L01, M09-L02, M06-L01, M06-B03.

**Requirements**

- `parse_line(line)` returns an `Entry` (a frozen dataclass), or `None` for a broken line (wrong number of parts, non-numeric status or time).
- `entries(lines)` is a *generator* that yields one `Entry` at a time and skips broken lines silently.
- `errors(stream)` keeps only status 500 and above; `slowest(stream, n)` returns the `n` slowest; `status_counts(stream)` counts by hundreds (200, 300, ...).
- `read_file(path)` yields lines one by one without loading the file.
- Everything must work on an endless stream (prove it with `itertools.islice`).

<details>
<summary><b>Hints for task 4</b></summary>

- A generator expression `(e for e in stream if ...)` is a one-line stage.
- `heapq.nlargest(n, stream, key=...)` never keeps more than `n` items.
- `yield from handle` inside `with open(...)`.

</details>

<details>
<summary><b>Reference solution for task 4</b></summary>

The files are in `solutions/T04_log_stream/`. From inside `solutions/`, run `python -m pytest T04_log_stream -v`.

`solutions/T04_log_stream/logstream.py`:

```python
"""Task 4 - analyse a huge log file lazily with generators."""
import heapq
from collections import Counter
from dataclasses import dataclass
from itertools import islice


@dataclass(frozen=True)
class Entry:
    method: str
    path: str
    status: int
    ms: int


def parse_line(line: str) -> Entry | None:
    """'GET /courses 200 12' -> Entry, or None for a broken line."""
    parts = line.split()
    if len(parts) != 4:
        return None
    method, path, status, ms = parts
    if not (status.isdigit() and ms.isdigit()):
        return None
    return Entry(method, path, int(status), int(ms))


def entries(lines):
    """Lazy: yields one Entry at a time, silently skipping bad lines."""
    for line in lines:
        entry = parse_line(line)
        if entry is not None:
            yield entry


def errors(stream):
    return (e for e in stream if e.status >= 500)


def slowest(stream, n=3):
    """Top n slowest entries without keeping the whole stream in memory."""
    return heapq.nlargest(n, stream, key=lambda e: e.ms)


def status_counts(stream):
    return Counter(e.status // 100 * 100 for e in stream)


def read_file(path):
    with open(path) as handle:
        yield from handle               # one line at a time


def first(stream, n):
    return list(islice(stream, n))
```

`solutions/T04_log_stream/test_t04.py`:

```python
import inspect

from logstream import Entry, entries, errors, first, parse_line, read_file, slowest, status_counts

LINES = [
    "GET /courses 200 12",
    "garbage",
    "POST /enroll 201 40",
    "GET /courses 500 300",
    "GET /x abc 5",
    "GET /pay 503 120",
]


def test_parse_line():
    assert parse_line("GET /a 200 7") == Entry("GET", "/a", 200, 7)
    assert parse_line("nonsense") is None
    assert parse_line("GET /a x 7") is None


def test_entries_skips_bad_lines():
    assert [e.path for e in entries(LINES)] == ["/courses", "/enroll", "/courses", "/pay"]


def test_entries_is_lazy():
    assert inspect.isgenerator(entries(LINES))

    def endless():
        while True:
            yield "GET /a 200 1"

    assert len(first(entries(endless()), 5)) == 5        # works on an endless stream


def test_errors_and_slowest():
    assert [e.status for e in errors(entries(LINES))] == [500, 503]
    assert [e.ms for e in slowest(entries(LINES), 2)] == [300, 120]


def test_status_counts():
    assert dict(status_counts(entries(LINES))) == {200: 2, 500: 2}


def test_read_file(tmp_path):
    f = tmp_path / "access.log"
    f.write_text("\n".join(LINES) + "\n")
    assert len(list(entries(read_file(f)))) == 4
```

Test output (Python 3.14):

```text
T04_log_stream/test_t04.py::test_parse_line PASSED
T04_log_stream/test_t04.py::test_entries_skips_bad_lines PASSED
T04_log_stream/test_t04.py::test_entries_is_lazy PASSED
T04_log_stream/test_t04.py::test_errors_and_slowest PASSED
T04_log_stream/test_t04.py::test_status_counts PASSED
T04_log_stream/test_t04.py::test_read_file PASSED
============================== 6 passed in 1.72s ===============================
```

</details>


## Task 5 · A rate limiter (medium)

*The allcsvideos login endpoint must allow at most 3 attempts per user per minute.*

**Skills:** `deque`, sliding window, an injectable clock, test design. **Taught in:** M18-L04, M09-L05.

**Requirements**

- `RateLimiter(limit, window, clock=time.monotonic)`; `allow(key)` returns `True` or `False`.
- A sliding window: only calls in the last `window` seconds count.
- Each key has its own budget.
- `retry_after(key)` returns the seconds until the next call would be allowed (0 when allowed now).
- Bad settings raise `ValueError`.
- The tests use a fake clock object, so they never sleep.

<details>
<summary><b>Hints for task 5</b></summary>

- Keep a `deque` of call times per key; drop old ones from the left.
- A call exactly `window` seconds old no longer counts.
- `defaultdict(deque)` makes the per-key storage easy.

</details>

<details>
<summary><b>Reference solution for task 5</b></summary>

The files are in `solutions/T05_rate_limiter/`. From inside `solutions/`, run `python -m pytest T05_rate_limiter -v`.

`solutions/T05_rate_limiter/limiter.py`:

```python
"""Task 5 - a sliding-window rate limiter with an injectable clock."""
import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self, limit: int, window: float, clock=time.monotonic):
        if limit < 1 or window <= 0:
            raise ValueError("limit must be >= 1 and window > 0")
        self.limit, self.window, self.clock = limit, window, clock
        self._calls: dict[str, deque] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = self.clock()
        calls = self._calls[key]
        while calls and calls[0] <= now - self.window:   # forget calls outside the window
            calls.popleft()
        if len(calls) >= self.limit:
            return False
        calls.append(now)
        return True

    def retry_after(self, key: str) -> float:
        """Seconds until the next call would be allowed (0 if allowed now)."""
        calls = self._calls[key]
        if len(calls) < self.limit:
            return 0.0
        return max(0.0, calls[0] + self.window - self.clock())
```

`solutions/T05_rate_limiter/test_t05.py`:

```python
import pytest

from limiter import RateLimiter


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def test_allows_up_to_limit_then_blocks():
    rl = RateLimiter(3, 60, FakeClock())
    assert [rl.allow("asha") for _ in range(5)] == [True, True, True, False, False]


def test_keys_are_independent():
    rl = RateLimiter(1, 60, FakeClock())
    assert rl.allow("asha") and rl.allow("lukas")
    assert not rl.allow("asha")


def test_window_slides():
    clock = FakeClock()
    rl = RateLimiter(2, 10, clock)
    assert rl.allow("k")            # t=0
    clock.now = 6
    assert rl.allow("k")            # t=6
    clock.now = 9
    assert not rl.allow("k")        # both still inside the window
    clock.now = 10.5                # the call at t=0 has slid out
    assert rl.allow("k")
    assert not rl.allow("k")


def test_retry_after():
    clock = FakeClock()
    rl = RateLimiter(1, 10, clock)
    assert rl.retry_after("k") == 0
    rl.allow("k")
    clock.now = 4
    assert rl.retry_after("k") == 6
    clock.now = 10
    assert rl.retry_after("k") == 0 and rl.allow("k")


def test_rejects_bad_settings():
    with pytest.raises(ValueError):
        RateLimiter(0, 10)
    with pytest.raises(ValueError):
        RateLimiter(1, 0)
```

Test output (Python 3.14):

```text
T05_rate_limiter/test_t05.py::test_allows_up_to_limit_then_blocks PASSED
T05_rate_limiter/test_t05.py::test_keys_are_independent PASSED
T05_rate_limiter/test_t05.py::test_window_slides PASSED
T05_rate_limiter/test_t05.py::test_retry_after PASSED
T05_rate_limiter/test_t05.py::test_rejects_bad_settings PASSED
============================== 5 passed in 2.19s ===============================
```

</details>


## Task 6 · A cart with discount rules (medium)

*Asha's shop sells courses. Marketing keeps inventing new discount rules, so each rule must be its own small class.*

**Skills:** dataclasses, abstract classes, composition, whole-rupee arithmetic. **Taught in:** M08-L04, M08-L06, M13-B07.

**Requirements**

- `Item(name, price, qty=1)`: a frozen dataclass; negative price or `qty < 1` raises `ValueError`; `total` is a property.
- `Rule` is an abstract class with a `discount(items, subtotal)` method. Write `PercentOff(percent, min_subtotal=0)`, `FlatOff(amount, min_subtotal=0)` and `BundleFree(needed=3)` (the cheapest item is free).
- `Cart.add(item)` merges quantities when the same course is added twice.
- `Cart.discounts()` lists `(label, rupees)` for each rule that applied; the total discount never exceeds the subtotal.
- `Cart.summary()` returns subtotal, discount, net, GST (18 percent of the net) and total. All money is whole rupees (`//`).

<details>
<summary><b>Hints for task 6</b></summary>

- `@dataclass(frozen=True)` for items and rules; `field(default_factory=list)` for the cart's lists.
- Track `left = subtotal` while you apply the rules, and cap each discount at `left`.
- A new rule in a test: subclass `Rule` and the cart works with it unchanged.

</details>

<details>
<summary><b>Reference solution for task 6</b></summary>

The files are in `solutions/T06_pricing/`. From inside `solutions/`, run `python -m pytest T06_pricing -v`.

`solutions/T06_pricing/pricing.py`:

```python
"""Task 6 - a cart with discount rules (OOP: dataclass, ABC, composition).

All money is whole rupees (int). GST is 18 percent of the discounted total.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

GST_PERCENT = 18


@dataclass(frozen=True)
class Item:
    name: str
    price: int
    qty: int = 1

    def __post_init__(self):
        if self.price < 0 or self.qty < 1:
            raise ValueError("price must be >= 0 and qty >= 1")

    @property
    def total(self) -> int:
        return self.price * self.qty


class Rule(ABC):
    label: str

    @abstractmethod
    def discount(self, items: list[Item], subtotal: int) -> int:
        """Rupees off. Must be 0 when the rule does not apply."""


@dataclass(frozen=True)
class PercentOff(Rule):
    percent: int
    min_subtotal: int = 0

    @property
    def label(self):
        return f"{self.percent}% off"

    def discount(self, items, subtotal):
        return subtotal * self.percent // 100 if subtotal >= self.min_subtotal else 0


@dataclass(frozen=True)
class FlatOff(Rule):
    amount: int
    min_subtotal: int = 0

    @property
    def label(self):
        return f"Rs {self.amount} off"

    def discount(self, items, subtotal):
        return self.amount if subtotal >= self.min_subtotal else 0


@dataclass(frozen=True)
class BundleFree(Rule):
    """Buy `needed` different items, and the cheapest one is free."""
    needed: int = 3
    label: str = "cheapest of the bundle free"

    def discount(self, items, subtotal):
        if len(items) < self.needed:
            return 0
        return min(item.price for item in items)


@dataclass
class Cart:
    items: list[Item] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)

    def add(self, item: Item) -> None:
        for index, existing in enumerate(self.items):
            if existing.name == item.name:          # same course twice: add the quantities
                self.items[index] = Item(item.name, existing.price, existing.qty + item.qty)
                return
        self.items.append(item)

    @property
    def subtotal(self) -> int:
        return sum(item.total for item in self.items)

    def discounts(self) -> list[tuple[str, int]]:
        """Each rule is applied to the subtotal; the sum never exceeds the subtotal."""
        left = self.subtotal
        applied = []
        for rule in self.rules:
            amount = min(rule.discount(self.items, self.subtotal), left)
            if amount > 0:
                applied.append((rule.label, amount))
                left -= amount
        return applied

    def summary(self) -> dict:
        discount = sum(amount for _, amount in self.discounts())
        net = self.subtotal - discount
        gst = net * GST_PERCENT // 100
        return {"subtotal": self.subtotal, "discount": discount, "net": net,
                "gst": gst, "total": net + gst}
```

`solutions/T06_pricing/test_t06.py`:

```python
import pytest

from pricing import BundleFree, Cart, FlatOff, Item, PercentOff, Rule


def cart(*items, rules=()):
    c = Cart(rules=list(rules))
    for item in items:
        c.add(item)
    return c


def test_item_total_and_validation():
    assert Item("Python", 499, 2).total == 998
    with pytest.raises(ValueError):
        Item("Python", -1)
    with pytest.raises(ValueError):
        Item("Python", 499, 0)


def test_adding_same_course_merges_quantity():
    c = cart(Item("Python", 499), Item("Python", 499, 2))
    assert len(c.items) == 1 and c.items[0].qty == 3


def test_no_rules_only_gst():
    assert cart(Item("Python", 500)).summary() == {
        "subtotal": 500, "discount": 0, "net": 500, "gst": 90, "total": 590}


def test_percent_with_minimum():
    rule = PercentOff(10, min_subtotal=1000)
    assert cart(Item("A", 500), rules=[rule]).summary()["discount"] == 0
    assert cart(Item("A", 1000), rules=[rule]).summary()["discount"] == 100


def test_rules_stack_and_are_listed():
    c = cart(Item("A", 600), Item("B", 400), rules=[PercentOff(10), FlatOff(50)])
    assert c.discounts() == [("10% off", 100), ("Rs 50 off", 50)]
    assert c.summary()["net"] == 850


def test_discount_never_exceeds_the_subtotal():
    c = cart(Item("A", 100), rules=[FlatOff(80), FlatOff(80)])
    assert c.summary()["net"] == 0 and c.summary()["total"] == 0


def test_bundle_cheapest_free():
    c = cart(Item("A", 500), Item("B", 300), Item("C", 800), rules=[BundleFree(3)])
    assert c.discounts() == [("cheapest of the bundle free", 300)]
    assert cart(Item("A", 500), Item("B", 300), rules=[BundleFree(3)]).discounts() == []


def test_rule_is_abstract_and_extendable():
    with pytest.raises(TypeError):
        Rule()

    class Tenner(Rule):
        label = "Rs 10 off"
        def discount(self, items, subtotal):
            return 10

    assert cart(Item("A", 100), rules=[Tenner()]).summary()["net"] == 90
```

Test output (Python 3.14):

```text
T06_pricing/test_t06.py::test_item_total_and_validation PASSED
T06_pricing/test_t06.py::test_adding_same_course_merges_quantity PASSED
T06_pricing/test_t06.py::test_no_rules_only_gst PASSED
T06_pricing/test_t06.py::test_percent_with_minimum PASSED
T06_pricing/test_t06.py::test_rules_stack_and_are_listed PASSED
T06_pricing/test_t06.py::test_discount_never_exceeds_the_subtotal PASSED
T06_pricing/test_t06.py::test_bundle_cheapest_free PASSED
T06_pricing/test_t06.py::test_rule_is_abstract_and_extendable PASSED
============================== 8 passed in 1.35s ===============================
```

</details>


## Task 7 · An async link checker (medium)

*Lukas must check hundreds of links in the lesson notes, without hammering any server.*

**Skills:** asyncio, `gather`, `Semaphore`, `wait_for`, retries. **Taught in:** M12-L04, M12-L05, M12-B06.

**Requirements**

- `check_all(urls, fetch, *, concurrency=5, timeout=1.0, retries=1)` is a coroutine; `fetch(url)` is an *async function you pass in* (so tests need no network) that returns a status code or raises `OSError`.
- At most `concurrency` fetches run at the same time.
- Results are `Result(url, ok, status, attempts, error)` objects, in the same order as the input.
- Status below 400 is ok; 4xx is a final answer (no retry); 5xx, timeouts and connection errors are retried up to `retries` extra times.
- A fetch that takes longer than `timeout` seconds counts as `"timeout"`.
- `concurrency < 1` raises `ValueError`.

<details>
<summary><b>Hints for task 7</b></summary>

- `asyncio.gather(*coroutines)` keeps the order of its arguments.
- `async with semaphore:` around one fetch, not around the whole retry loop.
- `asyncio.wait_for(fetch(url), timeout)` raises `asyncio.TimeoutError`.
- Tests: `asyncio.run(check_all(...))` and a shared counter to find the peak concurrency.

</details>

<details>
<summary><b>Reference solution for task 7</b></summary>

The files are in `solutions/T07_async_checker/`. From inside `solutions/`, run `python -m pytest T07_async_checker -v`.

`solutions/T07_async_checker/checker.py`:

```python
"""Task 7 - check many URLs concurrently, politely, with timeouts and retries."""
import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    url: str
    ok: bool
    status: int | None = None
    attempts: int = 0
    error: str | None = None


async def check_one(url, fetch, *, timeout, retries, semaphore) -> Result:
    attempts = 0
    error = None
    for _ in range(retries + 1):
        attempts += 1
        try:
            async with semaphore:                      # at most N requests in flight
                status = await asyncio.wait_for(fetch(url), timeout)
        except asyncio.TimeoutError:
            error = "timeout"
        except OSError as exc:                          # connection problems
            error = type(exc).__name__
        else:
            if status < 500:                            # 4xx is the site's answer: do not retry
                return Result(url, status < 400, status, attempts)
            error = f"server error {status}"
    return Result(url, False, None, attempts, error)


async def check_all(urls, fetch, *, concurrency=5, timeout=1.0, retries=1) -> list[Result]:
    """Results come back in the same order as `urls`."""
    if concurrency < 1:
        raise ValueError("concurrency must be at least 1")
    semaphore = asyncio.Semaphore(concurrency)
    return await asyncio.gather(*(
        check_one(url, fetch, timeout=timeout, retries=retries, semaphore=semaphore)
        for url in urls))
```

`solutions/T07_async_checker/test_t07.py`:

```python
import asyncio

import pytest

from checker import Result, check_all


def run(coro):
    return asyncio.run(coro)


def test_results_keep_the_input_order():
    async def fetch(url):
        await asyncio.sleep({"slow": 0.05, "fast": 0.0}[url])
        return 200

    results = run(check_all(["slow", "fast"], fetch))
    assert [r.url for r in results] == ["slow", "fast"]
    assert all(r.ok for r in results)


def test_status_handling():
    codes = {"ok": 200, "gone": 404}

    async def fetch(url):
        return codes[url]

    results = run(check_all(["ok", "gone"], fetch, retries=3))
    assert results == [Result("ok", True, 200, 1), Result("gone", False, 404, 1)]   # 404: no retries


def test_concurrency_is_limited():
    running = peak = 0

    async def fetch(url):
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await asyncio.sleep(0.01)
        running -= 1
        return 200

    run(check_all([f"u{i}" for i in range(12)], fetch, concurrency=3))
    assert peak == 3


def test_retry_then_success():
    calls = []

    async def fetch(url):
        calls.append(url)
        return 503 if len(calls) < 3 else 200

    (result,) = run(check_all(["u"], fetch, retries=2))
    assert result.ok and result.attempts == 3


def test_gives_up_after_retries():
    async def fetch(url):
        return 500

    (result,) = run(check_all(["u"], fetch, retries=1))
    assert not result.ok and result.attempts == 2 and result.error == "server error 500"


def test_timeout_and_connection_errors():
    async def fetch(url):
        if url == "hang":
            await asyncio.sleep(5)
        raise ConnectionRefusedError

    results = run(check_all(["hang", "down"], fetch, timeout=0.05, retries=0))
    assert [r.error for r in results] == ["timeout", "ConnectionRefusedError"]


def test_concurrency_must_be_positive():
    with pytest.raises(ValueError):
        run(check_all([], None, concurrency=0))
```

Test output (Python 3.14):

```text
T07_async_checker/test_t07.py::test_results_keep_the_input_order PASSED
T07_async_checker/test_t07.py::test_status_handling PASSED
T07_async_checker/test_t07.py::test_concurrency_is_limited PASSED
T07_async_checker/test_t07.py::test_retry_then_success PASSED
T07_async_checker/test_t07.py::test_gives_up_after_retries PASSED
T07_async_checker/test_t07.py::test_timeout_and_connection_errors PASSED
T07_async_checker/test_t07.py::test_concurrency_must_be_positive PASSED
============================== 7 passed in 1.36s ===============================
```

</details>


## Task 8 · A course catalogue API (medium-large)

*Priya needs the catalogue service of allcsvideos: create, read, search, update and delete courses.*

**Skills:** FastAPI, pydantic, status codes, pagination, dependency overrides in tests. **Taught in:** M15-L01 to M15-L06, M15-B08.

**Requirements**

- `POST /courses` (body: `title` 3-80 characters, `price` whole rupees >= 0, `level` one of beginner/intermediate/advanced, default beginner) answers `201` with a `Location` header; a duplicate title (ignoring case) is `409`.
- `GET /courses?q=&limit=&offset=` answers `{items, total, limit, offset}`; `limit` is 1-50 (default 10); bad values are `422`.
- `GET /courses/{id}`, `PATCH /courses/{id}` (only the given fields change; the title still must be unique, but a course may keep its own title) and `DELETE /courses/{id}` (`204`). A missing course is `404`.
- The store is injected with `Depends`, so each test gets a fresh one through `app.dependency_overrides`.

<details>
<summary><b>Hints for task 8</b></summary>

- `body.model_dump(exclude_unset=True)` gives only the fields the client sent.
- `Annotated[int, Query(ge=1, le=50)] = 10` for the limit.
- `course.model_copy(update=changes)` makes the updated record.
- Use a `client` fixture that builds a new `Store` for every test.

</details>

<details>
<summary><b>Reference solution for task 8</b></summary>

The files are in `solutions/T08_catalog_api/`. From inside `solutions/`, run `python -m pytest T08_catalog_api -v`.

`solutions/T08_catalog_api/catalog.py`:

```python
"""Task 8 - a course catalogue API (FastAPI + pydantic, in-memory store)."""
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, Field


class CourseIn(BaseModel):
    title: str = Field(min_length=3, max_length=80)
    price: int = Field(ge=0, description="whole rupees")
    level: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")


class CoursePatch(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=80)
    price: int | None = Field(default=None, ge=0)


class CourseOut(CourseIn):
    id: int


class Page(BaseModel):
    items: list[CourseOut]
    total: int
    limit: int
    offset: int


class Store:
    def __init__(self):
        self.rows: dict[int, CourseOut] = {}
        self.next_id = 1

    def title_taken(self, title: str, except_id: int | None = None) -> bool:
        return any(c.title.lower() == title.lower() and c.id != except_id
                   for c in self.rows.values())


_default_store = Store()


def get_store() -> Store:
    return _default_store


StoreDep = Annotated[Store, Depends(get_store)]
app = FastAPI(title="Catalogue")


@app.post("/courses", status_code=201, response_model=CourseOut)
def create(body: CourseIn, store: StoreDep, response: Response):
    if store.title_taken(body.title):
        raise HTTPException(409, "a course with this title already exists")
    course = CourseOut(id=store.next_id, **body.model_dump())
    store.rows[course.id] = course
    store.next_id += 1
    response.headers["Location"] = f"/courses/{course.id}"
    return course


@app.get("/courses", response_model=Page)
def list_courses(store: StoreDep,
                 q: str | None = None,
                 limit: Annotated[int, Query(ge=1, le=50)] = 10,
                 offset: Annotated[int, Query(ge=0)] = 0):
    rows = sorted(store.rows.values(), key=lambda c: c.id)
    if q:
        rows = [c for c in rows if q.lower() in c.title.lower()]
    return Page(items=rows[offset:offset + limit], total=len(rows), limit=limit, offset=offset)


def _get_or_404(store: Store, course_id: int) -> CourseOut:
    if course_id not in store.rows:
        raise HTTPException(404, "course not found")
    return store.rows[course_id]


@app.get("/courses/{course_id}", response_model=CourseOut)
def read(course_id: int, store: StoreDep):
    return _get_or_404(store, course_id)


@app.patch("/courses/{course_id}", response_model=CourseOut)
def patch(course_id: int, body: CoursePatch, store: StoreDep):
    course = _get_or_404(store, course_id)
    changes = body.model_dump(exclude_unset=True)
    if "title" in changes and store.title_taken(changes["title"], except_id=course_id):
        raise HTTPException(409, "a course with this title already exists")
    updated = course.model_copy(update=changes)
    store.rows[course_id] = updated
    return updated


@app.delete("/courses/{course_id}", status_code=204)
def delete(course_id: int, store: StoreDep):
    _get_or_404(store, course_id)
    del store.rows[course_id]
```

`solutions/T08_catalog_api/test_t08.py`:

```python
import pytest
from fastapi.testclient import TestClient

from catalog import Store, app, get_store


@pytest.fixture
def client():
    store = Store()                                     # a fresh store for every test
    app.dependency_overrides[get_store] = lambda: store
    yield TestClient(app)
    app.dependency_overrides.clear()


def make(client, title="Python", price=499, **extra):
    return client.post("/courses", json={"title": title, "price": price, **extra})


def test_create_and_read(client):
    created = make(client)
    assert created.status_code == 201
    assert created.headers["location"] == "/courses/1"
    assert created.json() == {"id": 1, "title": "Python", "price": 499, "level": "beginner"}
    assert client.get("/courses/1").json()["title"] == "Python"


@pytest.mark.parametrize("body", [
    {"title": "Py", "price": 1},
    {"title": "Python", "price": -5},
    {"title": "Python", "price": "free"},
    {"title": "Python", "price": 5, "level": "expert"},
    {"price": 5},
])
def test_validation_gives_422(client, body):
    assert client.post("/courses", json=body).status_code == 422


def test_duplicate_title_is_409_case_insensitive(client):
    make(client, "Python")
    assert make(client, "PYTHON").status_code == 409


def test_missing_course_is_404(client):
    assert client.get("/courses/99").status_code == 404
    assert client.delete("/courses/99").status_code == 404
    assert client.patch("/courses/99", json={"price": 1}).status_code == 404


def test_pagination_and_search(client):
    for n in range(25):
        make(client, f"Course {n:02d}")
    page = client.get("/courses", params={"limit": 10, "offset": 20}).json()
    assert page["total"] == 25 and len(page["items"]) == 5 and page["items"][0]["id"] == 21
    assert client.get("/courses", params={"q": "course 07"}).json()["total"] == 1
    assert client.get("/courses", params={"limit": 0}).status_code == 422
    assert client.get("/courses", params={"limit": 51}).status_code == 422


def test_patch_changes_only_given_fields(client):
    make(client, "Python", 499)
    changed = client.patch("/courses/1", json={"price": 399}).json()
    assert changed == {"id": 1, "title": "Python", "price": 399, "level": "beginner"}


def test_patch_title_clash_and_own_title(client):
    make(client, "Python")
    make(client, "SQL")
    assert client.patch("/courses/2", json={"title": "python"}).status_code == 409
    assert client.patch("/courses/2", json={"title": "SQL"}).status_code == 200   # own title is fine


def test_delete(client):
    make(client)
    assert client.delete("/courses/1").status_code == 204
    assert client.get("/courses/1").status_code == 404
```

Test output (Python 3.14):

```text
T08_catalog_api/test_t08.py::test_create_and_read PASSED
T08_catalog_api/test_t08.py::test_validation_gives_422[body0] PASSED
T08_catalog_api/test_t08.py::test_validation_gives_422[body1] PASSED
T08_catalog_api/test_t08.py::test_validation_gives_422[body2] PASSED
T08_catalog_api/test_t08.py::test_validation_gives_422[body3] PASSED
T08_catalog_api/test_t08.py::test_validation_gives_422[body4] PASSED
T08_catalog_api/test_t08.py::test_duplicate_title_is_409_case_insensitive PASSED
T08_catalog_api/test_t08.py::test_missing_course_is_404 PASSED
T08_catalog_api/test_t08.py::test_pagination_and_search PASSED
T08_catalog_api/test_t08.py::test_patch_changes_only_given_fields PASSED
T08_catalog_api/test_t08.py::test_patch_title_clash_and_own_title PASSED
T08_catalog_api/test_t08.py::test_delete PASSED
============================== 12 passed in 3.51s ==============================
```

</details>


## Task 9 · Enrollments in Postgres (large)

*A live class has only 3 seats, and ten students click "enroll" at the same moment. Exactly three must win.*

**Skills:** SQLAlchemy 2, constraints, transactions, `SELECT ... FOR UPDATE`, avoiding N+1. **Taught in:** M16-L01 to M16-L05, M20-L04. **Needs:** Postgres in Docker.

**Requirements**

- Tables `student`, `course` (with `seats`) and `enrollment`, with a unique constraint on `(student_id, course_id)` and foreign keys.
- `enroll(engine, student_id, course_id)` runs in one transaction: lock the course row, count the enrollments, raise `CourseFull` when there is no seat, and raise `AlreadyEnrolled` for a duplicate (catch the database's `IntegrityError`).
- An unknown course raises `NoResultFound`.
- `titles_for(engine, student_id)` returns the sorted course titles using a *constant* number of queries (no N+1).
- Tests run against a real Postgres, including a test where 10 threads race for 3 seats and exactly 3 succeed.

<details>
<summary><b>Hints for task 9</b></summary>

- `select(Course).where(...).with_for_update()` locks the row until the transaction ends.
- `with Session(engine) as session, session.begin():` commits or rolls back for you.
- `threading.Barrier(10)` makes all threads start together.
- Remove the lock and watch the race test fail, to see why it matters.

</details>

<details>
<summary><b>Reference solution for task 9</b></summary>

The files are in `solutions/T09_enrollment_db/`. From inside `solutions/`, run `python -m pytest T09_enrollment_db -v`.

`solutions/T09_enrollment_db/enrollments.py`:

```python
"""Task 9 - enrollments in Postgres: constraints, transactions and seat limits."""
from sqlalchemy import ForeignKey, UniqueConstraint, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, selectinload


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "t09_student"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="student")


class Course(Base):
    __tablename__ = "t09_course"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    seats: Mapped[int]


class Enrollment(Base):
    __tablename__ = "t09_enrollment"
    __table_args__ = (UniqueConstraint("student_id", "course_id"),)   # the database enforces it
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("t09_student.id"), index=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("t09_course.id"), index=True)
    student: Mapped[Student] = relationship(back_populates="enrollments")
    course: Mapped[Course] = relationship()


class CourseFull(Exception):
    pass


class AlreadyEnrolled(Exception):
    pass


def enroll(engine, student_id: int, course_id: int) -> int:
    """One transaction. The course row is locked, so two people cannot take the last seat."""
    with Session(engine) as session, session.begin():
        course = session.execute(
            select(Course).where(Course.id == course_id).with_for_update()
        ).scalar_one()                                     # NoResultFound if it does not exist
        taken = session.scalar(
            select(func.count()).select_from(Enrollment).where(Enrollment.course_id == course_id))
        if taken >= course.seats:
            raise CourseFull(course.title)
        row = Enrollment(student_id=student_id, course_id=course_id)
        session.add(row)
        try:
            session.flush()
        except IntegrityError as error:
            raise AlreadyEnrolled(f"{student_id} in {course_id}") from error
        return row.id


def titles_for(engine, student_id: int) -> list[str]:
    """All titles with three queries in total, however many enrollments (no N+1)."""
    with Session(engine) as session:
        student = session.scalars(
            select(Student).where(Student.id == student_id)
            .options(selectinload(Student.enrollments).selectinload(Enrollment.course))
        ).one()
        return sorted(e.course.title for e in student.enrollments)
```

`solutions/T09_enrollment_db/test_t09.py`:

```python
"""Needs Postgres:  docker run -d --name m23p04-pg -e POSTGRES_USER=practice \
-e POSTGRES_PASSWORD=practice -e POSTGRES_DB=practice -p 23604:5432 postgres:17"""
import threading

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from enrollments import (AlreadyEnrolled, Base, Course, CourseFull, Enrollment, Student,
                        enroll, titles_for)

URL = "postgresql+psycopg://practice:practice@localhost:23604/practice"


@pytest.fixture
def engine():
    engine = create_engine(URL, pool_size=15)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session, session.begin():
        session.add_all([Student(id=i, name=f"S{i}") for i in range(1, 21)])
        session.add_all([Course(id=1, title="Python", seats=3),
                         Course(id=2, title="SQL", seats=10),
                         Course(id=3, title="Rust", seats=10)])
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


def test_enroll_and_duplicate(engine):
    assert enroll(engine, 1, 2) > 0
    with pytest.raises(AlreadyEnrolled):
        enroll(engine, 1, 2)
    assert enroll(engine, 2, 2) > 0                     # the failed attempt left no mess behind


def test_unknown_course(engine):
    with pytest.raises(NoResultFound):
        enroll(engine, 1, 99)


def test_course_full(engine):
    for student in (1, 2, 3):
        enroll(engine, student, 1)
    with pytest.raises(CourseFull):
        enroll(engine, 4, 1)


def test_ten_people_race_for_three_seats(engine):
    outcomes = []
    gate = threading.Barrier(10)

    def attempt(student_id):
        gate.wait()                                    # everybody starts together
        try:
            enroll(engine, student_id, 1)
            outcomes.append("ok")
        except CourseFull:
            outcomes.append("full")

    threads = [threading.Thread(target=attempt, args=(i,)) for i in range(1, 11)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(outcomes) == ["full"] * 7 + ["ok"] * 3
    with Session(engine) as session:
        assert session.query(Enrollment).filter_by(course_id=1).count() == 3


def test_titles_use_two_queries(engine):
    for course in (1, 2, 3):
        enroll(engine, 1, course)
    statements = []
    event.listen(engine, "before_cursor_execute", lambda c, cur, stmt, *a: statements.append(stmt))
    assert titles_for(engine, 1) == ["Python", "Rust", "SQL"]
    assert len(statements) == 3          # student, enrollments, courses: constant, not 1 + N
```

Test output (Python 3.14):

```text
T09_enrollment_db/test_t09.py::test_enroll_and_duplicate PASSED
T09_enrollment_db/test_t09.py::test_unknown_course PASSED
T09_enrollment_db/test_t09.py::test_course_full PASSED
T09_enrollment_db/test_t09.py::test_ten_people_race_for_three_seats PASSED
T09_enrollment_db/test_t09.py::test_titles_use_two_queries PASSED
============================== 5 passed in 4.41s ===============================
```

</details>


## Task 10 · A short-link service with a cache (largest)

*Rahul's last task: build a URL shortener for allcsvideos that is fast under load and safe to retry.*

**Skills:** FastAPI + Postgres + Redis: cache-aside, invalidation, idempotency, rate limit, counters. **Taught in:** M15, M16, M18-L01, M18-L04, M19-L02. **Needs:** Postgres and Redis in Docker.

**Requirements**

- `POST /links` with `{url, code?}` creates a short link and answers `201 {code, url}`. Only `http` and `https` URLs are valid (`422` otherwise). Without `code`, make a random 7-character code; a custom code must be 3-32 letters, digits, `_` or `-`, and a taken one is `409`.
- An `Idempotency-Key` header makes a retry return the same link with `200` instead of creating a second one.
- `GET /{code}` answers `307` with a `Location` header. It uses **cache-aside**: look in Redis first, on a miss read Postgres and store the URL in Redis for 60 seconds. An unknown code is `404`.
- Every redirect increments a click counter in Redis; `GET /links/{code}/stats` shows it.
- `DELETE /links/{code}` answers `204` and **invalidates** the cached URL, so a deleted link never redirects again.
- Creating links is rate limited per caller (the `X-Api-Key` header or the client address): 5 per minute, then `429` with a `Retry-After` header.
- Tests run against real Postgres and Redis, and prove that the second visit does not touch Postgres.

<details>
<summary><b>Hints for task 10</b></summary>

- Keep the Redis keys under one prefix so tests can clean up with `scan_iter(prefix + "*")`.
- Rate limit with `INCR key`; when the count is 1, `EXPIRE key window`.
- Count Postgres statements with SQLAlchemy's `before_cursor_execute` event.
- Make the code unique with a primary key and retry on `IntegrityError`; never check-then-insert.
- `/{code}` matches a single path segment only, so it never clashes with `/links/{code}/stats`.

</details>

<details>
<summary><b>Reference solution for task 10</b></summary>

The files are in `solutions/T10_short_links/`. From inside `solutions/`, run `python -m pytest T10_short_links -v`.

`solutions/T10_short_links/shortener.py`:

```python
"""Task 10 - a URL shortener: FastAPI + Postgres + Redis (cache, counters, rate limit)."""
import os
import secrets
import string
from typing import Annotated

import redis
from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import AnyHttpUrl, BaseModel, Field
from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://practice:practice@localhost:23604/practice")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:23404/5")
PREFIX = "t10:"
CACHE_SECONDS = 60
RATE_LIMIT = 5              # link creations ...
RATE_WINDOW = 60            # ... per minute per caller
ALPHABET = string.ascii_letters + string.digits


class Base(DeclarativeBase):
    pass


class Link(Base):
    __tablename__ = "t10_link"
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    url: Mapped[str]
    idempotency_key: Mapped[str | None] = mapped_column(String(100), unique=True)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)
app = FastAPI(title="Short links")


def get_session():
    with Session(engine) as session:
        yield session


Db = Annotated[Session, Depends(get_session)]


class LinkIn(BaseModel):
    url: AnyHttpUrl
    code: str | None = Field(default=None, pattern=r"^[A-Za-z0-9_-]{3,32}$")


class LinkOut(BaseModel):
    code: str
    url: str


def new_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(7))


def rate_limit(request: Request):
    who = request.headers.get("x-api-key") or (request.client.host if request.client else "?")
    key = f"{PREFIX}rate:{who}"
    count = cache.incr(key)
    if count == 1:
        cache.expire(key, RATE_WINDOW)          # the window starts at the first call
    if count > RATE_LIMIT:
        wait = max(cache.ttl(key), 1)
        raise HTTPException(429, "too many links created", headers={"Retry-After": str(wait)})


@app.post("/links", status_code=201, response_model=LinkOut,
          dependencies=[Depends(rate_limit)])
def create(body: LinkIn, db: Db, response: Response,
           idempotency_key: Annotated[str | None, Header(max_length=100)] = None):
    if idempotency_key:                          # the same request again gives the same answer
        earlier = db.scalar(select(Link).where(Link.idempotency_key == idempotency_key))
        if earlier:
            response.status_code = 200
            return LinkOut(code=earlier.code, url=earlier.url)
    url = str(body.url)
    for _ in range(5):                           # random codes can (rarely) collide
        code = body.code or new_code()
        db.add(Link(code=code, url=url, idempotency_key=idempotency_key))
        try:
            db.commit()
            return LinkOut(code=code, url=url)
        except IntegrityError:
            db.rollback()
            if body.code:
                raise HTTPException(409, "that code is taken")
            if idempotency_key:                  # lost a race with the same key: return the winner
                earlier = db.scalar(select(Link).where(Link.idempotency_key == idempotency_key))
                if earlier:
                    response.status_code = 200
                    return LinkOut(code=earlier.code, url=earlier.url)
    raise HTTPException(503, "could not find a free code")


@app.get("/links/{code}/stats")
def stats(code: str):
    return {"code": code, "clicks": int(cache.get(f"{PREFIX}clicks:{code}") or 0)}


@app.delete("/links/{code}", status_code=204)
def delete(code: str, db: Db):
    link = db.get(Link, code)
    if link is None:
        raise HTTPException(404, "no such link")
    db.delete(link)
    db.commit()
    cache.delete(f"{PREFIX}url:{code}")          # invalidate, or the old URL would live on


@app.get("/{code}")
def follow(code: str, db: Db):
    key = f"{PREFIX}url:{code}"
    url = cache.get(key)                         # 1. look in the cache
    if url is None:
        link = db.get(Link, code)                # 2. miss: ask the database
        if link is None:
            raise HTTPException(404, "no such link")
        url = link.url
        cache.set(key, url, ex=CACHE_SECONDS)    # 3. remember it
    cache.incr(f"{PREFIX}clicks:{code}")
    return RedirectResponse(url, status_code=307)
```

`solutions/T10_short_links/test_t10.py`:

```python
"""Needs Postgres on 23604 and Redis on 23404 (containers m23p04-pg and m23p04-redis)."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event

import shortener
from shortener import Base, PREFIX, app, cache, engine


@pytest.fixture
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    for key in cache.scan_iter(f"{PREFIX}*"):
        cache.delete(key)
    yield TestClient(app, follow_redirects=False)
    Base.metadata.drop_all(engine)
    for key in cache.scan_iter(f"{PREFIX}*"):
        cache.delete(key)


def make(client, url="https://allcsvideos.com/python", **extra):
    return client.post("/links", json={"url": url, **extra})


def test_create_and_redirect(client):
    created = make(client)
    assert created.status_code == 201
    code = created.json()["code"]
    assert len(code) == 7
    hop = client.get(f"/{code}")
    assert hop.status_code == 307 and hop.headers["location"] == "https://allcsvideos.com/python"


def test_unknown_code_and_bad_url(client):
    assert client.get("/nope").status_code == 404
    assert make(client, url="not a url").status_code == 422
    assert make(client, url="ftp://example.com/x").status_code == 422


def test_custom_code_and_conflict(client):
    assert make(client, code="python").json()["code"] == "python"
    assert make(client, url="https://example.com/other", code="python").status_code == 409
    assert make(client, code="a b").status_code == 422


def test_idempotency_key(client):
    headers = {"Idempotency-Key": "k-1"}
    first = client.post("/links", json={"url": "https://example.com/a"}, headers=headers)
    again = client.post("/links", json={"url": "https://example.com/a"}, headers=headers)
    assert (first.status_code, again.status_code) == (201, 200)
    assert first.json() == again.json()


def test_second_visit_comes_from_the_cache(client):
    code = make(client).json()["code"]
    queries = []

    def record(conn, cursor, statement, *rest):
        queries.append(statement)

    event.listen(engine, "before_cursor_execute", record)
    try:
        client.get(f"/{code}")            # miss: asks Postgres
        assert len(queries) == 1
        client.get(f"/{code}")            # hit: no new query
        assert len(queries) == 1
    finally:
        event.remove(engine, "before_cursor_execute", record)
    assert 0 < cache.ttl(f"{PREFIX}url:{code}") <= shortener.CACHE_SECONDS


def test_clicks_are_counted(client):
    code = make(client).json()["code"]
    for _ in range(3):
        client.get(f"/{code}")
    assert client.get(f"/links/{code}/stats").json() == {"code": code, "clicks": 3}


def test_delete_invalidates_the_cache(client):
    code = make(client).json()["code"]
    client.get(f"/{code}")                                  # now cached
    assert cache.exists(f"{PREFIX}url:{code}")
    assert client.delete(f"/links/{code}").status_code == 204
    assert not cache.exists(f"{PREFIX}url:{code}")
    assert client.get(f"/{code}").status_code == 404        # not served from a stale cache
    assert client.delete(f"/links/{code}").status_code == 404


def test_rate_limit(client):
    codes = [make(client, url=f"https://example.com/{i}").status_code for i in range(7)]
    assert codes == [201] * 5 + [429, 429]
    blocked = make(client)
    assert 1 <= int(blocked.headers["retry-after"]) <= 60
    other = client.post("/links", json={"url": "https://example.com/x"}, headers={"X-Api-Key": "lukas"})
    assert other.status_code == 201                          # a different caller has its own budget
```

Test output (Python 3.14):

```text
T10_short_links/test_t10.py::test_create_and_redirect PASSED
T10_short_links/test_t10.py::test_unknown_code_and_bad_url PASSED
T10_short_links/test_t10.py::test_custom_code_and_conflict PASSED
T10_short_links/test_t10.py::test_idempotency_key PASSED
T10_short_links/test_t10.py::test_second_visit_comes_from_the_cache PASSED
T10_short_links/test_t10.py::test_clicks_are_counted PASSED
T10_short_links/test_t10.py::test_delete_invalidates_the_cache PASSED
T10_short_links/test_t10.py::test_rate_limit PASSED
============================== 8 passed in 3.60s ===============================
```

</details>


---

**Score yourself:** tasks 1 to 5 working with passing tests means you can handle most coding rounds. Tasks 6 to 8 add the object-oriented and web parts that backend interviews ask about. Tasks 9 and 10 are the kind of thing you can show in a portfolio, and talk about for twenty minutes.

## The last word

Rahul closes his notebook and smiles. "Asha, you came in knowing how to write five lines of Python. You are leaving knowing how to read code, test it, ship it, watch it, and explain it to someone who is paying you to get it right." Lukas, Priya and Meera clap from the back of the room.

You started with `print("welcome student")`. You finish with services that have tests, databases, caches, queues, containers and pipelines. None of it was magic: every piece was a small idea, run for real, and put together carefully. Keep building small things, keep running them, and keep reading other people's code.

Thank you for learning with us. Goodbye, and good luck with your interviews.
