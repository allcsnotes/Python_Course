# M12-L05 · Async in Practice

> Video: Module 12, Lesson 5. Watch it first, then follow along here.

## What you'll learn

- Why `async def` plus `gather` was not faster (a plain `httpx.get` blocks the loop) and how the async client fixes it
- `async with`: what `__aenter__` and `__aexit__` are, and why one client serves the whole program
- Handling errors per job, limiting the crowd with an `asyncio.Semaphore`
- Cancelling tasks: `task.cancel()`, `CancelledError`, `asyncio.timeout` as a cancel with a promise, and never swallowing a cancel
- Finding and fixing blocking calls: debug mode, a heartbeat, `asyncio.to_thread`

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- A virtual environment with `httpx` (pinned in `requirements.txt`): `python -m venv .venv`, activate it, `pip install -r requirements.txt`. No Docker needed.
- [M12-L04 · asyncio from Scratch](../m12-l04-asyncio-from-scratch/README.md).
- Start the practice service first, in its own terminal window (`python service.py`, it listens on port 8125 and allows at most 20 requests at the same time). It makes no real internet calls. **Timings depend on your computer**: the seconds below are from one real run (the waits are half-second sleeps, so they should be close to yours); the busy counts depend on timing and can differ by a few.

## Files in this folder

| File | What it is |
|------|------------|
| `service.py` | The practice service on localhost:8125: pages wait half a second, `/slow` waits five, at most 20 at once, otherwise `503 busy` |
| `requirements.txt` | `httpx==0.28.1` |
| `hook_sync.py` | The hook: twenty pages, one by one, with the plain client |
| `hook_async_bad.py` | `async def` and `gather`, but nothing gets faster |
| `one_request.py` | One request with the async client |
| `async_door.py` | The smallest `async with`: `__aenter__` and `__aexit__` |
| `many.py` | Twenty pages with the async client |
| `errors.py` | Every job catches its own network errors |
| `flood.py` | A hundred requests at once: 80 are turned away |
| `limited.py` | The same with a semaphore of ten |
| `cancel_task.py` | Cancel a slow request after one second |
| `cancel_timeout.py` | `asyncio.timeout` is a cancel with a promise |
| `swallow.py` | Pitfall: a bare `except` swallows the cancel |
| `beat.py` | A heartbeat that reports the worst gap between beats |
| `block_sleep.py` | A blocking `time.sleep` freezes the loop |
| `block_debug.py` | Debug mode names the guilty task |
| `block_thread.py` | Fix: `asyncio.to_thread(time.sleep, 2)` |
| `to_thread_pages.py` | The hook rescued with `to_thread` |
| `block_cpu.py` | Counting also blocks the loop |
| `block_cpu_thread.py` | Counting moved to a thread |
| `closed.py` | Pitfall: using the client after its block ended |

## Follow along

### 1. Set up, and the hook: async, and no faster

Create and activate a virtual environment and install `httpx` (module 7):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the practice service in its own terminal window and leave it running (stop it with Control-C at the end). Run the other commands in a second terminal, in the same folder, with the same environment:

```bash
python service.py
```

Asha's site has twenty course pages to check. They come from Priya's practice service, like the one in module 7, lesson 4, and it runs on this computer, so every number today is real. Each page takes half a second to answer. First, the plain way: a loop over the twenty pages and one `get` request for each, with a client from HTTPX. Twenty waits of half a second, one after another.

```python
import time

import httpx

URL = "http://localhost:8125/page/{}"

start = time.perf_counter()
with httpx.Client() as client:
    for n in range(1, 21):
        client.get(URL.format(n))
seconds = time.perf_counter() - start
print(f"20 pages, one by one: {seconds:.1f} seconds")
```

```bash
python hook_sync.py
```

```
20 pages, one by one: 10.2 seconds
```

About ten seconds: no surprise. Asha has just finished the asyncio lesson, so she changes the function to `async def` and asks for all twenty pages together with `gather`, exactly as you learned. The request line inside `fetch` stays as it is.

