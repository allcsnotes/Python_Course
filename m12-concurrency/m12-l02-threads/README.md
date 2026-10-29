# M12-L02 · Threads

> Video: Module 12, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- Why threads speed up waiting jobs (eight pages: 5 seconds became 1)
- How to start threads and wait for them: `Thread(target=..., args=(...,))`, `start()`, `join()`
- The thread pool: `ThreadPoolExecutor`, `map`, `submit` and `as_completed`, and how many workers to use
- How errors travel through a future (`result()`)
- Race conditions, and how to fix them with a `Lock` (and why to keep the lock small)
- Queues, and five pitfalls

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- A virtual environment with `httpx` (pinned in `requirements.txt`): `python -m venv .venv`, activate it, `pip install -r requirements.txt`. No Docker needed.
- [M12-L01 · CPU-Bound vs IO-Bound](../m12-l01-cpu-bound-vs-io-bound/README.md) and [M11-L03 · The GIL](../../m11-python-under-the-hood/m11-l03-the-gil-and-free-threaded-python/README.md).
- The lesson uses a small local web server (`server.py`, port 8122) with eight "course pages", each answering after a different delay. It makes no real internet calls. **Timings depend on your computer**: the seconds below are from one real run, so yours will differ a little; the pattern will be the same. Numbers like the lost-updates total change on every run.

## Files in this folder

| File | What it is |
|------|------------|
| `server.py` | The fake course service on localhost:8122 (eight pages, different delays) |
| `requirements.txt` | `httpx==0.28.1` |
| `pages.py` | `fetch(n)`: asks the service for course `n`'s title |
| `sequential.py` | The dashboard one page after the other (the hook) |
| `threaded.py` | One thread per page |
| `hello_thread.py` | The smallest thread |
| `daemon_beat.py` | A daemon thread |
| `pool_map.py` | A thread pool with `map` |
| `pool_submit.py` | `submit` and `as_completed` |
| `workers_table.py` | The same eight pages with 1, 2, 4, 8 and 16 workers |
| `pool_error.py` | A failing job inside a pool |
| `lost_updates.py` | A shared total without a lock: updates vanish |
| `locked.py` | The same with a lock |
| `lock_too_big.py` | A lock around the whole job, slow fetch included |
| `queue_workers.py` | Workers taking jobs from a queue |
| `join_inside.py` | Pitfall 1: `join` inside the loop |
| `target_called.py` | Pitfall 2: brackets after the target |
| `args_comma.py` | Pitfall 3: the missing comma in `args` |
| `silent.py` | Pitfall 4: an error nobody asks about |
| `deadlock.py` | Pitfall 5: a lock taken twice |

## Follow along

### 1. Set up: the server and the environment

Create and activate a virtual environment and install `httpx` (module 7):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the fake course service in its own terminal window and leave it running (stop it with Control-C at the end):

```bash
python server.py
```

Every other command in this lesson runs in a second terminal, in the same folder, with the same virtual environment active. `pages.py` has the function every example uses:

```python
import httpx

BASE = "http://localhost:8122"


def fetch(n):
    response = httpx.get(f"{BASE}/courses/{n}")
    if response.status_code != 200:
        message = f"course {n}: status {response.status_code}"
        raise ValueError(message)
    return response.json()["title"]
```

### 2. The hook: eight pages, five seconds

Last lesson's map said: a handful of waiting jobs, use threads. Asha is building the dashboard of allcsvideos.com. It needs the titles of eight course pages, and each title comes from the course service, which answers after a different delay. `show` prints one line: the course number and its title. A loop asks for the eight courses one after another, with a stopwatch around it. Real services are never equally fast. Guess: in what order will the lines appear, and about how long will all eight take?

```python
import time
from pages import fetch


def show(n):
    print(f"course {n}: {fetch(n)}")


start = time.perf_counter()
for n in range(1, 9):
    show(n)
print(f"{time.perf_counter() - start:.2f} s")
```

```bash
python sequential.py
```

```
course 1: Python
course 2: SQL
course 3: Docker
course 4: Git
course 5: Linux
course 6: Redis
course 7: Kafka
course 8: Spring Boot
5.01 s
```

In order, one to eight, and about five seconds. The program did nothing but wait: it asked for a page, sat still until the answer came, and only then asked for the next one. Waiting is exactly what threads are good at (module 11, lesson 3). Here is the same dashboard with one thread for every page. Do not worry about the details yet; we take them apart soon.

