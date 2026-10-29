# M09-L04 · Context Managers

> Video: Module 9, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- Why a stuck maintenance flag happens, and how `try`/`finally` cures it
- What the `with` statement really calls: `__enter__` at the start and `__exit__` at the end
- How to write your own context manager as a class, and the short way with `@contextmanager` and one `yield`
- Why returning `True` from `__exit__` hides errors, and how `contextlib.suppress` ignores one named error safely
- How to put several managers in one `with` line, and in which order they close

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed.
- The exceptions lesson (module 6, `try`, `except`, `finally`) and [M09-L03 · Closures and Decorators](../m09-l03-closures-and-decorators/README.md) for the `@` decorator shortcut. The generators lesson ([M09-L02](../m09-l02-generators/README.md)) explains `yield`.

## Files in this folder

| File | What it is |
|------|------------|
| `hook.py` | Asha's price update: the maintenance flag stays on after an error (the hook) |
| `hook_fin.py` | The cure with `try` and `finally` |
| `door1.py` | The smallest context manager: `Door` with `__enter__` and `__exit__` |
| `door2.py` | An error inside the block: `__exit__` still runs |
| `door3.py` | What `__exit__` receives: the error type and value |
| `quiet.py` | `__exit__` returns `True` and swallows the error |
| `maint1.py` | `Maintenance` as a class: the flag always goes off |
| `timer1.py` | A `Timer` stopwatch class |
| `flow.py` | A manager with `@contextmanager` and one `yield` |
| `cm1.py` | `@contextmanager` without `try`/`finally`: the flag sticks again |
| `cm2.py` | The fix: put the `yield` inside `try` and `finally` |
| `prices.txt` | Three prices, one per line |
| `opened.py` | A tiny `open()` copy that yields the file |
| `best0.py` | The best score the long way: `try`, `except FileNotFoundError`, `pass` |
| `best.py` | The same with `contextlib.suppress` |
| `in.txt` | Two names for the copy example |
| `two.py` | Two managers in one `with` line |
| `order.py` | Managers close in reverse order |
| `p1.py` | Mistake 1: `__enter__` but no `__exit__` |
| `p1b.py` | Mistake 2: `with Door:` without brackets |
| `p2.py` | Mistake 3: `as` gives `None` |

## Follow along

### 1. The hook: a stuck flag

Asha is updating prices on allcsvideos.com. While she works, the site must show a maintenance page. Her function switches the maintenance flag on, fixes each price, and switches the flag off. Three prices arrive as text: `499`, `abc`, `999`. The middle one is bad. Guess the output, and whether the flag is on or off at the end.

```python
site = {"maintenance": False}


def update_prices(prices):
    site["maintenance"] = True
    for price in prices:
        print("fixing", int(price))
    site["maintenance"] = False


try:
    update_prices(["499", "abc", "999"])
except ValueError:
    print("update failed")
print("maintenance:", site["maintenance"])
```

```bash
python hook.py
```

```
fixing 499
update failed
maintenance: True
```

`update failed` is expected, but `maintenance: True` is the bug: the error jumped out of the function before the line that switches the flag off, and every visitor would see the maintenance page. You know the cure from the exceptions lesson, `finally`:

```python
site = {"maintenance": False}


def update_prices(prices):
    site["maintenance"] = True
    try:
        for price in prices:
            print("fixing", int(price))
    finally:
        site["maintenance"] = False


try:
    update_prices(["499", "abc", "999"])
except ValueError:
    print("update failed")
print("maintenance:", site["maintenance"])
```

```bash
python hook_fin.py
```

```
fixing 499
update failed
maintenance: False
```

Now `maintenance: False`. But every function that switches something on must remember the same `try`/`finally`. Forget it once and the bug is back. There is something better, and you use it every day: the `with` statement. `with open(...)` sets a file up and cleans it up, and you cannot forget.

### 2. How `with` works: `__enter__` and `__exit__`

