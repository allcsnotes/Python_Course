# M09-B05 · Build a Decorator Toolkit

> Video: Module 9, Build 5. Watch it first, then follow along here.

## What you'll learn

- How to turn copy-pasted timing lines into one reusable label (a decorator)
- The four rules every wrapper follows: `*args`/`**kwargs`, call and return, `@wraps`, do the extra job
- Four decorators in one module: `timed`, `retry(times, delay)`, `cache_for(seconds)` and `require_login`
- Why the order of stacked decorators changes behaviour, and the rule "cheap checks on the outside"
- Where the toolkit breaks: mutable cache values, unhashable keys, retrying payments, a wrong first argument

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker needed, and nothing to install: only the standard library is used.
- Finish [M09-L03 · Closures and Decorators](../m09-l03-closures-and-decorators/README.md) and [M09-L05](../m09-l05-standard-library-power-tools/README.md) first. The build also uses errors from module 6, modules from module 7 and dataclasses from module 8.
- Every step has a snapshot folder (`step1/` ... `step5/`) with `toolkit.py` as it looks at the end of that step and the small `tryN.py` test files. Timings (the milliseconds) will differ a little on your computer.

## Files in this folder

| File | What it is |
|------|------------|
| `toolkit.py` | The finished toolkit module: 2 errors and 4 decorators, 67 lines |
| `demo.py` | The demo program that imports the toolkit and runs everything |
| `extra/before.py` | The problem: timing lines copied into every function |
| `extra/skeleton.py` | The four wrapper rules as a tiny file |
| `step1/toolkit.py` | Step 1: `timed` |
| `step1/try1.py` | Test: name and docstring survive |
| `step1/try1b.py` | Test: a crash is still timed |
| `step2/toolkit.py` | Step 2: adds `RetryableError` and `retry` |
| `step2/try2.py` | Test: a flaky function that works on the third call |
| `step2/try2b.py` | Test: always down, and a bug that is not retried |
| `step3/toolkit.py` | Step 3: adds `cache_for` |
| `step3/try3.py` | Test: a cached price that expires |
| `step4/toolkit.py` | Step 4: adds `LoginRequiredError` and `require_login` |
| `step4/try4.py` | Test: Priya is in, Lukas is refused |
| `step5/toolkit.py` | Step 5: same toolkit (stacking needs no new code) |
| `step5/try5.py` | Test: does the order of `@timed` and `@retry` matter? |
| `extra/mutable.py` | Breaks 1: the cache hands out the same list |
| `extra/unhashable.py` | Breaks 2: an unhashable user as a cache key |
| `extra/twice.py` | Breaks 3: retry charges a payment twice |
| `extra/wrongarg.py` | Breaks 4: the wrong first argument for `require_login` |

## Run it

From this folder (the one with `toolkit.py` and `demo.py`):

```bash
python demo.py
```

A catalog fails twice and works on the third try (and its time is measured), a price is looked up once and the second time it comes from a notebook, Priya buys a course, and Lukas, who has not logged in, is refused. The full expected output is in the section "Put it together" below.

## Build it step by step

### The problem: the same timing lines everywhere

Asha's allcsvideos.com server has dozens of functions and for many of them she wants to know how long they take. Here are two. Each carries the same three timing lines: take the clock at the start, take it again at the end, print the difference. (`time.sleep` just pauses the program to pretend to work.) Guess the output.

```bash
python before.py
```

```
load_report took 205 ms
daily report
load_students took 105 ms
['Priya', 'Lukas']
```

It works, but in each function three lines are about timing and the real work is two lines. With thirty functions, and then Meera asking for seconds instead of milliseconds, you would edit thirty places. For code that wraps around other code you learned the way out in this module: a decorator. Write the timing once and put one label above any function.

Today we build four such labels: `timed`, `retry`, `cache_for` and `require_login`, build each one from scratch, run it, and then stack them. Nothing here is new: it uses closures and decorators from lesson 3, errors from module 6 and modules from module 7.

### Plan on paper, and the four wrapper rules

Four tools, one label per job. `timed` measures how long a function takes. `retry` tries again when a function fails for a reason that may pass. `cache_for` remembers an answer for a number of seconds. `require_login` refuses anyone who has not logged in. Two are plain decorators (`@timed`), two need a setting and are written with brackets (`@retry(times=3)`, `@cache_for(seconds=1)`), which means one extra layer (lesson 3).