```python
import asyncio
import time

import httpx

URL = "http://localhost:8125/page/{}"


async def fetch(n):
    return httpx.get(URL.format(n))


async def main():
    start = time.perf_counter()
    await asyncio.gather(*(fetch(n) for n in range(1, 21)))
    seconds = time.perf_counter() - start
    print(f"20 pages, async: {seconds:.1f} seconds")


asyncio.run(main())
```

```bash
python hook_async_bad.py
```

```
20 pages, async: 10.2 seconds
```

About ten seconds. The same as one by one! She wrote `async def`, she wrote `gather`, and nothing got faster. Why? By the end of this lesson you will know exactly what is wrong and how to fix it.

### 2. Four needs, four tools

Remember the cook from the last lesson: one cook, many pots, who turns away from a pot whenever it only needs to wait. Today the pots are real: each pot is a request to a server, and the waiting is the server thinking. Real work brings four new needs. One: a way to talk to a server that lets the cook turn away. Two: a limit, because a stove has only so many burners. Three: a way to take a pot off the stove when nobody wants it any more. Four: a way to deal with a job that makes the cook stare at one pot and not turn away. Each need has a tool: the **async client from HTTPX**, a **semaphore**, **cancel**, and for the staring cook, a **thread**. We take them in this order, and the last one answers the mystery of the hook.

### 3. The async client and `async with`

HTTPX (the package you added with `uv` in module 7) has two kinds of client: the plain client, which waits for each answer (the hook), and the **async client**, whose requests can be awaited. Here is one request. The address has a hole for the page number. `main` is an `async def`. Inside it: `async with httpx.AsyncClient() as client:`, then `response = await client.get(...)`.

```python
import asyncio

import httpx

URL = "http://localhost:8125/page/{}"


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get(URL.format(1))
    print(response.status_code, response.json())


asyncio.run(main())
```

```bash
python one_request.py
```

```
200 {'page': '1', 'title': 'Course 1'}
```

200, and the data of page 1, the same response object as in module 7. Two things are new: the word `await` in front of `get`, and the words `async with`. `await` you know: the request is waiting, so the cook may turn away. `async with` is new, and the last lesson promised it.

Remember the `with` statement from module 9, lesson 4: it sets something up when the block starts and cleans up when it ends, by calling `__enter__` and `__exit__`. But getting a connection ready and closing it politely both mean waiting for the other side. So Python has a second kind of `with`: `async with`. It calls `__aenter__` and `__aexit__`: the same two jobs, but each is a coroutine, so it can `await` and the cook is free while it waits. The smallest one, a door: `__aenter__` prints `opening the door`, waits half a second and returns the key. `__aexit__` waits half a second and prints `closing the door`.

```python
import asyncio


class Door:
    async def __aenter__(self):
        print("enter: opening the door")
        await asyncio.sleep(0.5)
        return "the key"

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(0.5)
        print("exit: closing the door")


async def main():
    async with Door() as key:
        print("inside the block, with", key)
    print("after the block")


asyncio.run(main())
```

```bash
python async_door.py
```

```
enter: opening the door
inside the block, with the key
exit: closing the door
after the block
```

Enter, inside the block with the key, exit, after the block: the same order as the plain `with`. The difference is the two half seconds: while the door was opening and closing, the cook was free to run other jobs. For HTTPX it works the same way: entering gets the client ready, exiting closes its connections, and that may take a moment. The name `client` only belongs inside the block. Why one client for the whole program and not a new one for every request? The client keeps its connections open and reuses them, like staying on the phone line instead of dialling again for every question. You have now met `async with` several times: the task group, the timeout, and now the client. Whenever something must be set up and cleaned up, and the setting up or the cleaning up may wait, use `async with`.

### 4. Twenty pages, done properly

`fetch` takes the client and a page number and awaits `client.get`. It returns the title from the JSON. `main` opens one async client, builds a list of twenty `fetch` calls and `gather`s them. The hook took about ten seconds; the same twenty pages, half a second each, all together this time. Guess the time.