```python
import threading
import time
from pages import fetch


def show(n):
    print(f"course {n}: {fetch(n)}")


start = time.perf_counter()
threads = []
for n in range(1, 9):
    t = threading.Thread(target=show, args=(n,))
    t.start()
    threads.append(t)
for t in threads:
    t.join()
print(f"{time.perf_counter() - start:.2f} s")
```

```bash
python threaded.py
```

```
course 4: Git
course 7: Kafka
course 2: SQL
course 5: Linux
course 3: Docker
course 8: Spring Boot
course 1: Python
course 6: Redis
1.04 s
```

Look at the order: course 4 (Git, the quickest page) first, course 6 (Redis, the slowest) last. And the time: five seconds became one. Not eight times faster: as fast as the slowest single page. All eight waits happened together. But threads share data, and shared data can go wrong. Today you use threads properly and meet the lock that module 11 promised.

### 3. The office with one worker, and one whiteboard

Picture a small office with one worker. On the desk lie eight jobs: ask the course service for a title. The worker takes the first job, asks and waits for the answer. Only when it arrives do they take the next. Most of that time the worker is not busy at all: waiting needs no thinking, and a waiting thread puts the pen down (M11-L03). So give the office more workers. A **thread** is one more worker inside the same program. Eight workers each take one job, ask at the same moment, and all wait together. The office is finished when the slowest answer arrives.

Now the important part. All the workers sit in one office, and in that office there is one whiteboard. Every variable, list and dictionary of the program is written on that whiteboard, and every worker can read and change it. Sharing is useful: a worker can leave an answer for everyone. It is also dangerous: two workers may write on the same spot at the same moment. We will see that happen for real and fix it. This lesson has four jobs: start workers and wait for them, let a team do the chores, collect answers and errors, and protect the whiteboard.

### 4. Start a thread and wait for it

The smallest thread: `greet` takes a name, asks Python for the current thread, takes its name and prints it with a hello. `threading.Thread` makes the worker but does not start it. `target` is the job: the function `greet`. Look closely: **no round brackets after `greet`**. We hand over the recipe, we do not cook it. `args` is the tuple of inputs. `start()` sets the worker going and the main program carries on at once. `join()` makes the main program wait until that thread has finished. Guess the output (two lines, and what name does the thread have?):

```python
import threading


def greet(name):
    me = threading.current_thread().name
    print(f"{me}: hello, {name}")


t = threading.Thread(target=greet, args=("Lukas",))
t.start()
t.join()
print("main: all done")
```

```bash
python hello_thread.py
```

```
Thread-1 (greet): hello, Lukas
main: all done
```

The first thread you make is `Thread-1` (and in brackets the name of its function), the second `Thread-2`, and so on. The program itself also runs in a thread, called `MainThread`.

Now we can read the dashboard file slowly (`threaded.py` above). First an empty list called `threads`. The loop makes one thread for each course number: `target=show`, `args=(n,)` (with its comma), `start()` sets it going and the thread goes into the list. Then a second loop: for each thread in the list, `join()`. Why two loops? Start every thread first so that all the waiting happens together; only then wait for them one by one (pitfall 1 shows what goes wrong otherwise). One more fact: a thread cannot hand an answer back. Whatever the target function returns is thrown away. That is why `show` prints inside the thread. A pool (next step) solves that.

One last option, briefly: **daemon**. A daemon thread is a background helper. This function prints `still alive` every half second, forever. We start it as a daemon, then `main` sleeps 1.2 seconds and prints:

```python
import threading
import time


def heartbeat():
    while True:
        print("still alive")
        time.sleep(0.5)


threading.Thread(target=heartbeat, daemon=True).start()
time.sleep(1.2)
print("main is done")
```

```bash
python daemon_beat.py
```

```
still alive
still alive
still alive
main is done
```

Three times `still alive`, then `main is done`, and the program ends. A daemon never keeps the program alive: when the main thread is finished, the daemon is simply stopped. Without `daemon=True` the program would never end.

### 5. The thread pool: `ThreadPoolExecutor`

Starting threads by hand has chores: a list to keep, two loops, no answers coming back and no limit on how many you start. The standard library has a helper, the **thread pool**: like a post-office counter with a fixed number of clerks, the jobs wait in a line and free workers take them. From `concurrent.futures` we import `ThreadPoolExecutor`. `with ThreadPoolExecutor(max_workers=8) as pool:` (the `with` statement from module 9). Inside the block, one line does the work: `pool.map(fetch, range(1, 9))` hands each number to `fetch` on a free worker and gives the answers back **in the same order as the numbers**.