All four wrappers follow the same four rules: 1. take `*args` and `**kwargs` so the wrapper fits any function. 2. Call the real function and return what it returns. 3. Use `@wraps` so the name and docstring survive. 4. Do the extra job: before the call, after it, or around it. Here are the rules as a tiny file. Guess the output:

```python
from functools import wraps


def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper


@decorator
def greet(name):
    return f"Hello, {name}"


print(greet("Priya"))
```

```bash
python extra/skeleton.py
```

```
before
after
Hello, Priya
```

`before`, `after`, then `Hello Priya`: the two prints inside the wrapper come first because the wrapper runs before `print` gets the result. This skeleton is the heart of every decorator in the toolkit; we only change what happens at the dots.

The toolkit lives in one file, `toolkit.py`, a module like the drawers in module 7. A second file, `demo.py`, borrows it with `import`. Create an empty folder, put `toolkit.py` in it, and build it in five steps.

### Step 1: `timed`

Two upgrades over the lesson-3 timer. First, `try`/`finally`: the `finally` block works out the milliseconds and prints the function's name and time. It runs even when the function crashes, and even though `return` has already picked the value. Second, `@wraps` keeps the name and docstring. Create `toolkit.py`:

`step1/toolkit.py`:

```python
import time
from functools import wraps


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            ms = (time.perf_counter() - start) * 1000
            print(f"{func.__name__} took {ms:.0f} ms")
    return wrapper
```

Test it with `try1.py`. `load_report` pretends to work for a fifth of a second. Guess the four lines:

```python
import time

from toolkit import timed


@timed
def load_report(day):
    """Build the daily report."""
    time.sleep(0.2)
    return f"report for {day}"


print(load_report("Monday"))
print(load_report.__name__)
print(load_report.__doc__)
```

```bash
python step1/try1.py
```

```
load_report took 202 ms
report for Monday
load_report
Build the daily report.
```

The first line comes from the decorator: it appears first because the wrapper prints before the caller prints the result. Then the report, the name `load_report` and the docstring `Build the daily report.` Thanks to `wraps`, nothing was lost. Now the promise of `finally`. `broken_report` sleeps a tenth of a second and then raises a `ValueError`. Will we still get a timing line?

```python
import time

from toolkit import timed


@timed
def broken_report():
    time.sleep(0.1)
    raise ValueError("no data for today")


try:
    broken_report()
except ValueError as error:
    print("caught:", error)
```

```bash
python step1/try1b.py
```

```
broken_report took 105 ms
caught: no data for today
```

Yes: the timer reported, and the error still travelled on to the caller. Step 1 is done.

### Step 2: `retry`

Picture knocking on a shop door: nobody answers, you wait, knock again, and after three knocks you give up. A busy server often works a moment later. But not every error deserves a second try: a bug like dividing by zero fails the same way every time. So `retry` only tries again for errors that we mark. Make a new error with the two-line pattern from module 6, and add `retry` with three layers: `retry(times, delay)` takes the settings, `decorator` takes the function, `wrapper` does the work. Add these to `toolkit.py` (the error goes below the imports, `retry` goes at the end):

```python
class RetryableError(Exception):
    pass

# ...

def retry(times, delay=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except RetryableError as error:
                    print(f"attempt {attempt} failed: {error}")
                    if attempt == times:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator
```

In `wrapper`, a `for` loop counts the attempts from 1 up to `times`. The first success returns and ends everything. On a `RetryableError` we print which attempt failed. If it was the last attempt, a bare `raise` sends the same error up to the caller; otherwise `time.sleep(delay)` waits and the loop knocks again.

Test it. `load_catalog` counts its calls in a dictionary and raises `RetryableError("server busy")` on the first two calls. Guess the output:

```python
from toolkit import RetryableError, retry

state = {"calls": 0}


@retry(times=3, delay=0.1)
def load_catalog():
    state["calls"] += 1
    if state["calls"] < 3:
        raise RetryableError("server busy")
    return ["Python Basics", "Loops"]


print(load_catalog())
print("calls:", state["calls"])
```

```bash
python step2/try2.py
```

```
attempt 1 failed: server busy
attempt 2 failed: server busy
['Python Basics', 'Loops']
calls: 3
```

Two failed attempts, then the third call works. The caller never saw the trouble; it only waited a little longer. Now two edge cases: `always_down` raises on every call (`times=2`) and `buggy` divides by zero (`times=3`).

```python
from toolkit import RetryableError, retry


@retry(times=2)
def always_down():
    raise RetryableError("server busy")


@retry(times=3)
def buggy(total):
    return total / 0


try:
    always_down()
except RetryableError as error:
    print("gave up:", error)

buggy(10)
```

