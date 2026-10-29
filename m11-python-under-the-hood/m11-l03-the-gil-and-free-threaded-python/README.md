# M11-L03 · The GIL and Free-Threaded Python

> Video: Module 11, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- What the GIL (Global Interpreter Lock) is: one pen for the whole Python program
- Why it exists (reference counts) and what it costs: CPU-bound threads do not speed up, waiting threads do
- How to ask which Python you are running: `sys._is_gil_enabled()` and `python -VV`
- How to install and run free-threaded Python (`3.14t`) with `uv`, and the three catches
- Why free-threaded Python does not make unsafe code safe (lost updates)

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `uv` from module 7 (`uv python install 3.14t` installs the free-threaded build, about 25 MB). Docker is not needed.
- [M11-L02 · Memory and Garbage Collection](../m11-l02-memory-and-garbage-collection/README.md) (reference counts).
- **Timings depend on your computer.** The seconds in the counting examples are the numbers recorded for the video on a quiet 10-core Mac (the median of three runs), so yours will differ. When we re-ran every file while other programs were using the same computer, the exact seconds moved a lot, but the programs, the GIL flags and the pattern held. The `which_gil.py`, `-VV`, `io_bound.py` and `lost_updates.py` outputs below are fresh runs. What matters is the pattern: which runs are equal and which are faster. The `lost_updates.py` total is different on every run.

## Files in this folder

| File | What it is |
|------|------------|
| `speed.py` | The hook: one thread counts 300 million, then four threads count a quarter each |
| `speed8.py` | The same with eight threads |
| `which_gil.py` | Is the GIL on? Was this Python built without it? |
| `io_bound.py` | Waiting work: four waits one by one, then in four threads |
| `cpu_bound.py` | `speed.py` plus a line that prints whether the GIL is on |
| `lost_updates.py` | Four threads add 1 a million times each to a global total |
| `no_join.py` | Pitfall: timing threads without `join` |

## Follow along

### 1. The hook: four workers, same time

Asha's allcsvideos.com server has a heavy job: it counts through a huge number, a stand-in for real heavy work like building a report. Her computer has ten cores (a core is one worker inside the processor, able to do a job at the very same moment as the others). `count` counts a number down to zero, one step at a time: pure computing, no waiting. `run` starts some **threads** (one more line of work running inside your program; module 12 teaches them properly) and waits for them to finish: `start` sets a thread going and `join` waits for it. At the bottom there are two timings: one thread counts all 300 million, then four threads each count a quarter, 75 million. The total work is the same. Four workers, ten cores: Asha expects the second line to take about a quarter of the time. Guess the output.

```python
import threading
import time


def count(n):
    while n > 0:
        n -= 1


def run(threads, n):
    start = time.perf_counter()
    workers = [threading.Thread(target=count, args=(n,))
               for _ in range(threads)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    return time.perf_counter() - start


print(f"one thread:   {run(1, 300_000_000):.2f} s")
print(f"four threads: {run(4, 75_000_000):.2f} s")
```

```bash
python speed.py
```

```
one thread:   2.62 s
four threads: 2.62 s
```

The very same time. Four workers did not make the job one bit faster. It is not a bug in Asha's code. It is a rule inside Python, a rule about one pen.

### 2. One pen: the GIL

Picture a small office with one pen. Four workers sit at four desks, each with a report to write, but there is only one pen in the whole office. Only the worker holding the pen can write; the others wait. After a very short time the pen is passed to the next worker, who writes for a moment and passes it on. How many reports get written in an hour? Exactly as many as one worker with that pen could write. Only more pens would add speed.

In Python the workers are threads and the pen is the **GIL**, the Global Interpreter Lock. *Interpreter* is the part of Python that runs your code (module 1, lesson 4); *lock* means only one holder at a time. The rule: in one Python program, only the thread that holds the GIL can run Python code. Every other thread waits for its turn.

