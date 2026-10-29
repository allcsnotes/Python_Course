# M12-L04 · asyncio from Scratch

> Video: Module 12, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- The cook with three pots: the event loop, and coroutines as functions that can pause
- `async def`, `await` and `asyncio.run`: why a coroutine does nothing until the loop runs it
- Tasks, `asyncio.gather` and `asyncio.TaskGroup`: how to run jobs together (three waits of one second in one second)
- How a task group collects many errors into an exception group, and cancels the other jobs
- Time limits with `asyncio.timeout`, and the rule "only an `await` lets the cook turn away"
- Four mistakes

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- No Docker and no packages needed (only the standard library).
- [M12-L02 · Threads](../m12-l02-threads/README.md), the generators lesson ([M09-L02](../../m09-writing-pythonic-code/m09-l02-generators/README.md)) and exception groups ([M10-L04](../../m10-type-hints-and-modern-python/m10-l04-whats-new-in-modern-python/README.md)).
- **Timings depend on your computer.** The seconds below are from one real run; the waits here are `sleep`s, so they should be close to yours, but the counting example at the end depends on your processor.

## Files in this folder

| File | What it is |
|------|------------|
| `waits.py` | The hook: three pages, one second each, one worker |
| `never_awaited.py` | Calling an `async def` function does not run it |
| `run_hello.py` | `asyncio.run` runs a coroutine |
| `one_by_one.py` | Three `await`s in a row: three seconds |
| `tasks.py` | `create_task`: three waits together |
| `many.py` | One hundred pages with `gather` |
| `trace.py` | Watching the cook: start and done messages |
| `gather_errors.py` | `gather` loses errors |
| `group.py` | `asyncio.TaskGroup` |
| `emails.py` | A task group and `except*` on four emails |
| `cancel_group.py` | A failing task cancels the others |
| `timeout.py` | `asyncio.timeout` around a slow page |
| `timeout_bare.py` | What an unhandled timeout looks like |
| `blocking.py` | `time.sleep` inside a coroutine blocks everything |
| `forgot_await.py` | Mistake 1: forgetting `await` |
| `await_outside.py` | Mistake 2: `await` outside an `async def` |
| `nested_run.py` | Mistake 3: `asyncio.run` inside a coroutine |
| `cpu_async.py` | Mistake 4: `async` does not speed up counting |

## Follow along

### 1. The hook: one worker, three waits

Asha's site needs three course pages: `python`, `pytest` and `git`. Each page comes from a slow server and takes one second to arrive. In lesson 2, threads solved this kind of waiting: workers that wait together. Here is her new file. Do not worry about the new words yet: this whole lesson explains them one by one. Just read the shape. `fetch` waits one second and gives back the name of the page. `main` gathers the three fetches, and prints the list and the time. Three waits of one second each, and one worker. Guess the output.

```python
import asyncio
import time


async def fetch(page):
    await asyncio.sleep(1)
    return page


async def main():
    start = time.perf_counter()
    pages = await asyncio.gather(
        fetch("python"), fetch("pytest"), fetch("git"))
    print(pages)
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
```

```bash
python waits.py
```

```
['python', 'pytest', 'git']
took 1.00 s
```

The list of three pages, and `took 1.00 seconds`: three waits of one second, finished in one second by a single thread. No threads, no extra workers: one worker that does not stand still while it waits. The tool is `asyncio`, and it lives in the standard library. In lesson 1 it was the answer on the map for very many waits.

### 2. The cook with three pots

A cook has three pots on the stove: rice, lentils and soup, each needing ten minutes of boiling. The first cook starts the rice and stares at it for ten minutes, then does the lentils, then the soup: thirty minutes. That is a normal program: one job after another, even while a job is only waiting. The clever cook starts the rice and turns away at once, because boiling needs no help; starts the lentils; starts the soup; then walks along the stove, and whichever pot is ready gets attention. Ten minutes in total. Lesson 2 had another answer: hire three cooks, one for each pot. That works for a few pots, but a busy server may wait on ten thousand pots at once, and ten thousand cooks would fill the whole street. One clever cook is enough.

Now the Python names. The clever cook is the **event loop**: a loop that keeps asking "which job is ready?" and gives it a turn. Each pot is a **coroutine**: a function that can pause while it waits and carry on later. A function that can pause: you have met it, a generator (module 9, lesson 2): `yield` hands over a value and pauses, and `next` wakes the function up with all its names still alive. A coroutine is the same idea, written with different words.