```python
import time
from concurrent.futures import ThreadPoolExecutor
from pages import fetch

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=8) as pool:
    for title in pool.map(fetch, range(1, 9)):
        print(title)
print(f"{time.perf_counter() - start:.2f} s")
```

```bash
python pool_map.py
```

```
Python
SQL
Docker
Git
Linux
Redis
Kafka
Spring Boot
1.04 s
```

In order: Python, SQL, Docker, Git, Linux, Redis, Kafka, Spring Boot. About one second, the same speed as the threads by hand. Git finished first, but `map` still gives the answers in the order you asked. Fewer lines, answers come back, no joining by hand.

Sometimes you want each answer as soon as it is ready. For that there is `submit`. `pool.submit(fetch, n)` hands over one job and gives back a **future**: a ticket for an answer that does not exist yet, like the buzzer at a restaurant. `as_completed` takes the tickets and hands them back in the order they finish. Our tickets are the keys of a dictionary (a dictionary comprehension from module 5), so each ticket remembers its course number.

```python
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from pages import fetch

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = {pool.submit(fetch, n): n for n in range(1, 9)}
    for future in as_completed(futures):
        gone = time.perf_counter() - start
        n = futures[future]
        print(f"{gone:.1f} s  course {n}: {future.result()}")
```

```bash
python pool_submit.py
```

```
0.2 s  course 4: Git
0.3 s  course 7: Kafka
0.4 s  course 2: SQL
0.6 s  course 5: Linux
0.7 s  course 3: Docker
0.8 s  course 8: Spring Boot
0.9 s  course 1: Python
1.0 s  course 6: Redis
```

Course 4 first, at about 0.2 seconds, then 7, 2, 5, 3, 8 and 1; course 6 last, at one second. The fastest page comes first. Use `map` when you want the answers in order, and `submit` with `as_completed` when you want the fastest first.

How many workers do you need? `max_workers` is the size of the team. This file runs the same eight pages with 1, 2, 4, 8 and 16 workers. Guess the output. Which of the five will be the fastest?

```python
import time
from concurrent.futures import ThreadPoolExecutor
from pages import fetch

for workers in (1, 2, 4, 8, 16):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(fetch, range(1, 9)))
    elapsed = time.perf_counter() - start
    print(f"workers={workers}: {elapsed:.2f} s")
```

```bash
python workers_table.py
```

```
workers=1: 4.99 s
workers=2: 2.84 s
workers=4: 1.62 s
workers=8: 1.02 s
workers=16: 1.01 s
```

One worker takes about five seconds, exactly like the plain loop. More workers help until there is one worker per job; sixteen workers for eight jobs is no better than eight. If you give no number, Python picks one for you: the number of cores plus four, but at most 32. And a warning for real services: a thousand workers means a thousand open connections, and the other side may say no. Use as many as you have jobs waiting, and no more than the other side can take.

### 6. Errors travel through the future

What happens when a job fails? Suppose the service has no course 13. It answers with status 404 and `fetch` raises a `ValueError` (module 6). In a pool, that error does not crash your program on its own; it is kept inside the future. This file submits three jobs: courses 1, 13 and 3. Then, for each future, we try `future.result()` and `except ValueError` prints `failed` and the message. Guess the output.

```python
from concurrent.futures import ThreadPoolExecutor
from pages import fetch

with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(fetch, n) for n in (1, 13, 3)]
    for future in futures:
        try:
            print(future.result())
        except ValueError as error:
            print("failed:", error)
```

```bash
python pool_error.py
```

```
Python
failed: course 13: status 404
Docker
```

`Python`, then `failed: course 13: status 404`, then `Docker`. The failure belonged to one future and did not stop the other two. In a pool, errors travel through the ticket, and you decide what to do with them when you ask for the result.

### 7. Break a shared number for real, then fix it with a lock

The promise from module 11, lesson 3: four threads added one to a shared total and the answer was wrong. The fix is a lock of your own. The shared total starts at zero. `add_many` adds one, `count` times. `global total` says: this name lives on the shared whiteboard. Each round has three steps: read the number into `current`, add one, write it back. (A tiny `time.sleep(0)` between read and write makes the bug show every time, instead of rarely.) Four threads, each adding 50,000 times. The right answer is 200,000. Guess the last line.