But here is the good part. A worker who must wait for a delivery puts the pen down while waiting, and someone else picks it up. Waiting does not need the pen. So there are two kinds of work: work where a worker is busy thinking and writing every moment (needs the pen all the time), and work where a worker mostly waits (the pen is free most of the time).

### 3. Why does the pen exist?

Remember the meeting room with a counter on the door (the last lesson)? Every object in Python has such a counter, its reference count. Now two threads use the same object at the same instant and each adds a pointer. Thread A reads the count: 2. Thread B also reads the count: 2. Thread A writes 3. Thread B writes 3. Two pointers were added, so the count should be 4, but it says 3. A count that is too low is dangerous: Python may free the object while a pointer still points at it, and the program crashes. A count that is too high means the object is never freed: a leak.

So Python needs a guard. One choice: a small lock on every single object. That is millions of locks, a lot of extra work and a slowdown even for programs with one thread. The other choice: one big lock for everything, the GIL. Simple and fast for one thread. When Python got threads, in the 1990s, computers mostly had one core, so one pen cost almost nothing, and the libraries written in C that Python uses for speed could also rely on the pen. Today a laptop has ten cores and the one pen is a limit. That is why people worked for years to remove it.

### 4. Measure the pen: CPU-bound work

The function `count` is CPU work: the processor is busy every moment and nobody waits. We call that **CPU-bound**: the limit is how fast the processor can think. Every thread needs the pen all the time, so only one of them counts at any moment and the total time stays the same as one thread. How fast is the pen passed on? A small file prints three answers: is the GIL on, was this Python built without it, and the switch interval.

```python
import sys
import sysconfig

print("GIL on:", sys._is_gil_enabled())
print("built without GIL:",
      bool(sysconfig.get_config_var("Py_GIL_DISABLED")))
print("switch interval:", sys.getswitchinterval())
```

```bash
python which_gil.py
```

```
GIL on: True
built without GIL: False
switch interval: 0.005
```

`sys._is_gil_enabled()` (the name starts with an underscore) asks: is the pen in use? The answer is `True`. The second line we use later. `sys.getswitchinterval()` says 0.005: five thousandths of a second. A thread that has held the pen for about that long is asked to pass it on if another thread is waiting. Fast enough that all four threads look busy, but never two at the same time.

What if we change it? Eight threads instead of four, each counting a smaller share (37.5 million). Faster, slower, or the same?

```python
import threading
import time


def count(n):
    while n > 0:
        n -= 1


def run(threads, n):
    start = time.perf_counter()
    workers = [threading.Thread(target=count, args=(n,))
               for _ in range(threads)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    return time.perf_counter() - start


print(f"one thread:   {run(1, 300_000_000):.2f} s")
print(f"eight threads: {run(8, 37_500_000):.2f} s")
```

```bash
python speed8.py
```

```
one thread:   2.68 s
eight threads: 2.69 s
```

The same again. More workers, same pen. So, plainly: for CPU-bound work, threads on normal Python do not make the program faster. It is not Asha's mistake; it is how the pen works. Module 12 shows the tool for this job.

### 5. Measure the pen: waiting work

Now the other kind of work: asking a server for data, reading a file, asking a database. The computer sends the request and then waits. This is **I/O-bound** (I/O means input and output). To test waiting we use `time.sleep`, a good stand-in for a slow server because a sleeping thread does not need the pen. `wait` sleeps for one second. First we call it four times one after another; then we start four threads that each call `wait`, so the four waits happen together. Guess the output.

```python
import threading
import time


def wait():
    time.sleep(1)


start = time.perf_counter()
for _ in range(4):
    wait()
print(f"one by one:   {time.perf_counter() - start:.2f} s")

start = time.perf_counter()
workers = [threading.Thread(target=wait) for _ in range(4)]
for w in workers:
    w.start()
for w in workers:
    w.join()
print(f"four threads: {time.perf_counter() - start:.2f} s")
```