```bash
python step2/try2b.py
```

```
attempt 1 failed: server busy
attempt 2 failed: server busy
gave up: server busy
Traceback (most recent call last):
  File "step2/try2b.py", line 19, in <module>
    buggy(10)
    ~~~~~^^^^
  File "step2/toolkit.py", line 27, in wrapper
    return func(*args, **kwargs)
  File "step2/try2b.py", line 11, in buggy
    return total / 0
           ~~~~~~^~~
ZeroDivisionError: division by zero
```

`always_down`: attempt 1 and 2 failed, and because the last attempt failed too, the error travels up and we catch it. `buggy`: no retry line at all, a `ZeroDivisionError` straight away, with a traceback through the wrapper. Retry never hides a bug, and that is the point.

### Step 3: `cache_for`

A cook has a notepad by the stove. A guest asks the price of course C101; the cook walks to the office, finds it, and writes it on the pad with the time. The next guest asking within a short while gets the answer from the pad. After a while the note is too old and the cook walks to the office again. The caches from lessons 3 and 5 never forget (or forget only when they run out of pages), never because of time. This one has a time limit, and it is the new idea. It is a decorator with a setting, so it has three layers again, and one dictionary `saved` lives in the middle layer. Add to `toolkit.py`:

```python
def cache_for(seconds):
    def decorator(func):
        saved = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in saved:
                value, stamp = saved[key]
                if now - stamp < seconds:
                    return value
            value = func(*args, **kwargs)
            saved[key] = (value, now)
            return value
        return wrapper
    return decorator
```

The wrapper builds a key from the call: the positional arguments and the keyword arguments turned into a sorted tuple, so the same arguments make the same key. `time.monotonic()` is a clock that only moves forward, so a change of the computer's time can never confuse it. If the key is saved and `now - stamp < seconds`, the note is fresh: return it and the real function is not called at all. Otherwise call the function, save the value together with the time, and return it.

Test it. `get_price` prints `looking up`, sleeps a fifth of a second to pretend to ask a database, and returns a price. Above it: `@timed` (so we can see the time) and `@cache_for(seconds=1)`. Ask for C101 twice, then C102, then wait 1.2 seconds and ask for C101 again:

```python
import time

from toolkit import cache_for, timed

PRICES = {"C101": 499, "C102": 799}


@timed
@cache_for(1)
def get_price(course_id):
    print("looking up", course_id)
    time.sleep(0.2)
    return PRICES[course_id]


print(get_price("C101"))
print(get_price("C101"))
print(get_price("C102"))
time.sleep(1.2)
print(get_price("C101"))
```

```bash
python step3/try3.py
```

```
looking up C101
get_price took 205 ms
499
get_price took 0 ms
499
looking up C102
get_price took 201 ms
799
looking up C101
get_price took 203 ms
499
```

The first call looks up and takes about 200 ms. The second prints no `looking up` and takes 0 ms: the notebook answered. C102 is a different key, so it looks up again. After 1.2 seconds the note is too old, so C101 is looked up again.

### Step 4: `require_login`

A doorman at the staff entrance looks at your badge before you step in. No badge, no entry, and what is behind the door never happens. The badge is a user object with a `name` and a `logged_in` flag. The test file uses a small dataclass from module 8; the toolkit never imports it, it only expects an object with these two attributes. Add a new error and `require_login` (no settings, so two layers only). Note that `user` comes first in `wrapper`: the first argument of a protected function must be the user.

```python
    pass


class LoginRequiredError(Exception):

# ...

def require_login(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.logged_in:
            msg = f"{user.name} must log in first"
            raise LoginRequiredError(msg)
        return func(user, *args, **kwargs)
    return wrapper
```

Test it. `enrol` takes a user and a course. Priya is logged in, Lukas is not. Guess both outputs:

```python
from dataclasses import dataclass

from toolkit import LoginRequiredError, require_login


@dataclass
class User:
    name: str
    logged_in: bool = False


@require_login
def enrol(user, course):
    return f"{user.name} is now in {course}"


priya = User("Priya", logged_in=True)
lukas = User("Lukas")

print(enrol(priya, "Python Basics"))
try:
    print(enrol(lukas, "Python Basics"))
except LoginRequiredError as error:
    print("refused:", error)
```

```bash
python step4/try4.py
```

```
Priya is now in Python Basics
refused: Lukas must log in first
```

Priya is enrolled. For Lukas the body of `enrol` never ran: the doorman stopped him at the door.

### Step 5: stacking