```python
import asyncio
import time

import httpx

URL = "http://localhost:8125/page/{}"


async def fetch(client, n):
    response = await client.get(URL.format(n))
    return response.json()["title"]


async def main():
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        jobs = [fetch(client, n) for n in range(1, 21)]
        titles = await asyncio.gather(*jobs)
    seconds = time.perf_counter() - start
    print(titles[:3], "...")
    print(f"20 pages, async: {seconds:.1f} seconds")


asyncio.run(main())
```

```bash
python many.py
```

```
['Course 1', 'Course 2', 'Course 3'] ...
20 pages, async: 0.6 seconds
```

The first titles, and about half a second: twenty pages in about the time of one, roughly twenty times faster than the hook, with one thread and one client. What changed from the hook? The `get` is now `await client.get`: the cook can turn away while the answer travels. You will see exactly what the plain `get` did wrong in a few minutes.

Real pages also fail. From module 7, lesson 4 you know the three ways: the service says no with an error code, it answers too slowly, or it is down. HTTPX gives each its own error. So each job should catch its own trouble and return a sentence about what happened. `check` takes the client and a path: inside `try`, `get`, then `raise_for_status`, then `except httpx.HTTPError`. `main` checks four paths: page 1, a page that is missing, the slow page that waits five seconds, and page 2. The client gets `timeout=2`: no request waits longer than two seconds. Guess the output.

```python
import asyncio
import time

import httpx

BASE = "http://localhost:8125"


async def check(client, path):
    try:
        response = await client.get(BASE + path)
        response.raise_for_status()
    except httpx.HTTPError as error:
        return f"{path}: failed ({type(error).__name__})"
    return f"{path}: ok"


async def main():
    paths = ["/page/1", "/missing", "/slow", "/page/2"]
    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=2) as client:
        jobs = [check(client, p) for p in paths]
        results = await asyncio.gather(*jobs)
    print("\n".join(results))
    print(f"{time.perf_counter() - start:.1f} seconds")


asyncio.run(main())
```

```bash
python errors.py
```

```
/page/1: ok
/missing: failed (HTTPStatusError)
/slow: failed (ReadTimeout)
/page/2: ok
2.1 seconds
```

Page 1 ok, missing failed (HTTP status error, the 404), slow failed (read timeout), page 2 ok. And about two seconds: the slow page was cut at two seconds, not five. That is the habit for many requests: every job catches its own network errors and returns an answer that says what happened. The list keeps the order of the paths.

### 5. A flood, and the semaphore

Twenty pages were easy. What about a hundred? Starting them all in the same moment is a flood. Priya's service says: I can answer twenty at a time; for anything more, I reply `503 busy`. Here is the hundred, all at once. `fetch` returns only the status code; `main` gathers a hundred jobs and counts how many answers were 200 and how many were 503. Guess the two numbers.

```python
import asyncio

import httpx

URL = "http://localhost:8125/page/{}"


async def fetch(client, n):
    response = await client.get(URL.format(n))
    return response.status_code


async def main():
    async with httpx.AsyncClient() as client:
        jobs = [fetch(client, n) for n in range(1, 101)]
        codes = await asyncio.gather(*jobs)
    print(codes.count(200), "ok,", codes.count(503), "busy")


asyncio.run(main())
```

```bash
python flood.py
```

```
19 ok, 81 busy
```

```bash
curl http://localhost:8125/stats
```

```
{"now": 1, "peak": 20, "busy": 81}
```

About 20 ok and about 80 busy (the exact split depends on timing; 19 and 81 in one run). The service's own counter agrees: at most twenty at once, and about eighty turned away. Eighty pages are missing from Asha's report and the program did not even crash. A flood fails quietly. We need a limit: at most so many requests in flight, and the rest wait their turn. The tool is a **semaphore**. Picture a stove with ten burners: a pot can start only when a burner is free; when it finishes, the burner goes to the next pot waiting. In code, a semaphore is a counter of free places: `asyncio.Semaphore(10)`. A job asks for a place with `async with sem:`. If a place is free, it takes it and goes on. If not, the job pauses (the cook is free) until a place opens up. Three small changes: `main` makes the semaphore with ten places and passes it to every job, and `fetch` wraps only the `get` in `async with sem`. Guess: how many ok, how many busy, and how long?