```python
import threading
import time

total = 0


def add_many(count):
    global total
    for _ in range(count):
        current = total
        time.sleep(0)
        total = current + 1


threads = [threading.Thread(target=add_many, args=(50_000,))
           for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print("expected 200000, got", total)
```

```bash
python lost_updates.py
```

```
expected 200000, got 50006
```

Far less than 200,000 (in the video: 50,012, three quarters of all additions vanished). Run it again and the number changes a little. Why? Take two workers and a total of 5. Worker A reads 5. Then A pauses and B gets a turn. B also reads 5. A writes 6. B writes 6. Two additions happened, but the total only went up by one. It is a **race condition**: the result depends on which thread gets there first. The three steps (read, add, write) must happen as one piece. A piece of code that only one thread at a time may run is a *critical section*.

The tool is a **lock**. Think of the hotel from module 9: to use the whiteboard room, take the one key from its hook, go in, do your three steps, come out and hang the key back. While you hold the key, nobody else can go in. In code: `threading.Lock()`, made outside the function so all four threads share the same lock, and around the three steps `with lock:` (you know this from context managers). Same program, same four threads, now with the lock. What does the last line print this time?

```python
import threading
import time

total = 0
lock = threading.Lock()


def add_many(count):
    global total
    for _ in range(count):
        with lock:
            current = total
            time.sleep(0)
            total = current + 1


threads = [threading.Thread(target=add_many, args=(50_000,))
           for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print("expected 200000, got", total)
```

```bash
python locked.py
```

```
expected 200000, got 200000
```

Exactly right, and exactly right every time. The three steps now happen one worker at a time, so no update is lost.

A lock has a price: while one thread holds it, all the others wait. So what if we put the lock around the whole job, including the slow page fetch? How long will it take?

```python
import threading
import time
from pages import fetch

lock = threading.Lock()


def show(n):
    with lock:
        print(f"course {n}: {fetch(n)}")


start = time.perf_counter()
threads = []
for n in range(1, 9):
    t = threading.Thread(target=show, args=(n,))
    t.start()
    threads.append(t)
for t in threads:
    t.join()
print(f"{time.perf_counter() - start:.2f} s")
```

```bash
python lock_too_big.py
```

```
course 1: Python
course 2: SQL
course 3: Docker
course 4: Git
course 5: Linux
course 6: Redis
course 7: Kafka
course 8: Spring Boot
4.98 s
```

About five seconds again. Eight threads, but only one of them could be inside the lock at a time, so the waiting happened one after another. A lock around a slow wait throws the speed away. So two rules: **lock only the steps that touch shared data, never the waiting**; and **every thread must use the same lock for the same data**. A lock that one thread forgets to take protects nothing.

### 8. Pass notes with a queue

There is a calmer way to share work: do not share the whiteboard, pass notes. A **queue** is a line of jobs: `put` adds a job at the end and `get` takes the first one. The queue from the standard library has a lock built in. This file puts the eight course numbers into a queue. Each worker loops: `get_nowait` takes the next number; when the line is empty it raises `queue.Empty`, the worker catches that and returns, and its day is over.

```python
import queue
import threading
from pages import fetch

jobs = queue.Queue()
for n in range(1, 9):
    jobs.put(n)


def worker():
    name = threading.current_thread().name
    while True:
        try:
            n = jobs.get_nowait()
        except queue.Empty:
            return
        print(f"{name} took course {n}: {fetch(n)}")


team = [threading.Thread(target=worker) for _ in range(3)]
for t in team:
    t.start()
for t in team:
    t.join()
```

```bash
python queue_workers.py
```

```
Thread-2 (worker) took course 2: SQL
Thread-2 (worker) took course 4: Git
Thread-3 (worker) took course 3: Docker
Thread-1 (worker) took course 1: Python
Thread-1 (worker) took course 7: Kafka
Thread-2 (worker) took course 5: Linux
Thread-3 (worker) took course 6: Redis
Thread-1 (worker) took course 8: Spring Boot
```

It can differ on every run (so yours will differ), but the idea is clear: the thread that got the quick pages kept coming back for more. Each course was taken by exactly one worker, none twice. A good habit: when threads must share, prefer a queue, or the answers of a pool, over a shared variable with a lock. Then there are fewer places where you can forget a lock.

### 9. Five pitfalls

**1. `join` inside the loop.** This loop starts a thread and joins it straight away. How long will it take?