Two rules to remember. One: the cook can only turn away at an `await`. A job that never says `await` keeps the cook all to itself until it finishes. Two: nobody is interrupted in the middle of a step. A job pauses only at an `await`, so between two awaits your code runs alone (which makes many bugs from lesson 2 impossible).

### 3. `async def`, `await` and `asyncio.run`

The smallest coroutine: a function called `hello` with two words in front, `async def`. Below it we call `hello()` once, keep the result in a name and print the name.

```python
async def hello():
    print("hello from a coroutine")


result = hello()
print(result)
```

```bash
python never_awaited.py
```

```
<coroutine object hello at 0x10452ac80>
<sys>:0: RuntimeWarning: coroutine 'hello' was never awaited
```

Nothing from inside the function! What we see is a coroutine object and its address in memory (yours will differ), and a warning from Python: the coroutine `hello` was never awaited. It is just like calling a generator function: calling an `async def` function does not run its body. It builds a coroutine, a paused function waiting for the event loop. The warning means: you built one and never ran it. To run a coroutine we hand it to the event loop with `asyncio.run`, which starts a new event loop, runs the coroutine until it ends, and closes the loop.

```python
import asyncio


async def hello():
    print("hello from a coroutine")


asyncio.run(hello())
```

```bash
python run_hello.py
```

```
hello from a coroutine
```

This time the body ran. So far: `async def` makes a coroutine function, calling it builds a coroutine, and `asyncio.run` runs it.

### 4. `await` alone is not enough

The word that matters most is `await`. It can only be written inside an `async def`. It means: pause me here until this has finished, and let the loop run another job meanwhile. When it has finished, `await` also gives back the result. In `fetch`, `await asyncio.sleep(1)` is the async kind of sleep: this coroutine pauses for one second and the cook is free for other jobs. Now a new `main` that awaits three fetches in three separate lines. Same `fetch`, one second each. Guess the total time.

```python
import asyncio
import time


async def fetch(page):
    await asyncio.sleep(1)
    return page


async def main():
    start = time.perf_counter()
    a = await fetch("python")
    b = await fetch("pytest")
    c = await fetch("git")
    print(a, b, c)
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
```

```bash
python one_by_one.py
```

```
python pytest git
took 3.00 s
```

Three seconds, not one. `await` means "wait here until this has finished", and the next line does not start before. So three awaits in a row are simply three waits in a row. `async def` and `await` alone do not make anything concurrent. To run jobs together we must start them all first and collect them afterwards. For that we need **tasks**.

### 5. Tasks and `gather`

A task is a coroutine that the loop has taken on. `asyncio.create_task` takes a coroutine, puts it on the stove and returns at once with a task object. It does not wait; the job starts as soon as the current code reaches an `await`. Three `create_task` lines (three pots on the stove), and only then do we collect the results with `await` in front of each task. Guess the time.

```python
import asyncio
import time


async def fetch(page):
    await asyncio.sleep(1)
    return page


async def main():
    start = time.perf_counter()
    a = asyncio.create_task(fetch("python"))
    b = asyncio.create_task(fetch("pytest"))
    c = asyncio.create_task(fetch("git"))
    print(await a, await b, await c)
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
```

```bash
python tasks.py
```

```
python pytest git
took 1.00 s
```

One second. When `main` awaits `a`, the loop starts `b` and `c` too and all three wait together. By the time `main` asks for `b` and `c`, they are finished. The total time is the longest job, not the sum.

Writing `create_task` and `await` for every job is long. The shortcut is `asyncio.gather`: give it coroutines, as many as you like; it makes tasks, runs them together and returns a list of the results in the order you gave them (this is the hook file `waits.py` you ran at the start). With a long list of pages we use the star (module 4, lesson 3) to spread a list into separate arguments. One hundred pages, built with a list comprehension, one second each:

```python
import asyncio
import time


async def fetch(page):
    await asyncio.sleep(1)
    return page


async def main():
    pages = [f"page {n}" for n in range(100)]
    start = time.perf_counter()
    results = await asyncio.gather(*[fetch(p) for p in pages])
    print(len(results), "pages")
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
```

```bash
python many.py
```

```
100 pages
took 1.00 s
```