```python
import asyncio
import time

import httpx

URL = "http://localhost:8125/page/{}"


async def fetch(client, sem, n):
    async with sem:
        response = await client.get(URL.format(n))
    return response.status_code


async def main():
    sem = asyncio.Semaphore(10)
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        jobs = [fetch(client, sem, n) for n in range(1, 101)]
        codes = await asyncio.gather(*jobs)
    print(codes.count(200), "ok,", codes.count(503), "busy")
    print(f"{time.perf_counter() - start:.1f} seconds")


asyncio.run(main())
```

```bash
python limited.py
```

```
100 ok, 0 busy
5.1 seconds
```

```bash
curl http://localhost:8125/stats
```

```
{"now": 0, "peak": 11, "busy": 0}
```

100 ok, 0 busy, about five seconds. A hundred pages in ten rounds of ten, half a second each; the service's counter says the peak was about ten. Slower than the flood, but every page arrived. What number should you choose? Start from what the service allows (here twenty, so ten leaves room for others). For an ordinary web site, ten to fifty is a common start. Then measure: a bigger number is faster until the other side starts saying no. Two details: create the semaphore once, inside `main`, and share it with all the jobs; and wrap only the request, not the whole job, so the places are held for as short a time as possible.

### 6. Cancel

A cook sometimes takes a pot off the stove: the guest left, or the pot is taking far too long. In asyncio that is **cancel**. Every task has a method called `cancel`. Here the task is a request for the slow page (five seconds). `main` waits one second and then calls `task.cancel()`. Then it awaits the task inside `try` and catches `asyncio.CancelledError`.

```python
import asyncio
import time

import httpx

SLOW = "http://localhost:8125/slow"


async def main():
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        task = asyncio.create_task(client.get(SLOW))
        await asyncio.sleep(1)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("cancelled:", task.cancelled())
    print(f"stopped after {time.perf_counter() - start:.1f} seconds")


asyncio.run(main())
```

```bash
python cancel_task.py
```

```
cancelled: True
stopped after 1.0 seconds
```

`cancelled: True`, and stopped after about one second, not five. The request was dropped in the middle of waiting. How does cancel work? It does not kill the task. It leaves a message: at the task's next turn, raise `CancelledError` right at the `await` where the task was paused, as if the `await` itself had failed. Because cancel is just an error travelling upward, a `finally` block still runs. That is the place to close a file, put something back or tell somebody. Now we can finally explain the timeout from the last lesson:

```python
import asyncio

import httpx

SLOW = "http://localhost:8125/slow"


async def download(client):
    try:
        await client.get(SLOW)
    finally:
        print("download: cleaning up")


async def main():
    async with httpx.AsyncClient() as client:
        try:
            async with asyncio.timeout(1):
                await download(client)
        except TimeoutError:
            print("main: too slow, gave up")


asyncio.run(main())
```

```bash
python cancel_timeout.py
```

```
download: cleaning up
main: too slow, gave up
```

`download: cleaning up`, then `main: too slow, gave up`. A timeout is a cancel with a promise: after one second it cancels the work inside the block, the cleanup runs, and then the `CancelledError` is turned into a `TimeoutError` that you can catch.

One special thing. `CancelledError` is not an ordinary exception: it does not come under the class `Exception`, so a normal `except Exception` does not catch it. That is on purpose: a cancel is a request to stop, not a failure. But a bare `except` catches everything, even a cancel. Here is a worker doing five steps of 0.4 seconds. `main` waits half a second and cancels. The worker has a bare `except` around its step.

```python
import asyncio


async def worker():
    for step in range(1, 6):
        try:
            await asyncio.sleep(0.4)
            print("step", step)
        except:
            print("ignored the cancel")


async def main():
    task = asyncio.create_task(worker())
    await asyncio.sleep(0.5)
    task.cancel()
    await task
    print("cancelled?", task.cancelled())


asyncio.run(main())
```

```bash
python swallow.py
```

```
step 1
ignored the cancel
step 3
step 4
step 5
cancelled? False
```