```bash
python io_bound.py
```

```
one by one:   4.02 s
four threads: 1.01 s
```

Four seconds, then one second. Four threads waiting together took only as long as the longest single wait. Here the threads helped a lot, on normal Python, with the pen still there: a thread that waits puts the pen down (when it sleeps, or waits for the network or a file), and another thread picks it up. That is why a web server can use threads even on normal Python: most of its time goes to waiting for databases and payments. In one line: CPU-bound work, like counting: threads do not help on normal Python. I/O-bound work, like waiting: threads help a lot.

### 6. Free-threaded Python: no pen

For many years the answer to a slow counting job was "not with threads". Then Python 3.13 added an option and 3.14 made it official: a Python built without the pen, called **free-threaded** Python. It is a second build of Python, chosen on purpose. The Python you installed in module 1 is not it. "Official" means the Python docs support it, not that it replaced the normal one.

You can get it with `uv` (module 7, lesson 3). The letter `t` means free-threaded. The download is about 25 MB (the exact version and time will differ):

```bash
uv python install 3.14t
```

```
Downloading cpython-3.14.10+freethreaded-macos-aarch64-none (download) (25.2MiB)
 Downloaded cpython-3.14.10+freethreaded-macos-aarch64-none (download)
Installed Python 3.14.10 in 2.95s
 + cpython-3.14.10+freethreaded-macos-aarch64-none (python3.14t)
```

How do we tell the two apart? One way is `python -VV`, which prints the version with more detail. The free-threaded one adds the words `free-threading build`:

```bash
python -VV
```

```
Python 3.14.7 (main, Aug  5 2026, 10:29:49) [Clang 21.0.0 (clang-2100.1.1.101)]
```

```bash
uv run --python 3.14t python -VV
```

```
Python 3.14.10 free-threading build (main, Oct 26 2026, 13:59:22) [Clang 23.1.3 ]
```

The second way is from inside a program. We run `which_gil.py` on both. Normal Python: GIL on `True`, built without it `False`. Free-threaded: GIL on `False`, built without it `True`. The switch interval is still there, but nobody uses it.

```bash
uv run --python 3.14t which_gil.py
```

```
GIL on: False
built without GIL: True
switch interval: 0.005
```

Now Asha's counting file again, with two extra lines: `import sys` at the top and a line that prints whether the pen is on. On normal Python it is the result you know:

```python
import sys
import threading
import time


def count(n):
    while n > 0:
        n -= 1


def run(threads, n):
    start = time.perf_counter()
    workers = [threading.Thread(target=count, args=(n,))
               for _ in range(threads)]
    for w in workers:
        w.start()
    for w in workers:
        w.join()
    return time.perf_counter() - start


print("GIL on:", sys._is_gil_enabled())
print(f"one thread:   {run(1, 300_000_000):.2f} s")
print(f"four threads: {run(4, 75_000_000):.2f} s")
```

```bash
python cpu_bound.py
```

```
GIL on: True
one thread:   2.68 s
four threads: 2.68 s
```

Same file, same computer, but with the free-threaded Python. Guess: is the GIL on? And what about the four threads line?

```bash
uv run --python 3.14t cpu_bound.py
```

```
GIL on: False
one thread:   2.80 s
four threads: 1.18 s
```

`GIL on: False`, and the four threads are much faster than one thread: for the first time four threads really counted at the same moment. Not four times faster, and that is honest: other programs run too, and on many computers some cores are slower, power-saving ones. Your numbers will differ. The direction is the point. How does it stay safe without the pen? It guards each piece of data in smaller, cleverer ways, so the guarding is spread out instead of one lock for everything. That took years of work, and it is why this build is a separate choice.

### 7. The three catches

**Catch 1: single-thread speed.** The free-threaded build does extra work to stay safe, so ordinary code can run a little slower. The Python 3.14 notes say roughly 5 to 10 percent, depending on the machine. Compare the one-thread lines above: the free-threaded one thread is usually a little slower than normal Python.

