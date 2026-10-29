# M09-L03 · Closures and Decorators

> Video: Module 9, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- A function is a value: you can give it a second label, hand it over, and return it
- What a closure is: an inner function that carries names from the function around it, like a backpack
- How to write a decorator step by step, and what `@name` above a `def` really means
- Why a wrapper takes `*args` and `**kwargs`, returns the result and wears `@wraps(func)`
- How to give a decorator its own setting (`@repeat(3)`) and how to build a notebook cache
- Three pitfalls: when a decorator runs, a missing `(3)`, and loop variables in closures

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed.
- Module 4 (functions, `nonlocal`, `*args` and `**kwargs`) and module 8 (`@property`, `@dataclass`). No earlier lesson folder is needed.

## Files in this folder

| File | What it is |
|------|------------|
| `counter.py` | `make_counter`: a function that remembers (the hook) |
| `alias.py` | A second label for a function: `shout = greet` |
| `apply_twice.py` | Handing a function to another function |
| `greeters.py` | A function that makes functions: `make_greeter` |
| `peek.py` | Peeking into the backpack with `__closure__` |
| `two_counters.py` | Two independent counters from one recipe |
| `broken_counter.py` | Forgetting `nonlocal` |
| `report.py` | `timer` decorator applied the long way |
| `report_at.py` | The same with `@timer` |
| `bad_add.py` | A wrapper with empty brackets breaks on `add(2, 3)` |
| `timed_add.py` | `timer` with `*args` and `**kwargs` |
| `no_return.py` | A wrapper that forgets to `return` |
| `names.py` | The wrapper replaces the name and the docstring |
| `names_fixed.py` | Fixed with `@wraps(func)` |
| `repeat_demo.py` | A decorator with a setting: `@repeat(3)` |
| `notebook.py` | `remember`: a cache kept in the backpack |
| `announce_demo.py` | Pitfall 1: when does a decorator run? |
| `bad_repeat.py` | Pitfall 2: `@repeat` without brackets |
| `loops.py` | Pitfall 3: three functions made in a loop |
| `loops_fixed.py` | The fix: a default value |
| `tryit.py` | A model answer to the Try it yourself task |

## Follow along

### 1. The hook: a function that remembers

In module 4 you learned that local names are wiped when a function ends. Now look at this code. `make_counter` sets `count` to 0, defines `add_one` inside, and returns `add_one` without round brackets: it hands the inner function out without running it. We call `make_counter()` once, keep the result in `counter`, and call `counter()` three times. Guess the three lines.

```python
def make_counter():
    count = 0

    def add_one():
        nonlocal count
        count += 1
        return count

    return add_one


counter = make_counter()
print(counter())
print(counter())
print(counter())
```

```bash
python counter.py
```

```
1
2
3
```

The count grows, even though `make_counter` finished long ago. So where does `count` live? Inside the inner function. A function that remembers names from the place where it was made is called a **closure**. The second half of the lesson is about decorators: lines that start with `@` and wrap another function.

### 2. A function is a value

A recipe card in a binder can get a second label, be handed to somebody, or be put in a box. A function in Python is a value too. First use: a second label. `shout = greet` has no round brackets, so nothing runs.

```python
def greet(name):
    return f"Hello, {name}!"


shout = greet
print(shout("Lukas"))
print(shout is greet)
```

```bash
python alias.py
```

```
Hello, Lukas!
True
```

Two labels, one function, like two labels on one list. Second use: hand a function to another function (you did this with `max(..., key=len)`). Inside `apply_twice`, `func` is just a label for whatever function arrived:

```python
def excite(text):
    return text + "!"


def apply_twice(func, value):
    return func(func(value))


print(apply_twice(excite, "Hi"))
```

```bash
python apply_twice.py
```

```
Hi!!
```

Third use, the new one: a function can make a function and give it back.

```python
def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}!"

    return greet


hello = make_greeter("Hello")
namaste = make_greeter("Namaste")
print(hello("Lukas"))
print(namaste("Priya"))
```

```bash
python greeters.py
```

```
Hello, Lukas!
Namaste, Priya!
```

Each function remembers its own greeting. `greeting` is not a parameter of `greet`, and `greet` does not make it: it reads it from the function around it (the enclosing scope from module 4). And yet `make_greeter` finished long ago. That is the **backpack**.