One second again, still one thread. A hundred threads would be heavy; a hundred coroutines are light, because a coroutine is much smaller than a thread.

Now watch the cook at work. Each job prints `start`, sleeps, and prints `done`, but the times differ: python 3 seconds, pytest 1 second, git 2 seconds. Then `gather`, and we print the results. Guess the order of the lines.

```python
import asyncio


async def fetch(page, seconds):
    print("start", page)
    await asyncio.sleep(seconds)
    print("done ", page)
    return page


async def main():
    results = await asyncio.gather(
        fetch("python", 3),
        fetch("pytest", 1),
        fetch("git", 2),
    )
    print(results)


asyncio.run(main())
```

```bash
python trace.py
```

```
start python
start pytest
start git
done  pytest
done  git
done  python
['python', 'pytest', 'git']
```

`start python`, `start pytest`, `start git`: all three begin at once, before anything is done. Then `done pytest` after one second, `done git` after two, `done python` after three. And the list reads python, pytest, git: `gather` returns the results in the order you asked, not the order they finished. What the cook did: gave python a turn (it printed `start` and reached its `await`), then pytest, then git. All three paused and the cook had nothing to do. After one second pytest was ready and got a turn, and so on.

### 6. Errors: `gather` against `TaskGroup`

`gather` has a weak spot: errors. Three jobs: job 1 works; jobs 2 and 3 raise a `ValueError`. First we call `gather` inside a `try` and catch the `ValueError`. Then we call it again with `return_exceptions=True`.

```python
import asyncio


async def job(n):
    await asyncio.sleep(n / 10)
    if n > 1:
        raise ValueError(f"bad {n}")
    return "ok"


async def main():
    try:
        await asyncio.gather(job(1), job(2), job(3))
    except ValueError as error:
        print("first error only:", error)
    results = await asyncio.gather(
        job(1), job(2), job(3), return_exceptions=True)
    print(results)


asyncio.run(main())
```

```bash
python gather_errors.py
```

```
first error only: bad 2
['ok', ValueError('bad 2'), ValueError('bad 3')]
```

First line: only one error, `bad 2`. Job 3 also failed, but its error was lost. Second line: with `return_exceptions`, the list holds the results and the errors side by side, and you must check every item yourself.

Since Python 3.11 there is a safer tool: the **task group**. `async with asyncio.TaskGroup() as group:` (`async with` is the `with` statement for coroutines), and inside the block `group.create_task(...)` for each job.

```python
import asyncio
import time


async def fetch(page):
    await asyncio.sleep(1)
    return page


async def main():
    start = time.perf_counter()
    async with asyncio.TaskGroup() as group:
        a = group.create_task(fetch("python"))
        b = group.create_task(fetch("pytest"))
        c = group.create_task(fetch("git"))
    print(a.result(), b.result(), c.result())
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
```

```bash
python group.py
```

```
python pytest git
took 1.00 s
```

When the block ends, the task group waits for every task. After the block all three are finished, and each task's `.result()` gives its value. Why is it safer? The jobs live inside the block, so none can be forgotten and left running. And when something fails, the group tells you, and tells you all of it.

Now a promise from module 10, lesson 4: exception groups. It said "you will meet them when many jobs run together". This is that moment. Asha's mail again: four addresses. One is fine, two have no `@` sign, one ends in `.xx` (a slow server). `main` makes one task for each email inside a task group, then two blocks: `except* ValueError` and `except* TimeoutError`. The same shape as module 10. Guess the output.

```python
import asyncio


async def send(email):
    await asyncio.sleep(0.1)
    if "@" not in email:
        raise ValueError(f"bad: {email}")
    if email.endswith(".xx"):
        raise TimeoutError(f"slow: {email}")
    print("sent to", email)


emails = ["asha@x.com", "lukas.com", "priya@y.xx", "meera"]


async def main():
    try:
        async with asyncio.TaskGroup() as group:
            for email in emails:
                group.create_task(send(email))
    except* ValueError as errors:
        print("bad addresses:", len(errors.exceptions))
        for error in errors.exceptions:
            print(" ", error)
    except* TimeoutError as errors:
        print("slow servers:", len(errors.exceptions))


asyncio.run(main())
```

```bash
python emails.py
```

```
sent to asha@x.com
bad addresses: 2
  bad: lukas.com
  bad: meera
slow servers: 1
```