Picture a hotel room: you put the key card in the slot and the lights come on; you take it out and the lights go off, however you left, calmly or in a hurry. Three things happen: something at the start, whatever you do in the room, and something at the end that always happens. That is a **context manager**. `with` does not know what a file is. It simply asks the object for two methods: `__enter__` at the start and `__exit__` at the end (dunder methods from module 8).

The smallest one, a class `Door`. Guess the four lines and their order:

```python
class Door:
    def __enter__(self):
        print("enter: open the door")
        return "the key"

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit: close the door")


with Door() as key:
    print("inside, holding", key)
print("after the block")
```

```bash
python door1.py
```

```
enter: open the door
inside, holding the key
exit: close the door
after the block
```

`enter` first, then the block, then `exit`, then the line after the block. The name `key` received whatever `__enter__` returned. Now what if an error happens inside the block? Does `exit` still run?

```python
class Door:
    def __enter__(self):
        print("enter: open the door")
        return "the key"

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit: close the door")


with Door() as key:
    print("inside, holding", key)
    int("abc")
    print("never printed")
print("after the block")
```

```bash
python door2.py
```

```
enter: open the door
inside, holding the key
exit: close the door
Traceback (most recent call last):
  File "door2.py", line 12, in <module>
    int("abc")
    ~~~^^^^^^^
ValueError: invalid literal for int() with base 10: 'abc'
```

Yes: `exit` runs even though the program is crashing, and only then does the traceback appear. `__exit__` always runs, just like `finally`.

The three names in the brackets of `__exit__` describe the error: its type, its value and its traceback. When there is no error all three are `None`. Here the first block has no error and the second raises a `ValueError` inside a `try`:

```python
class Door:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit got:", exc_type, exc_value)


with Door():
    print("fine")

try:
    with Door():
        raise ValueError("bad price")
except ValueError:
    print("caught outside")
```

```bash
python door3.py
```

```
fine
exit got: None None
exit got: <class 'ValueError'> bad price
caught outside
```

With no error: `None None`. With an error: the type and the message. After `exit` finished the error carried on and the `try` caught it.

### 3. The danger: returning `True` from `__exit__`

If `__exit__` returns `True`, Python decides the error was handled and it disappears. Here is a class that returns `True` every time, and a typo `totl` inside the block:

```python
class Quiet:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return True


with Quiet():
    print("start")
    print(totl)
    print("end")
print("done")
```

```bash
python quiet.py
```

```
start
done
```

`start`, `done`, and no traceback at all. The typo raised a `NameError`, `exit` swallowed it, `print("end")` never ran, and nobody was told. It is the quiet bug from the exceptions lesson hiding inside a `with`. So the rule: normally return nothing from `__exit__`, and errors travel on. Return `True` only if you chose, on purpose, one small kind of error to ignore (you will see a safe way in step 6).

### 4. Cure the stuck flag with a class

A class `Maintenance`: `__init__` keeps the site, `__enter__` switches the flag on, `__exit__` switches it off and returns nothing, so errors are not hidden. `update_prices` now only fixes prices and knows nothing about the flag.

```python
class Maintenance:
    def __init__(self, site):
        self.site = site

    def __enter__(self):
        self.site["maintenance"] = True

    def __exit__(self, exc_type, exc_value, traceback):
        self.site["maintenance"] = False


site = {"maintenance": False}


def update_prices(prices):
    for price in prices:
        print("fixing", int(price))


try:
    with Maintenance(site):
        update_prices(["499", "abc", "999"])
except ValueError:
    print("update failed")
print("maintenance:", site["maintenance"])
```

```bash
python maint1.py
```

```
fixing 499
update failed
maintenance: False
```

`maintenance: False`. The error still travelled up to the `try`, and the flag still went off. Setup and cleanup now live in one place, and every use is one line.

A second example, a stopwatch. `__enter__` notes the clock and returns `self`; `__exit__` works out the seconds and keeps the number:

```python
import time


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.seconds = time.perf_counter() - self.start


with Timer() as timer:
    time.sleep(0.2)
print("took", round(timer.seconds, 1), "seconds")
```