### 3. Closures: the backpack

When Python creates the inner function, it looks at which outside names that function uses, packs them into a backpack and attaches it to the function. Every call to `make_greeter` creates a new function with its own backpack. You can peek: every function has `__closure__`, a tuple of cells, and `cell_contents` holds the value. You will rarely need it in real code.

```python
def make_greeter(greeting):
    def greet(name):
        return f"{greeting}, {name}!"

    return greet


hello = make_greeter("Hello")
namaste = make_greeter("Namaste")
print(hello.__closure__[0].cell_contents)
print(namaste.__closure__[0].cell_contents)
```

```bash
python peek.py
```

```
Hello
Namaste
```

Back to the hook. `count` lives in the backpack of `add_one`, and the `nonlocal` line lets `add_one` change a name in its backpack instead of making a new local. Every call to `make_counter` makes a new backpack, so one recipe gives two independent counters:

```python
def make_counter():
    count = 0

    def add_one():
        nonlocal count
        count += 1
        return count

    return add_one


views = make_counter()
logins = make_counter()
print(views())
print(views())
print(logins())
print(views())
```

```bash
python two_counters.py
```

```
1
2
1
3
```

What if we forget `nonlocal`? `count += 1` assigns, so Python makes `count` local to `add_one`, and it has no value yet:

```python
def make_counter():
    count = 0

    def add_one():
        count += 1

    return add_one


counter = make_counter()
counter()
```

```bash
python broken_counter.py
```

```
Traceback (most recent call last):
  File "broken_counter.py", line 11, in <module>
    counter()
    ~~~~~~~^^
  File "broken_counter.py", line 5, in add_one
    count += 1
    ^^^^^
UnboundLocalError: cannot access local variable 'count' where it is not associated with a value
```

The fix is the line you know: `nonlocal count`. So a closure is simply an inner function that uses a name from the function around it and carries it along.

### 4. Your first decorator: `timer`