```python
import threading
import time
from pages import fetch

start = time.perf_counter()
for n in range(1, 9):
    t = threading.Thread(target=fetch, args=(n,))
    t.start()
    t.join()
print(f"{time.perf_counter() - start:.2f} s")
```

```bash
python join_inside.py
```

```
4.99 s
```

About five seconds, the same as no threads at all. The second thread cannot start until the first has finished, so there is never more than one worker. Start all the threads first and join in a separate loop.

**2. Brackets after the target.** `fetch(1)` with brackets runs the function right now, in the main program, and hands its answer to the thread. What happens?

```python
import threading
from pages import fetch

t = threading.Thread(target=fetch(1))
t.start()
t.join()
print("done")
```

```bash
python target_called.py
```

```
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/lib/python3.14/threading.py", line 1082, in _bootstrap_inner
    self._context.run(self.run)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/usr/lib/python3.14/threading.py", line 1024, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: 'str' object is not callable
done
```

The program waited almost a second first, because `fetch` really ran in the main program. Then the thread tried to run the answer, the text `Python`, as if it were a function: `TypeError: 'str' object is not callable`. The program still printed `done`: an error inside a thread does not stop the main program. (The long traceback through `threading.py` is the same on every Python 3.14.)

**3. The missing comma.** `args=(1)` is only the number 1 in brackets, not a tuple:

```python
import threading
from pages import fetch

t = threading.Thread(target=fetch, args=(1))
t.start()
t.join()
print("done")
```

```bash
python args_comma.py
```

```
Exception in thread Thread-1 (fetch):
Traceback (most recent call last):
  File "/usr/lib/python3.14/threading.py", line 1082, in _bootstrap_inner
    self._context.run(self.run)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/usr/lib/python3.14/threading.py", line 1024, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: pages.fetch() argument after * must be an iterable, not int
done
```

`TypeError: pages.fetch() argument after * must be an iterable, not int`. Python wants a tuple of inputs and got a plain number. And again the program went on to print `done`. Write `args=(1,)`.

**4. An error nobody asks about.** This pool submits course 13, which does not exist, and never looks at the result. Will we see an error?

```python
from concurrent.futures import ThreadPoolExecutor
from pages import fetch

with ThreadPoolExecutor() as pool:
    pool.submit(fetch, 13)
print("finished, and no error was shown")
```

```bash
python silent.py
```

```
finished, and no error was shown
```

No error at all: `finished, and no error was shown`. The failure sits inside the future and nobody opened it. A pool never shouts. Always call `result()` on your futures, or loop over `map`, so that errors come out.

**5. A lock taken twice.** `update` takes the lock, then calls `record`, and `record` wants the same lock. A plain lock does not know that the same thread already holds it, so the thread waits for itself, for ever. The program is run for two seconds and then stopped with Control-C:

```python
import threading

lock = threading.Lock()


def record():
    with lock:
        print("writing the record")


def update():
    with lock:
        print("got the lock")
        record()


update()
```

```bash
python deadlock.py
```

```
got the lock
^C
Traceback (most recent call last):
  ...
  File "deadlock.py", line 7, in record
    with lock:
         ^^^^
KeyboardInterrupt
```

It printed, got the lock, and then nothing: stuck. The Control-C error report shows exactly where it waits: the `with lock` line inside `record`. The fix: never call code that takes a lock from code that already holds the same lock.

## Common mistakes

1. Calling `join()` inside the loop that starts the threads: no overlap, no speed-up.

2. Writing `target=fetch(1)` (brackets) or `args=(1)` (no comma).

3. Changing shared data from several threads without a lock: updates vanish. Even a plain `total += 1` is three steps.

4. Putting the lock around a slow wait: the speed is gone. Lock only the steps that touch shared data.

5. Never calling `result()` on futures: errors in a pool stay silent.

6. Taking the same plain lock twice in one thread: the thread waits for itself for ever.

## Clean up

Stop the course service with Control-C in its terminal window, and delete the `.venv` folder you made (`rm -rf .venv`) if you do not need it any more.

## Next

Next lesson: [M12-L03 · Processes](../m12-l03-processes/README.md). Threads cannot make counting faster on normal Python. Next, we use more than one pen at a time.

Your turn first: change `max_workers` and watch the time; run `lost_updates.py` a few times, then add the lock; put the lock around the fetch and time it; and use `as_completed` to print only the slowest course.