```bash
python timer1.py
```

```
took 0.2 seconds
```

Note that `timer` still works after the block: `as` gave us the `Timer` object itself, because `__enter__` returned `self`. The recipe for a class: `__init__` stores what you need, `__enter__` does the setup and returns the value for the `as` name, `__exit__` does the cleanup.

### 5. The short way: `@contextmanager`

A whole class for a before and an after is a lot of typing. Remember generators: `yield` pauses a function in the middle and it can continue later. That is the shape we need: setup, pause while the block runs, cleanup. `contextlib` has a decorator for it. No class:

```python
from contextlib import contextmanager


@contextmanager
def door():
    print("enter: open the door")
    yield
    print("exit: close the door")


with door():
    print("inside")
print("after the block")
```

```bash
python flow.py
```

```
enter: open the door
inside
exit: close the door
after the block
```

The same order as the class. The `@` above a function means `door = contextmanager(door)` (lesson 3). Calling `door()` builds a generator paused before its first line and wraps it in a context manager. When `with` starts, Python runs it up to the `yield` (the enter part), then your block runs, then Python resumes it after the `yield` (the exit part).

Now Asha's maintenance, the short way. Guess the last line:

```python
from contextlib import contextmanager

site = {"maintenance": False}


@contextmanager
def maintenance(site):
    site["maintenance"] = True
    yield
    site["maintenance"] = False


def update_prices(prices):
    for price in prices:
        print("fixing", int(price))


try:
    with maintenance(site):
        update_prices(["499", "abc", "999"])
except ValueError:
    print("update failed")
print("maintenance:", site["maintenance"])
```

```bash
python cm1.py
```

```
fixing 499
update failed
maintenance: True
```

`maintenance: True`: the stuck flag is back. When the block fails, Python raises the error inside the generator, exactly at the `yield` line, so the line after the `yield` never runs. It is the same trap as the very first function, and so is the cure: put the `yield` inside `try` and the cleanup in `finally`.

```python
from contextlib import contextmanager

site = {"maintenance": False}


@contextmanager
def maintenance(site):
    site["maintenance"] = True
    try:
        yield
    finally:
        site["maintenance"] = False


def update_prices(prices):
    for price in prices:
        print("fixing", int(price))


try:
    with maintenance(site):
        update_prices(["499", "abc", "999"])
except ValueError:
    print("update failed")
print("maintenance:", site["maintenance"])
```

```bash
python cm2.py
```

```
fixing 499
update failed
maintenance: False
```

The rule for this style: always put the `yield` inside `try` and `finally`.

A manager can also hand a value to the name after `as`: whatever you `yield`. A tiny copy of `open` (the file `prices.txt` has three prices):

```python
from contextlib import contextmanager


@contextmanager
def opened(path):
    file = open(path)
    try:
        yield file
    finally:
        file.close()
        print("closed")


with opened("prices.txt") as f:
    print(f.readline().strip())
print(f.closed)
```

```bash
python opened.py
```

```
1499
closed
True
```

The file is shut after the block, even though we never wrote `close()` in the main part. So there are two ways to make a context manager: a class with `__enter__` and `__exit__`, or a generator with one `yield` inside `try`/`finally` and the decorator. The short way is what most people write.

### 6. Ignore one error on purpose: `suppress`

Sometimes a problem is normal and you want to ignore it. If the best-score file does not exist yet, the best score is 0. The long way:

```python
from pathlib import Path

best = 0
try:
    best = int(Path("best.txt").read_text())
except FileNotFoundError:
    pass
print("best so far:", best)
```

```bash
python best0.py
```

```
best so far: 0
```

`contextlib` has a ready-made manager for this: `suppress`. The same job in two lines:

```python
from contextlib import suppress
from pathlib import Path

best = 0
with suppress(FileNotFoundError):
    best = int(Path("best.txt").read_text())
print("best so far:", best)
```

```bash
python best.py
```

```
best so far: 0
```