You can put more than one label above a function, like wrapping a gift: first the paper, then the ribbon. The label closest to the function is applied first, so `@timed` above `@retry` above the function means `load = timed(retry(load))`. The bottom label wraps first and the top one is outermost. Does the order matter? `flaky` raises `RetryableError` on the first two calls and works on the third. `load_one` has `timed` on top and `retry` below; `load_two` has `retry` on top and `timed` below. How many timing lines does each print?

```python
from toolkit import RetryableError, retry, timed

tries = {"one": 0, "two": 0}


def flaky(name):
    tries[name] += 1
    if tries[name] < 3:
        raise RetryableError("server busy")


@timed
@retry(times=3, delay=0.1)
def load_one():
    flaky("one")


@retry(times=3, delay=0.1)
@timed
def load_two():
    flaky("two")


load_one()
load_two()
```

```bash
python step5/try5.py
```

```
attempt 1 failed: server busy
attempt 2 failed: server busy
load_one took 205 ms
load_two took 0 ms
attempt 1 failed: server busy
load_two took 0 ms
attempt 2 failed: server busy
load_two took 0 ms
```

`load_one`: `timed` is outside, so it starts the clock once and the whole retry loop, with its two failures and the waiting, happens inside: one line of a little over 200 ms. `load_two`: `timed` is inside, so it measures each single attempt: three lines of about 0 ms. Neither is wrong; they answer different questions: how long did the whole job take, waiting included, or how long does one attempt take?

A rule of thumb for the whole toolkit: cheap checks go on the outside. `require_login` on top means a person who is not allowed never even starts the clock, the retry loop or the cache. The cache goes close to the function, so a hit skips only the slow work. Stacking needs no new code, so `step5/toolkit.py` is the same as step 4.

### Put it together: `toolkit.py` and `demo.py`

`toolkit.py` is now the drawer from module 7: two errors and four decorators in 67 lines. Here it is, complete:

`toolkit.py`:

```python
import time
from functools import wraps


class RetryableError(Exception):
    pass


class LoginRequiredError(Exception):
    pass


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            ms = (time.perf_counter() - start) * 1000
            print(f"{func.__name__} took {ms:.0f} ms")
    return wrapper


def retry(times, delay=0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except RetryableError as error:
                    print(f"attempt {attempt} failed: {error}")
                    if attempt == times:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator


def cache_for(seconds):
    def decorator(func):
        saved = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in saved:
                value, stamp = saved[key]
                if now - stamp < seconds:
                    return value
            value = func(*args, **kwargs)
            saved[key] = (value, now)
            return value
        return wrapper
    return decorator


def require_login(func):
    @wraps(func)
    def wrapper(user, *args, **kwargs):
        if not user.logged_in:
            msg = f"{user.name} must log in first"
            raise LoginRequiredError(msg)
        return func(user, *args, **kwargs)
    return wrapper
```

`demo.py` borrows the drawer. It imports the four decorators in one line and the two errors in another, defines a small user class, and the story is: `load_catalog` is flaky with `@timed` above `@retry`, `get_price` has `@cache_for`, and `enrol` has `@require_login` and calls `get_price`. `main` tells the story, and the guard `if __name__ == "__main__":` at the bottom lets another file import `demo` without running it.

`demo.py`:

```python
import time
from dataclasses import dataclass

from toolkit import timed, retry, cache_for, require_login
from toolkit import RetryableError, LoginRequiredError

PRICES = {"C101": 499, "C102": 799}
state = {"calls": 0}


@dataclass
class User:
    name: str
    logged_in: bool = False


@timed
@retry(times=3, delay=0.1)
def load_catalog():
    state["calls"] += 1
    if state["calls"] < 3:
        raise RetryableError("server busy")
    return list(PRICES)


@cache_for(1)
def get_price(course_id):
    print("looking up", course_id)
    time.sleep(0.2)
    return PRICES[course_id]


@require_login
def enrol(user, course_id):
    price = get_price(course_id)
    return f"{user.name} bought {course_id} for Rs {price}"


def main():
    print(load_catalog())
    priya, lukas = User("Priya", True), User("Lukas")
    print(enrol(priya, "C101"))
    print(enrol(priya, "C101"))
    try:
        enrol(lukas, "C101")
    except LoginRequiredError as error:
        print("refused:", error)
    funcs = enrol, get_price, load_catalog
    print([func.__name__ for func in funcs])


if __name__ == "__main__":
    main()
```

One question before the run: when Priya buys C101 a second time, will `looking up` appear again? And which names will the last line show?

```bash
python demo.py
```