**Catch 2: libraries.** Many Python libraries contain C code, and each one must be updated to work without the pen. If you import one that is not marked as ready, Python switches the GIL back on and prints a warning. So always check `sys._is_gil_enabled()` after your imports. You can also switch it back on yourself with the environment variable `PYTHON_GIL=1` in front of the command. Same file, same free-threaded Python, but now the pen is on and the four threads take as long as one:

```bash
PYTHON_GIL=1 uv run --python 3.14t cpu_bound.py
```

```
GIL on: True
one thread:   2.81 s
four threads: 2.81 s
```

**Catch 3, the most important: your own code.** This file adds 1 to a global total a million times in each of four threads. The right answer is 4,000,000. Guess the answer on normal Python, and then on free-threaded Python.

```python
import threading

total = 0


def add_many():
    global total
    for _ in range(1_000_000):
        total += 1


workers = [threading.Thread(target=add_many) for _ in range(4)]
for w in workers:
    w.start()
for w in workers:
    w.join()
print("expected 4000000, got", total)
```

```bash
python lost_updates.py
```

```
expected 4000000, got 4000000
```

```bash
uv run --python 3.14t lost_updates.py
```

```
expected 4000000, got 1155108
```

On free-threaded Python many additions were lost (the total is different on every run; yours will differ). Just like the two threads and the reference count. `total += 1` is really three small steps: read the number, add one, write it back. With real parallel threads two of them read the same number and one addition vanishes. The pen had been hiding the bug.

Be careful with that claim: the same code can lose additions on normal Python too. The pen is only passed at certain moments, so it rarely shows. The pen protects the inner workings of Python, like reference counts. It never protected your logic. The fix is a lock of your own, and that is module 12, lesson 2. For today: free-threaded Python does not make unsafe code safe, it only stops hiding it.

So which Python should you use? Honest advice: the normal one for almost everything. Every library works, and it is the default. Consider free-threaded when you have heavy CPU work that threads can split, your libraries support it, and you have measured the gain.

### 8. Pitfall: timing threads without `join`

Pitfall 5 in the video: delete the two `join` lines and run again. The clock stops the moment the threads start, not when they finish.

```python
import threading
import time


def count(n):
    while n > 0:
        n -= 1


def run(threads, n):
    start = time.perf_counter()
    workers = [threading.Thread(target=count, args=(n,))
               for _ in range(threads)]
    for w in workers:
        w.start()
    return time.perf_counter() - start


print(f"one thread:   {run(1, 300_000_000):.2f} s")
print(f"four threads: {run(4, 75_000_000):.2f} s")
```

```bash
python no_join.py
```

```
one thread:   0.01 s
four threads: 0.10 s
```

Four threads in a tiny fraction of the time: impossible, of course. The workers were still counting when we printed. `join` waits for them, so always join before you stop the clock.

## Common mistakes

1. Expecting threads to speed up CPU work on normal Python. Measure first; use processes (module 12) or free-threaded Python.

2. Believing the GIL makes your code thread-safe. It protects Python's inner workings, not your logic: shared data that changes needs a lock of your own.

3. Thinking free-threaded Python is simply faster: one thread can be slower, and it helps only when several threads share heavy CPU work.

4. Not knowing which Python is running. Check `sys._is_gil_enabled()` or `python -VV` instead of guessing.

5. Timing threads without `join`: the clock stops before the work does.

## Clean up

The free-threaded Python installed by `uv python install 3.14t` stays on your computer. Remove it with `uv python uninstall 3.14t` if you do not need it.

## Next

Next lesson: [M11-L04 · Measuring and Improving Speed](../m11-l04-measuring-and-improving-speed/README.md). Today we used a stopwatch. Next we find out where the time really goes, and when it does not matter at all.