Asha has a slow job on allcsvideos.com, building the weekly report, and wants to time it. Editing twenty functions is a lot of work and every edit can add a bug. Can we add timing from outside? Yes, with a function that takes a function. `timer` receives `func`, defines `wrapper` (which reads the clock, calls `func`, reads the clock again, prints the difference and returns `func`'s answer) and returns `wrapper`. `func` inside `wrapper` comes from the backpack: the wrapper is a closure.

`weekly_report = timer(weekly_report)` puts the wrapper back under the old label. The old function is not lost: the wrapper keeps it in its backpack. Guess the output.

```python
import time


def timer(func):
    def wrapper():
        start = time.perf_counter()
        result = func()
        took = time.perf_counter() - start
        print(f"Took {took:.1f} seconds")
        return result

    return wrapper


def weekly_report():
    time.sleep(0.2)
    print("Report ready")


weekly_report = timer(weekly_report)
weekly_report()
```

```bash
python report.py
```

```
Report ready
Took 0.2 seconds
```

`Report ready` comes first, then the time: the wrapper started the clock, called the real function, then printed the time. We never edited `weekly_report`. Python has a shortcut for that easy-to-forget line: put `@timer` above the `def`.

```python
import time


def timer(func):
    def wrapper():
        start = time.perf_counter()
        result = func()
        took = time.perf_counter() - start
        print(f"Took {took:.1f} seconds")
        return result

    return wrapper


@timer
def weekly_report():
    time.sleep(0.2)
    print("Report ready")


weekly_report()
```

```bash
python report_at.py
```

```
Report ready
Took 0.2 seconds
```

Remember the rule: `@timer` above `def weekly_report` means `weekly_report = timer(weekly_report)`. Nothing more. This is what `@property`, `@classmethod` and `@dataclass` were doing: each one receives what is below it and gives back a replacement.

### 5. Wrappers that accept anything, and return

Our wrapper has empty round brackets. Real functions take values. What happens with `add(2, 3)`?

```python
import time


def timer(func):
    def wrapper():
        start = time.perf_counter()
        result = func()
        took = time.perf_counter() - start
        print(f"Took {took:.1f} seconds")
        return result

    return wrapper


@timer
def add(a, b):
    return a + b


print(add(2, 3))
```

```bash
python bad_add.py
```

```
Traceback (most recent call last):
  File "bad_add.py", line 20, in <module>
    print(add(2, 3))
          ~~~^^^^^^
TypeError: timer.<locals>.wrapper() takes 0 positional arguments but 2 were given
```

`add` is now the wrapper, so the wrapper must accept whatever the function accepts. Use `*args` and `**kwargs` (module 4): in the `def` line they pack, in a call they unpack, so `func` receives exactly what `wrapper` received. Call it by position and by name:

```python
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        took = time.perf_counter() - start
        print(f"Took {took:.1f} seconds")
        return result

    return wrapper


@timer
def add(a, b):
    time.sleep(0.2)
    return a + b


print(add(2, 3))
print(add(a=10, b=5))
```

```bash
python timed_add.py
```

```
Took 0.2 seconds
5
Took 0.2 seconds
15
```

Each call prints `Took 0.2 seconds` first, because the function runs before `print` shows its answer. Positional and named values both pass through untouched. Now a mistake many people make: the wrapper must also give the answer back.

```python
def timer(func):
    def wrapper(*args, **kwargs):
        print("Timing...")
        func(*args, **kwargs)

    return wrapper


@timer
def add(a, b):
    return a + b


print(add(2, 3))
```

```bash
python no_return.py
```

```
Timing...
None
```

`None`. `add` computed 5 but the wrapper threw it away. A good wrapper has three habits: it accepts `*args` and `**kwargs`, calls `func` with them, and returns the result.

### 6. Keep the name: `functools.wraps`

The wrapper replaces the function, including its name and notes. Every function has a name tag `__name__` and its docstring is in `__doc__`. Guess what we get:

```python
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        took = time.perf_counter() - start
        print(f"Took {took:.1f} seconds")
        return result

    return wrapper


@timer
def add(a, b):
    """Add two numbers."""
    return a + b


print(add.__name__)
print(add.__doc__)
```

```bash
python names.py
```

```
wrapper
None
```

`wrapper` and `None`. Error messages, `help` and debugging tools all show the name; twenty decorated functions would all be called `wrapper`. The fix is `from functools import wraps` and `@wraps(func)` above the wrapper. It copies the name and the docstring onto the wrapper:

```python
import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        took = time.perf_counter() - start
        print(f"Took {took:.1f} seconds")
        return result

    return wrapper


@timer
def add(a, b):
    """Add two numbers."""
    return a + b


print(add.__name__)
print(add.__doc__)
```

```bash
python names_fixed.py
```

```
add
Add two numbers.
```

Make it a habit: every wrapper you write gets `@wraps(func)`, no exceptions.

### 7. A decorator with a setting

Sometimes a decorator needs a setting, like `@repeat(3)`. `repeat` is called with a number, but a decorator receives a function. One more layer solves it. `@repeat(3)` works in two steps: Python calls `repeat(3)`, which returns a decorator, then applies that decorator to the function below. Three layers: `repeat` holds the setting, `decorator` holds the function, `wrapper` does the work at call time. The `_` in the `for` line is a loop name we do not need.

```python
from functools import wraps


def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@repeat(3)
def cheer(name):
    print(f"Go, {name}!")


cheer("Priya")
```

```bash
python repeat_demo.py
```

```
Go, Priya!
Go, Priya!
Go, Priya!
```

The setting travelled in the backpack of `wrapper`. Remember the shape: the outer function takes the settings, the middle one takes the function, the inner one takes the call. The build video uses this shape for a retry decorator and a cache that forgets.

### 8. A notebook in the backpack: `remember`

Looking up a course price is slow. If a hundred students ask for the same price, repeating the work is wasteful. The idea: the first time, do the work and write the answer in a notebook; the next time, read it from the notebook. `notebook` is an empty dictionary made once, when the function is decorated, and it lives in the backpack, so every call of `wrapper` sees the same one. A tuple works as a dictionary key. Guess the five lines.

```python
from functools import wraps


def remember(func):
    notebook = {}

    @wraps(func)
    def wrapper(*args):
        if args not in notebook:
            notebook[args] = func(*args)
        return notebook[args]

    return wrapper


@remember
def course_price(course_id):
    print(f"Looking up course {course_id}")
    prices = {7: 1499, 8: 999}
    return prices[course_id]


print(course_price(7))
print(course_price(7))
print(course_price(8))
```

```bash
python notebook.py
```

```
Looking up course 7
1499
1499
Looking up course 8
999
```

The second call for course 7 prints only the price: the answer came from the notebook. Course 8 is new, so it looks up again. Two honest limits: this version understands only positional values, and the notebook never forgets. Python ships a careful version, `functools.cache`, in lesson 5, and the build video writes a cache that forgets after some seconds.

### 9. Pitfalls

**Pitfall 1: when does a decorator run?** `announce` prints in its own body and inside the wrapper. Guess all six lines.

```python
def announce(func):
    print("Decorating now")

    def wrapper():
        print("Calling now")
        func()

    return wrapper


@announce
def hello():
    print("Hello")


print("Defined")
hello()
hello()
```

```bash
python announce_demo.py
```

```
Decorating now
Defined
Calling now
Hello
Calling now
Hello
```

`Decorating now` comes first, even before `Defined`. The decorator runs once, at the moment Python reaches the `def`, not at every call. Work that should happen at every call belongs inside the wrapper.

**Pitfall 2: forgetting the brackets on a decorator with a setting.** Here the line says `@repeat`, with no `(3)`. Will Python complain?

```python
from functools import wraps


def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@repeat
def cheer(name):
    print(f"Go, {name}!")


cheer("Priya")
```

```bash
python bad_repeat.py
```

(no output)

Nothing at all: no error and not a single `Go`. Python ran `cheer = repeat(cheer)`, so `times` became the function and `cheer` now holds the decorator. The fix is `@repeat(3)`. If a decorator has a setting, always call it.

**Pitfall 3: the backpack holds the name, not the value.** Three small functions made in a loop (a `lambda` with nothing before the colon takes no values):

```python
greeters = []
for name in ["Lukas", "Priya", "Meera"]:
    greeters.append(lambda: f"Hello, {name}!")

for greeter in greeters:
    print(greeter())
```

```bash
python loops.py
```

```
Hello, Meera!
Hello, Meera!
Hello, Meera!
```

Meera, three times. When the loop ends, `name` is `Meera` and all three functions read that. The fix is to give each function its own copy with a default value: `lambda name=name:` makes a parameter and fills it with the current value at the moment the function is made.

```python
greeters = []
for name in ["Lukas", "Priya", "Meera"]:
    greeters.append(lambda name=name: f"Hello, {name}!")

for greeter in greeters:
    print(greeter())
```

```bash
python loops_fixed.py
```

```
Hello, Lukas!
Hello, Priya!
Hello, Meera!
```

### 10. Try it yourself: model answer

Write `make_multiplier(n)` that returns a function multiplying by `n`. Then a decorator `log_calls` that prints the function's name and values before each call. Use `wraps`, apply it to `add`, and check that `add`'s name is still `add`. Here is one answer:

```python
from functools import wraps


def make_multiplier(n):
    def multiply(x):
        return x * n

    return multiply


def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with {args}")
        return func(*args, **kwargs)

    return wrapper


@log_calls
def add(a, b):
    return a + b


triple = make_multiplier(3)
print(triple(5))
print(add(2, 3))
print(add.__name__)
```

```bash
python tryit.py
```

```
15
Calling add with (2, 3)
5
add
```

## Common mistakes

1. Forgetting `nonlocal` when a closure changes a name from its backpack (`UnboundLocalError`).

2. A wrapper with empty brackets: it breaks as soon as the function takes values. Use `*args` and `**kwargs`.

3. A wrapper that does not `return` the result: the decorated function now gives back `None`.

4. Forgetting `@wraps(func)`: every decorated function is called `wrapper` and loses its docstring.

5. Writing `@repeat` instead of `@repeat(3)`: no error, but the function silently does nothing.

6. Putting per-call work in the decorator body instead of the wrapper: the body runs once, when the function is defined.

7. Making functions in a loop that use the loop variable: they all see its last value. Use a default value.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next lesson: [M09-L04 · Context Managers](../m09-l04-context-managers/README.md). You will learn what really happens behind the `with` statement, and how to write your own.