One sent to `asha@x.com`. Bad addresses: two (`lukas.com` and `meera`). Slow servers: one. When several tasks fail, the task group gathers every error into one exception group and `except*` sorts them.

One more question: when one job fails, what happens to the others? Here `slow` waits five seconds and has a `finally` line that prints. `broken` fails after half a second. `main` puts both in a task group, catches the error with `except*` and measures the time. How long does the whole run take?

```python
import asyncio
import time


async def slow():
    try:
        await asyncio.sleep(5)
    finally:
        print("slow: stopped early")


async def broken():
    await asyncio.sleep(0.5)
    raise ValueError("boom")


async def main():
    start = time.perf_counter()
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(slow())
            group.create_task(broken())
    except* ValueError:
        print("caught the error")
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
```

```bash
python cancel_group.py
```

```
slow: stopped early
caught the error
took 0.50 s
```

`slow: stopped early`, caught the error, about half a second. The group **cancelled** `slow`: it stopped at its `await`, its `finally` line ran, and the whole thing ended at half a second, not five. Notice that cleanup code in `finally` still runs. Which one should you use? For jobs that belong together, prefer the task group: errors are never lost and nothing is left running. `gather` is fine for a quick script, and its `return_exceptions` option is handy when you want every result, good or bad.

### 7. Time limits

Real servers sometimes never answer, and a program that waits for ever is a broken program. So we put a time limit around an `await`: `async with asyncio.timeout(1):`. If the block takes longer than one second, it is cancelled and a `TimeoutError` is raised. The slow page waits five seconds. We wrap its `await` in a timeout of one second and catch `TimeoutError`, printing `gave up`. Then we print the time. Guess the output.

```python
import asyncio
import time


async def slow_page():
    await asyncio.sleep(5)
    return "page"


async def main():
    start = time.perf_counter()
    try:
        async with asyncio.timeout(1):
            await slow_page()
    except TimeoutError:
        print("gave up")
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
```

```bash
python timeout.py
```

```
gave up
took 1.00 s
```

`gave up`, about one second. Five seconds of waiting, cut to one. What if we forget the `except`? A long traceback, because asyncio's own frames are inside (only the key lines are shown here):

```python
import asyncio


async def slow_page():
    await asyncio.sleep(5)
    return "page"


async def main():
    async with asyncio.timeout(1):
        await slow_page()


asyncio.run(main())
```

```bash
python timeout_bare.py
```

```
Traceback (most recent call last):
  File "timeout_bare.py", line 11, in main
    await slow_page()
  File "timeout_bare.py", line 5, in slow_page
    await asyncio.sleep(5)
  ...
Traceback (most recent call last):
  File "timeout_bare.py", line 14, in <module>
    asyncio.run(main())
  ...
  File "timeout_bare.py", line 10, in main
    async with asyncio.timeout(1):
  ...
    raise TimeoutError from exc_val
TimeoutError
```

Read it from the bottom: the last line says `TimeoutError`. It is a normal error, so it can be caught like any other.

### 8. The rule that decides everything: only `await` turns the cook away

Here is the hook file with one change: in `fetch`, `await asyncio.sleep(1)` becomes `time.sleep(1)`, the plain sleep from module 9.

```python
import asyncio
import time


async def fetch(page):
    time.sleep(1)
    return page


async def main():
    start = time.perf_counter()
    pages = await asyncio.gather(
        fetch("python"), fetch("pytest"), fetch("git"))
    print(pages)
    print(f"took {time.perf_counter() - start:.2f} s")


asyncio.run(main())
```

```bash
python blocking.py
```

```
['python', 'pytest', 'git']
took 3.01 s
```

About three seconds: back to one after another. `time.sleep` is not an `await`. While it sleeps, the whole thread sleeps, and the cook sleeps too. No other job gets a turn until it has finished. This is the trap: a function marked `async def` with a plain waiting call inside looks asynchronous and behaves like normal code. The rule: inside an `async def`, waiting must be an `await`. Any slow call without `await` freezes the whole loop.

### 9. Four mistakes

**1. Calling an async function without `await`.** In `main`, `name = get_name()` has no `await`. Then we print `name.upper()`.

```python
import asyncio


async def get_name():
    await asyncio.sleep(0.1)
    return "python"


async def main():
    name = get_name()
    print(name.upper())


asyncio.run(main())
```

```bash
python forgot_await.py
```