Step 1, then `ignored the cancel`, then steps 3, 4, 5, and `cancelled? False`. The bare `except` caught the cancel and threw it away, so the worker carried on to the end. The task could not be stopped. The rule: **never swallow a cancel**. Catch only the errors you expect, like `httpx.HTTPError`. And if you ever do catch `CancelledError` to clean up, raise it again when you are done.

### 7. The mystery of the hook: blocking calls

Why did Asha's async version take ten seconds? It is the same trap as `time.sleep` in the last lesson, only better hidden. Remember the rule: the cook can only turn away at an `await`. `httpx.get` is a plain call that waits for the answer without an `await`, so while it waits, the cook stares at one pot and no other job gets a turn. A call that holds the cook is called a **blocking call**. Plain `sleep` is one. A plain request is one. So are reading a big file, a database library that is not async, and a long counting loop. While any of them runs, every other job is frozen.

A small helper in its own file, `beat.py`: `heartbeat`. Every tenth of a second it wakes up and notes the clock. It remembers the worst gap between two beats. In a healthy program the gap stays near a tenth of a second.

```python
import asyncio
import time


async def heartbeat():
    last = time.perf_counter()
    worst = 0
    for _ in range(30):
        await asyncio.sleep(0.1)
        now = time.perf_counter()
        worst = max(worst, now - last)
        last = now
    print(f"worst gap between beats: {worst:.1f} seconds")
```

The blocker is a second job: it waits one second politely and then calls the plain `time.sleep(2)`. `main` runs both with `gather`. Guess the worst gap between beats.

```python
import asyncio
import time

from beat import heartbeat


async def blocker():
    await asyncio.sleep(1)
    time.sleep(2)


async def main():
    await asyncio.gather(heartbeat(), blocker())


asyncio.run(main())
```

```bash
python block_sleep.py
```

```
worst gap between beats: 2.1 seconds
```

About 2.1 seconds. The heart did not beat for two seconds. Nothing else could run: no request, no timer, nothing. On a real server every visitor would be stuck for those two seconds.

How do you find the guilty line in a big program? asyncio can tell you. Run it with `debug=True`. Now whenever one step of the loop takes longer than a tenth of a second, asyncio prints a warning:

```python
import asyncio
import time

from beat import heartbeat


async def blocker():
    await asyncio.sleep(1)
    time.sleep(2)


async def main():
    await asyncio.gather(heartbeat(), blocker())


asyncio.run(main(), debug=True)
```

```bash
python block_debug.py
```

```
Executing <Task finished name='Task-3' coro=<blocker() done, defined at block_debug.py:7> result=None created at /usr/lib/python3.14/asyncio/tasks.py:735> took 2.005 seconds
worst gap between beats: 2.1 seconds
```

There it is: `Executing <Task ... name='...blocker...'> took 2.00x seconds`. It names the task and how long it held the loop. In a real program the name leads you to the line.

Two ways to fix it. **Fix one: use the async version.** For web requests that is the async client you have been using; many libraries have an async twin, so look in their documentation first. **Fix two, when no async version exists: move the call to a thread.** `asyncio.to_thread` takes a plain function and its arguments and runs it in a worker thread, like the ones from lesson 2. You `await` it, so the cook stays free:

```python
import asyncio
import time

from beat import heartbeat


async def blocker():
    await asyncio.sleep(1)
    await asyncio.to_thread(time.sleep, 2)


async def main():
    await asyncio.gather(heartbeat(), blocker())


asyncio.run(main())
```

```bash
python block_thread.py
```

```
worst gap between beats: 0.1 seconds
```

About 0.1 seconds: a tenth, the healthy number. The sleep happens in a thread and the cook never stopped. The same trick rescues the hook: `fetch` becomes `await asyncio.to_thread(httpx.get, url)`.

```python
import asyncio
import time

import httpx

URL = "http://localhost:8125/page/{}"


async def fetch(n):
    return await asyncio.to_thread(httpx.get, URL.format(n))


async def main():
    start = time.perf_counter()
    await asyncio.gather(*(fetch(n) for n in range(1, 21)))
    seconds = time.perf_counter() - start
    print(f"20 pages, threads: {seconds:.1f} seconds")


asyncio.run(main())
```