There is no `best.txt` yet, so the `FileNotFoundError` was swallowed and the best score stays 0. Now make a `best.txt` holding a 5 and run it again:

```bash
echo 5 > best.txt
```


```bash
python best.py
```

```
best so far: 5
```

```bash
rm best.txt
```


The block ran and nothing was suppressed. Why is this safe when returning `True` from `__exit__` was dangerous? Because `suppress` names the error: only a `FileNotFoundError` disappears. A `ValueError`, a typo, anything else still stops the program. Name the narrowest error you expect, as you do with `try` blocks.

### 7. Several managers in one `with`

Put a comma between them. Here we copy `in.txt` in capital letters (the file has `lukas` and `priya` on two lines):

```python
from pathlib import Path

with open("in.txt") as src, open("out.txt", "w") as dst:
    for line in src:
        dst.write(line.upper())
print(Path("out.txt").read_text().split())
```

```bash
python two.py
```

```
['LUKAS', 'PRIYA']
```

Both files were closed at the end by one `with` statement. In which order do they close? A small manager `step` prints `start` and `end`, with the `yield` in `try`/`finally`:

```python
from contextlib import contextmanager


@contextmanager
def step(name):
    print("start", name)
    try:
        yield
    finally:
        print("end", name)


with step("A"), step("B"):
    print("inside")
```

```bash
python order.py
```

```
start A
start B
inside
end B
end A
```

`start A`, `start B`, `inside`, then `end B`, `end A`. The one opened last is closed first, like plates in a stack, because B may depend on A.

### 8. Three mistakes

**Mistake 1: `__enter__` but no `__exit__`.** A protocol is an agreed set of methods, and a context manager needs both.

```python
class Door:
    def __enter__(self):
        return self


with Door():
    print("inside")
```

```bash
python p1.py
```

```
Traceback (most recent call last):
  File "p1.py", line 6, in <module>
    with Door():
         ~~~~^^
TypeError: 'Door' object does not support the context manager protocol (missed __exit__ method)
```

**Mistake 2: forgetting the round brackets.** This class has both methods, but `with Door:` uses the class itself, not an object made from it. The error even says `__exit__`, which is misleading: the real problem is that `Door` needs brackets to make an object.

```python
class Door:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


with Door:
    print("inside")
```

```bash
python p1b.py
```

```
Traceback (most recent call last):
  File "p1b.py", line 9, in <module>
    with Door:
         ^^^^
TypeError: 'type' object does not support the context manager protocol (missed __exit__ method)
```

**Mistake 3: `as` gives `None`.** Our maintenance manager yields nothing, so a bare `yield` hands out `None`. Use `as` only when your manager yields something.

```python
from contextlib import contextmanager

site = {"maintenance": False}


@contextmanager
def maintenance(site):
    site["maintenance"] = True
    try:
        yield
    finally:
        site["maintenance"] = False


with maintenance(site) as m:
    print(m)
```

```bash
python p2.py
```

```
None
```

## Common mistakes

1. Switching something on and forgetting to switch it off when an error happens. Use a context manager, not a bare function.

2. Returning `True` from `__exit__` by accident: it swallows every error, even typos.

3. Writing `@contextmanager` and putting the cleanup after the `yield` without `try`/`finally`: an error skips the cleanup.

4. Writing `with Door:` instead of `with Door():`.

5. Using `as m` when the manager yields nothing: `m` is `None`.

6. Using a very broad `suppress(Exception)`. Name the narrowest error you expect.

## Clean up

Nothing to clean up: `out.txt` is created next to the files when you run `two.py`. Delete it if you want.

## Next

Next lesson: [M09-L05 · Standard Library Power Tools](../m09-l05-standard-library-power-tools/README.md). You will meet `deque`, `groupby`, `partial` and `cache`: ready-made tools for jobs you would otherwise write by hand.

Your turn first: write a context manager that prints "entering" and "leaving" and use it around a line that raises an error; write it again with `@contextmanager`; then use `suppress` to ignore a missing file.