```
Traceback (most recent call last):
  File "forgot_await.py", line 14, in <module>
    asyncio.run(main())
    ~~~~~~~~~~~^^^^^^^^
  File "/usr/lib/python3.14/asyncio/runners.py", line 205, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/usr/lib/python3.14/asyncio/runners.py", line 128, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/usr/lib/python3.14/asyncio/base_events.py", line 720, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "forgot_await.py", line 11, in main
    print(name.upper())
          ^^^^^^^^^^
AttributeError: 'coroutine' object has no attribute 'upper'
<sys>:0: RuntimeWarning: coroutine 'get_name' was never awaited
```

`AttributeError: 'coroutine' object has no attribute 'upper'` and the old warning: never awaited. The name holds a coroutine, not the text. The fix: `name = await get_name()`. Whenever an error mentions a coroutine object, look for a missing `await`.

**2. `await` outside an `async def`.** A file with one line, `result = await asyncio.sleep(1)`:

```python
import asyncio

result = await asyncio.sleep(1)
```

```bash
python await_outside.py
```

```
  File "await_outside.py", line 3
    result = await asyncio.sleep(1)
             ^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: 'await' outside function
```

`SyntaxError: 'await' outside function`. The word `await` only works inside an `async def`. At the top level of a file, use `asyncio.run(...)`.

**3. `asyncio.run` inside a coroutine.** `main` calls `asyncio.run(inner())`:

```python
import asyncio


async def inner():
    print("inner")


async def main():
    asyncio.run(inner())


asyncio.run(main())
```

```bash
python nested_run.py
```

```
Traceback (most recent call last):
  File "nested_run.py", line 12, in <module>
    asyncio.run(main())
    ~~~~~~~~~~~^^^^^^^^
  File "/usr/lib/python3.14/asyncio/runners.py", line 205, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "/usr/lib/python3.14/asyncio/runners.py", line 128, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/usr/lib/python3.14/asyncio/base_events.py", line 720, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "nested_run.py", line 9, in main
    asyncio.run(inner())
    ~~~~~~~~~~~^^^^^^^^^
  File "/usr/lib/python3.14/asyncio/runners.py", line 201, in run
    raise RuntimeError(
        "asyncio.run() cannot be called from a running event loop")
RuntimeError: asyncio.run() cannot be called from a running event loop
<sys>:0: RuntimeWarning: coroutine 'inner' was never awaited
```

`RuntimeError: asyncio.run() cannot be called from a running event loop`. One loop is already running. Inside a coroutine, use `await inner()`.

**4. Using `async` for counting.** `async` only helps with waiting. Three counting coroutines, 100 million steps each, run with `gather`:

```python
import asyncio
import time

N = 100_000_000


async def count(n):
    while n > 0:
        n -= 1


async def main():
    start = time.perf_counter()
    await count(N)
    one = time.perf_counter() - start
    start = time.perf_counter()
    await asyncio.gather(count(N), count(N), count(N))
    three = time.perf_counter() - start
    print(f"one count:    {one:.2f} s")
    print(f"three counts: {three:.2f} s")


asyncio.run(main())
```

```bash
python cpu_async.py
```

```
one count:    0.97 s
three counts: 2.87 s
```

Three together take about three times as long as one: no gain, because counting never reaches an `await`, so the cook never turns away. For computing, use processes (lesson 3).

## Common mistakes

1. Calling an `async def` function and forgetting `await` (or `asyncio.run`): nothing runs.

2. Writing three `await`s in a row and expecting them to overlap. Use tasks, `gather` or a task group.

3. Using `time.sleep` (or any slow plain call) inside a coroutine: it freezes the whole loop. Use `await asyncio.sleep(...)`.

4. Calling `asyncio.run` inside a coroutine.

5. Using `async` for CPU work: it does not help. Use processes.

6. Forgetting a time limit around a call to a server that might never answer.

## Clean up

Nothing to clean up. Delete the folder if you want it gone.

## Next

Next lesson: [M12-L05 · Async in Practice](../m12-l05-async-in-practice/README.md). We will fetch real web pages from a slow local server with `httpx`, limit how many run at once with a semaphore, cancel tasks, and more.

Your turn first: change the hook to ten pages and watch the time; replace the `await sleep` with `time.sleep` and measure; make one email in the task group fail on purpose and catch it with `except*`; wrap a slow call in a timeout.