```bash
python to_thread_pages.py
```

```
20 pages, threads: 1.0 seconds
```

Twenty pages in about a second: far better than ten, but a bit slower than the async client, because each plain call needs its own thread. Prefer the async client; use `to_thread` when there is no async version.

Counting is blocking too, because counting never says `await`. `crunch` adds up thirty million squares. The blocker waits one second and then calls `crunch`. Guess the worst gap.

```python
import asyncio

from beat import heartbeat


def crunch():
    return sum(i * i for i in range(30_000_000))


async def blocker():
    await asyncio.sleep(1)
    crunch()


async def main():
    await asyncio.gather(heartbeat(), blocker())


asyncio.run(main())
```

```bash
python block_cpu.py
```

```
worst gap between beats: 1.1 seconds
```

More than a second of frozen loop. And with `await asyncio.to_thread(crunch)`:

```python
import asyncio

from beat import heartbeat


def crunch():
    return sum(i * i for i in range(30_000_000))


async def blocker():
    await asyncio.sleep(1)
    await asyncio.to_thread(crunch)


async def main():
    await asyncio.gather(heartbeat(), blocker())


asyncio.run(main())
```

```bash
python block_cpu_thread.py
```

```
worst gap between beats: 0.1 seconds
```

The worst gap is back near 0.1: the heartbeat is smooth again. But be careful: the thread did not make the counting faster. It only freed the cook. On normal Python, threads still share one pen (module 11, lesson 3). To make heavy counting itself faster, use a process (lesson 3). The rule of thumb: inside `async def`, every wait is an `await`. A call that cannot be awaited goes to a thread. Heavy counting goes to a process. And when in doubt, run with debug mode or a heartbeat and measure.

### 8. Pitfalls

**1. Using the client after its block has ended.** This `main` opens the async client and passes straight out of the block, then calls `get`. (The long middle of the traceback is inside HTTPX and is trimmed here.)

```python
import asyncio

import httpx

URL = "http://localhost:8125/page/1"


async def main():
    async with httpx.AsyncClient() as client:
        pass
    await client.get(URL)


asyncio.run(main())
```

```python
import asyncio

import httpx

URL = "http://localhost:8125/page/1"


async def main():
    async with httpx.AsyncClient() as client:
        pass
    await client.get(URL)


asyncio.run(main())
```

```bash
python closed.py
```

```
Traceback (most recent call last):
  File "closed.py", line 3, in <module>
  ...
```

`RuntimeError: Cannot send a request, as the client has been closed.` Leaving the `async with` block closed the client. Do every request inside the block.

**2. No limit.** A hundred requests at once gave eighty busy answers. For many requests always limit with a semaphore, at a number the service can take.

**3. Swallowing the cancel.** A bare `except` kept the worker running to the end. Catch only the errors you expect and raise `CancelledError` again if you catch it.

**4. A blocking call inside `async def`.** The hook took ten seconds for twenty half-second pages. Look for a missing `await`, measure with a heartbeat, and let debug mode name the task.

## Common mistakes

1. Using `httpx.get` (or any plain call that waits) inside `async def`: it blocks the whole loop. Use the async client, or `asyncio.to_thread`.

2. Using the client after its `async with` block ended.

3. Starting hundreds of requests with no limit: the other side says busy and your report silently misses pages. Use a `Semaphore`.

4. Swallowing `CancelledError` with a bare `except` (or not re-raising it).

5. Wrapping a whole job (not only the request) in the semaphore.

6. Believing `to_thread` makes counting faster. It only frees the loop; heavy counting needs processes.

## Clean up

Stop the practice service with Control-C in its terminal window, and delete the `.venv` folder you made (`rm -rf .venv`) if you do not need it any more.

## Next

Next: the build video, [M12-B06 · Build a Concurrent Link Checker](../m12-b06-build-a-concurrent-link-checker/README.md). You will build one checker three ways (one by one, with threads, and with asyncio) and put the three timings side by side.

Your turn first: run the hundred pages with a semaphore of five and of twenty and compare the times; cancel a request after two seconds; move a plain sleep into a thread; and turn on debug mode and read its warning.