```
attempt 1 failed: server busy
attempt 2 failed: server busy
load_catalog took 209 ms
['C101', 'C102']
looking up C101
Priya bought C101 for Rs 499
Priya bought C101 for Rs 499
refused: Lukas must log in first
['enrol', 'get_price', 'load_catalog']
```

Two failed attempts, the timing line and the catalog. Priya's first purchase looks up the price once; her second prints no `looking up`, because the notebook already had it. Lukas is refused. The names are `enrol`, `get_price`, `load_catalog`: correct, thanks to `wraps`.

### Where it breaks

A toolkit is finished only when you know where it breaks.

**1. The cache hands out the same list every time.** `lessons` returns a list and is cached for ten seconds. We append `Oops` to the first answer and ask again:

```python
from toolkit import cache_for


@cache_for(10)
def lessons(course_id):
    return ["Intro", "Loops"]


mine = lessons("C101")
mine.append("Oops")
print(lessons("C101"))
```

```bash
python extra/mutable.py
```

```
Traceback (most recent call last):
  File "extra/mutable.py", line 1, in <module>
    from toolkit import cache_for
ModuleNotFoundError: No module named 'toolkit'
```

The cache saved the list itself, not a copy; both names point at one object (names and objects lesson), so we changed the cached answer by accident. Cache numbers, text and things nobody edits, or return a copy.

**2. The key.** `greeting` takes a user and has `@cache_for`:

```python
from dataclasses import dataclass

from toolkit import cache_for


@dataclass
class User:
    name: str


@cache_for(10)
def greeting(user):
    return f"Welcome back, {user.name}"


print(greeting(User("Priya")))
```

```bash
python extra/unhashable.py
```

```
Traceback (most recent call last):
  File "extra/unhashable.py", line 3, in <module>
    from toolkit import cache_for
ModuleNotFoundError: No module named 'toolkit'
```

The key holds the user, and a normal dataclass has no hash (module 8). Cached inputs must be hashable; a frozen dataclass would work.

**3. Retry repeats the work.** `pay` adds the amount to a list of charges and then fails with "no reply from the bank". Maybe the money moved, maybe not. With `retry(times=2)`, what is in the list at the end?

```python
from toolkit import RetryableError, retry

charged = []


@retry(times=2)
def pay(amount):
    charged.append(amount)
    raise RetryableError("no reply")


try:
    pay(499)
except RetryableError:
    print("payment failed")
print("charged:", charged)
```

```bash
python extra/twice.py
```

```
Traceback (most recent call last):
  File "extra/twice.py", line 1, in <module>
    from toolkit import RetryableError, retry
ModuleNotFoundError: No module named 'toolkit'
```

499 twice: Priya was charged two times. Retry cannot know whether the first try did something. Only retry actions that are safe to repeat, like reading a page. Never retry a payment blindly.

**4. The wrong first argument.** `require_login` expects a user first; we pass the text `"Lukas"`:

```python
from toolkit import require_login


@require_login
def enrol(user, course_id):
    return f"{user.name} is in {course_id}"


print(enrol("Lukas", "C101"))
```

```bash
python extra/wrongarg.py
```

```
Traceback (most recent call last):
  File "extra/wrongarg.py", line 1, in <module>
    from toolkit import require_login
ModuleNotFoundError: No module named 'toolkit'
```

The message is right but it points inside the toolkit. Fixing it is one of the upgrades below.

### Upgrades to try yourself

Pick one and try it. Small upgrades like these are exactly how programmers learn.

- `require_role`: a decorator with a setting, `@require_role("instructor")`.
- Log every call to a file.
- A rate limit that refuses a user who calls too fast.
- A maximum size for the cache, so it cannot grow forever.
- A clear error in `require_login` when the first argument is not a user.

## Common mistakes

1. Forgetting `@wraps`: the decorated function loses its name and docstring.

2. Writing `@retry` instead of `@retry(times=3)`: a decorator with a setting must be called.

3. Retrying something that is not safe to repeat (a payment). Retry only reads and other safe actions, and only for errors you marked.

4. Caching a mutable value (a list) and then changing it: the cached answer changes too.

5. Using an unhashable argument, such as a plain dataclass, in a cached function.

6. Putting `@require_login` below a slow decorator: refuse people first, on the outside.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next: [M10-L01 · Type Hints](../../m10-type-hints-and-modern-python/m10-l01-type-hints/README.md). Your toolkit works with any function; next you will write down what each argument should be, so your editor warns you about a mistake before you run the code. (Module 9 has no practice sheet, so we go straight on.)
