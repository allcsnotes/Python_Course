# M12-B06 · Build a Concurrent Link Checker

> Video: Module 12, Build 6. Watch it first, then follow along here.

## What you'll learn

- How to plan a tool: four requirements, and five things that can happen to a link (ok, moved, broken, timeout, down)
- How to build the same checker three ways with one shared `core.py`: one at a time, with a thread pool, and with asyncio and a semaphore
- How to turn every network error into a result, so one bad link cannot stop the others
- How to make a command-line tool (`linkcheck.py async 8`) that writes `report.json` and returns an exit code
- How the number of workers changes the time (and why a run is never shorter than its slowest link)
- What breaks: too many at once, an uncaught error, a blocking call inside async code

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- A virtual environment with `httpx` (pinned in `requirements.txt`). No Docker needed.
- The rest of module 12, especially [M12-L05 · Async in Practice](../m12-l05-async-in-practice/README.md), and the retry decorator from [M09-B05](../../m09-writing-pythonic-code/m09-b05-build-a-decorator-toolkit/README.md) for one of the upgrades.
- The checker never touches the real internet. `server.py` is a small test server on this computer (port 8626) with the 24 links of `links.txt`: twelve course pages (0.2 s each), four video pages (1 s each), three old addresses that redirect to a course page, two pages that are gone (404), one API that fails (500), one page that hangs for 5 seconds (it will time out at 2 s), and one link to a port where nothing listens (down). It answers `503 too busy` when more than 16 requests arrive at once.
- **Timings depend on your computer.** The seconds below are from one real run (the waits are sleeps, so they should be close to yours). Everything else (the counts, the kinds) will be the same.

## Files in this folder

| File | What it is |
|------|------------|
| `server.py` | The test server on port 8626 |
| `requirements.txt` | `httpx==0.28.1` |
| `links.txt` | The 24 links, one per line |
| `core.py` | Shared pieces: `LINKS`, `OPTIONS`, `Result`, `from_response`, `from_error`, `report` |
| `try1.py` | Checks three links by hand to test the pieces |
| `seq.py` | Step 2: one at a time |
| `threaded.py` | Step 3: a thread pool |
| `aio.py` | Step 4: asyncio with a semaphore |
| `linkcheck.py` | Step 5: the command-line tool |
| `sweep.py` | Times threads and async with 1, 2, 4, 8 and 12 workers |
| `nocatch.py` | Breaks 2: a version of `check` without `try` |
| `blocking.py` | Breaks 3: an async version with a blocking call |

## Run it

Create and activate a virtual environment and install `httpx` (module 7). Then start the test server in its own terminal window (leave it running; stop it with Control-C at the end), and run the checker from a second terminal in the same folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
python server.py
```

```bash
python linkcheck.py async 8
echo $?
```

The checker visits the same 24 links one at a time (`seq`), with eight threads (`threads 8`) or with eight async tasks (`async 8`), prints only the links with a problem, and ends with exit code 1 when there are problems (0 when all is well). The full expected output is in the sections below.

## Build it step by step

### What we build

Asha's allcsvideos.com has a page for every course, and every page is full of links: to other courses, to videos, to old addresses. One day Lukas writes to her: the link to the regex course is dead. How many more are dead? Nobody knows. So Asha builds a **link checker**: a program that visits every link and reports the ones with a problem. To stay safe we do not touch the real internet: `server.py` is a small test server on this computer. Start it in its own terminal window and leave it running:

```bash
python server.py
```

This is the finished checker run three ways on the same 24 links: one at a time, then with eight threads, then with eight async tasks. We keep only the last two lines of each report. Guess the three times.

```bash
python linkcheck.py seq | tail -2
```

```
24 links checked in 9.1 s
16 ok, 3 moved, 3 broken, 1 timeout, 1 down
```

```bash
python linkcheck.py threads 8 | tail -2
```

```
24 links checked in 2.2 s
16 ok, 3 moved, 3 broken, 1 timeout, 1 down
```

```bash
python linkcheck.py async 8 | tail -2
```

```
24 links checked in 2.3 s
16 ok, 3 moved, 3 broken, 1 timeout, 1 down
```

About nine seconds one at a time, about two seconds with eight threads, about two seconds with eight async tasks. And the answer is the same every time: 16 ok, 3 moved, 3 broken, 1 timeout, 1 down. How can that be? Most of the time the checker is not computing: it is waiting for servers. That is I/O-bound work (lesson 1). While one link waits, the next ones can be asked. Today we build all three versions, step by step.

### Plan on paper

Four requirements. One: visit every link and say what happened. Two: one bad link must never stop the others. Three: ask many links at the same time, but never too many. Four: print a short report for people and a file for machines.

What can happen to a link? Five things. **ok**: the page answered, all is well. **moved**: the address was old and the server pointed to a new one (a *redirect*), and we follow it. **broken**: the server answered, but with an error (404, 500, and so on). **timeout**: the server did not answer in time (we wait at most 2 seconds). **down**: nobody is there at all (the connection was refused).

The 24 links of `links.txt` (the first few lines are shown; `server.py` makes each kind behave as described in *Before you start*):

```
http://localhost:8626/course/python-basics
http://localhost:8626/video/intro
http://localhost:8626/course/functions
http://localhost:8626/old/classes
http://localhost:8626/course/files
http://localhost:8626/gone/regex-course
http://localhost:8626/course/errors
http://localhost:8626/video/threads
http://localhost:8626/course/modules
http://localhost:8626/api/payments
http://localhost:8626/course/testing
http://localhost:8626/old/git
http://localhost:8626/course/docker
http://localhost:8626/hang/report
http://localhost:8626/course/sql
http://localhost:8626/video/asyncio
http://localhost:8626/course/apis
http://localhost:8626/old/sql
http://localhost:8626/course/async
http://localhost:8626/gone/rust-course
http://localhost:8626/course/packaging
http://localhost:8626/video/pytest
http://localhost:8626/course/typing
http://localhost:8627/up
```

The code goes in five files. `core.py` holds the shared pieces: the list of links, the result of one check and the report. Then one file for each way of working: `seq.py` (one at a time), `threaded.py` (threads), `aio.py` (async). Finally `linkcheck.py`, the tool that picks the way from the command line. The package is `httpx`, the one you met in module 7, lesson 4.

### Step 1: `core.py`

Start at the top. `Path("links.txt").read_text().split()` reads the file (module 6) and cuts it at every line break, so `LINKS` is a list of 24 addresses. `OPTIONS` is a dictionary of settings for the client: wait at most 2 seconds, and follow redirects. `BAD` lists the three kinds that mean trouble.

The result of one check is a small dataclass (module 8, lesson 6): the URL, the status number (or `None` when the server never answered), the kind (one of our five words) and the milliseconds the check took. Next come two helpers that build a `Result`. `elapsed` turns a start time into milliseconds, with `perf_counter` (module 5). `from_response` looks at an answer: a status of 400 or more is `broken`; otherwise, if the history says we were redirected, it is `moved`; otherwise `ok`. `from_error` handles the case with no answer at all: a timeout error means `timeout`; any other failure, like a refused connection, is `down`, and the status is `None` because there is none. Finally `report` prints only the links that are not ok (a checker should speak up only when something is wrong) and a summary with a count per kind.

`core.py`:

```python
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import httpx

BASE = "http://localhost:8626"
OPTIONS = {"timeout": 2, "follow_redirects": True}
BAD = ("broken", "timeout", "down")
LINKS = Path("links.txt").read_text().split()


@dataclass
class Result:
    url: str
    status: int | None
    kind: str
    ms: int


def elapsed(start):
    return round((time.perf_counter() - start) * 1000)


def from_response(url, response, start):
    status = response.status_code
    if status >= 400:
        kind = "broken"
    elif response.history:
        kind = "moved"
    else:
        kind = "ok"
    return Result(url, status, kind, elapsed(start))


def from_error(url, error, start):
    if isinstance(error, httpx.TimeoutException):
        kind = "timeout"
    else:
        kind = "down"
    return Result(url, None, kind, elapsed(start))


def report(results, seconds):
    for r in results:
        if r.kind == "ok":
            continue
        code = r.status or "-"
        path = r.url.removeprefix(BASE)
        print(f"{r.kind:<8}{code:>4}{r.ms:>6} ms  {path}")
    counts = Counter(r.kind for r in results)
    parts = ", ".join(f"{n} {k}" for k, n in counts.items())
    print(f"{len(results)} links checked in {seconds:.1f} s")
    print(parts)
```

Test the pieces before building on them. `try1.py` checks three links by hand (a course page, an old address, a missing page) and then a link to a port where nothing listens, inside `try`. For each one it prints the kind, the status and the milliseconds.

```python
import time

import httpx

from core import BASE, OPTIONS, from_error, from_response

client = httpx.Client(**OPTIONS)
for path in ["/course/sql", "/old/sql", "/gone/rust-course"]:
    url = BASE + path
    start = time.perf_counter()
    response = client.get(url)
    result = from_response(url, response, start)
    print(result.kind, result.status, result.ms)

url = "http://localhost:8627/up"
start = time.perf_counter()
try:
    client.get(url)
except httpx.HTTPError as error:
    result = from_error(url, error, start)
    print(result.kind, result.status, result.ms)
```

```bash
python try1.py
```

```
ok 200 204
moved 200 207
broken 404 1
down None 0
```

The course page: `ok`, 200, about 200 ms. The old address: `moved`, with status 200 because it was redirected first. The missing page: `broken`, 404, and almost no time, because the server says no at once. The dead port: `down`, status `None`.

### Step 2: one at a time (`seq.py`)

`check` takes the client and one link. It starts the clock and tries to get the page. If anything goes wrong with the request we catch `httpx.HTTPError`, the parent of the timeout error and the connection errors, and turn it into a result with `from_error`. `run` builds the list: one client is created with the options, in a `with` block (module 9, lesson 4), because a client keeps its settings and reuses its connections. Then a list comprehension calls `check` for every link. At the bottom is the guard from module 7: it starts the clock, runs, and prints the report.

`seq.py`:

```python
import time

import httpx

from core import LINKS, OPTIONS, from_error, from_response, report


def check(client, url):
    start = time.perf_counter()
    try:
        response = client.get(url)
    except httpx.HTTPError as error:
        return from_error(url, error, start)
    return from_response(url, response, start)


def run(links):
    with httpx.Client(**OPTIONS) as client:
        return [check(client, url) for url in links]


if __name__ == "__main__":
    began = time.perf_counter()
    results = run(LINKS)
    report(results, time.perf_counter() - began)
```

Before we run it: twelve course pages at a fifth of a second, four videos at a second each, three moved links, and one link that waits for the whole 2-second timeout, one after another, adds up to about nine seconds.

```bash
python seq.py
```

```
moved    200   206 ms  /old/classes
broken   404     1 ms  /gone/regex-course
broken   500     1 ms  /api/payments
moved    200   207 ms  /old/git
timeout    -  2002 ms  /hang/report
moved    200   204 ms  /old/sql
broken   404     1 ms  /gone/rust-course
down       -     0 ms  http://localhost:8627/up
24 links checked in 9.1 s
16 ok, 3 moved, 3 broken, 1 timeout, 1 down
```

Eight lines of problems, and the summary: 16 ok, 3 moved, 3 broken, 1 timeout, 1 down, in about nine seconds. Look at the timeout line: about 2,000 milliseconds. We waited the whole 2 seconds and gave up. And in those nine seconds the program did nothing except wait. Waiting for a server is I/O-bound work, exactly the kind that threads and async can overlap.

### Step 3: threads (`threaded.py`)

Lesson 2 taught the plan: a pool of workers and `pool.map`. Picture eight helpers standing at a pile of 24 links; each takes the next link, checks it and comes back for another. `threaded.py` imports `check` from `seq.py`: the same function, not one new line of checking. The client is shared by all the threads, and HTTPX promises that this is safe. A small function called `work` remembers the client for each thread. `pool.map` hands the results back in the order of the links, even when the checks finish in another order, and `list` collects them. The `with` block waits for every thread (lesson 2). Do we need a lock? No: each thread builds its own `Result` and nothing shared is changed.

`threaded.py`:

```python
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

from core import LINKS, OPTIONS, report
from seq import check


def run(links, workers=8):
    with httpx.Client(**OPTIONS) as client:

        def work(url):
            return check(client, url)

        with ThreadPoolExecutor(max_workers=workers) as pool:
            return list(pool.map(work, links))


if __name__ == "__main__":
    began = time.perf_counter()
    results = run(LINKS)
    report(results, time.perf_counter() - began)
```

Guess before we run: eight workers. How long will the same 24 links take?

```bash
python threaded.py
```

```
moved    200   209 ms  /old/classes
broken   404     3 ms  /gone/regex-course
broken   500     2 ms  /api/payments
moved    200   204 ms  /old/git
timeout    -  2002 ms  /hang/report
moved    200   207 ms  /old/sql
broken   404     1 ms  /gone/rust-course
down       -     1 ms  http://localhost:8627/up
24 links checked in 2.2 s
16 ok, 3 moved, 3 broken, 1 timeout, 1 down
```

About two seconds, with the same 16, 3, 3, 1, 1. From nine seconds to two. Why not eight times faster? Because the run can never be shorter than its slowest link: the one that waits for the 2-second timeout.

### Step 4: async (`aio.py`)

Remember the cook with many pots from lesson 4: one cook, no helpers; the cook starts one pot, and while it heats, starts the next. Our cook starts all the requests and handles each answer as it arrives. In `aio.py`, `check` is now an `async def`. It takes the client, a limit and the link. `async with limit:` is a semaphore from lesson 5, a counter of free places: only eight tasks can be inside at a time. We start the clock, `await client.get`, and turn answers and errors into results exactly as before. `run_async` makes the limit (a semaphore with `workers` places), then an async client with the same options in an `async with` block. `jobs` is a list of `check` calls; these are coroutines, so nothing has run yet (lesson 4). `await asyncio.gather(*jobs)` runs them and returns the results in order. The last function, `run`, wraps it all in `asyncio.run`, so that `aio.py` offers the same function as the others: links in, results out.

`aio.py`:

```python
import asyncio
import time

import httpx

from core import LINKS, OPTIONS, from_error, from_response, report


async def check(client, limit, url):
    async with limit:
        start = time.perf_counter()
        try:
            response = await client.get(url)
        except httpx.HTTPError as error:
            return from_error(url, error, start)
        return from_response(url, response, start)


async def run_async(links, workers):
    limit = asyncio.Semaphore(workers)
    async with httpx.AsyncClient(**OPTIONS) as client:
        jobs = [check(client, limit, url) for url in links]
        return await asyncio.gather(*jobs)


def run(links, workers=8):
    return asyncio.run(run_async(links, workers))


if __name__ == "__main__":
    began = time.perf_counter()
    results = run(LINKS)
    report(results, time.perf_counter() - began)
```

Guess: eight at a time. Will async beat the threads?

```bash
python aio.py
```

```
moved    200   209 ms  /old/classes
broken   404     5 ms  /gone/regex-course
broken   500     4 ms  /api/payments
moved    200   209 ms  /old/git
timeout    -  2004 ms  /hang/report
moved    200   205 ms  /old/sql
broken   404     1 ms  /gone/rust-course
down       -     1 ms  http://localhost:8627/up
24 links checked in 2.2 s
16 ok, 3 moved, 3 broken, 1 timeout, 1 down
```

About two seconds: the same answers, and a hair slower than the threads, which is just noise. For 24 links async and threads tie. Async pays off when you have thousands of connections, because a task is much lighter than a thread.

### Step 5: the tool (`linkcheck.py`)

`linkcheck.py` picks the way from the command line. `sys.argv` is the list of words typed on the command line: for `linkcheck.py async 8` it holds the file name, then `async`, then `8`. The mode defaults to `async` and the workers to 8. A plain `if` / `elif` / `else` picks the module and calls its `run`; an unknown mode ends the program with `sys.exit` and a message. Then the report. After that, `json.dump` writes all the results into `report.json` for machines. The last two lines are for robots: if any result has a bad kind, `sys.exit(1)`. An exit code of 0 means all is well; anything else means there were problems, and robots that run your code, like a CI system (module 19), read that number.

`linkcheck.py`:

```python
import json
import sys
import time
from dataclasses import asdict

import aio
import seq
import threaded
from core import BAD, LINKS, report


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "async"
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    began = time.perf_counter()
    if mode == "seq":
        results = seq.run(LINKS)
    elif mode == "threads":
        results = threaded.run(LINKS, workers)
    elif mode == "async":
        results = aio.run(LINKS, workers)
    else:
        sys.exit(f"unknown mode: {mode}")
    report(results, time.perf_counter() - began)
    with open("report.json", "w") as file:
        json.dump([asdict(r) for r in results], file, indent=2)
    if any(r.kind in BAD for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
```

Run it: async, eight. Then `echo $?` prints the exit code of the last command, and we look at the first lines of `report.json`:

```bash
python linkcheck.py async 8
echo $?
head -n 8 report.json
```

```
moved    200   211 ms  /old/classes
broken   404     6 ms  /gone/regex-course
broken   500     3 ms  /api/payments
moved    200   208 ms  /old/git
timeout    -  2003 ms  /hang/report
moved    200   205 ms  /old/sql
broken   404     2 ms  /gone/rust-course
down       -     1 ms  http://localhost:8627/up
24 links checked in 2.2 s
16 ok, 3 moved, 3 broken, 1 timeout, 1 down
1
[
  {
    "url": "http://localhost:8626/course/python-basics",
    "status": 200,
    "kind": "ok",
    "ms": 224
  },
  {
```

The same report as before. Then the exit code, 1: problems were found. And `report.json` holds every result, not only the problems.

Now the question from the plan: how many workers? `sweep.py` times threads and async with 1, 2, 4, 8 and 12 workers. Guess the times. (This takes about a minute.)

```python
import time

import aio
import threaded
from core import LINKS

print("workers  threads  async")
for workers in [1, 2, 4, 8, 12]:
    times = []
    for run in (threaded.run, aio.run):
        began = time.perf_counter()
        run(LINKS, workers)
        times.append(time.perf_counter() - began)
    print(f"{workers:>7}  {times[0]:>6.1f}s  {times[1]:>4.1f}s")
```

```bash
python sweep.py
```

```
workers  threads  async
      1     9.1s   9.1s
      2     4.9s   4.9s
      4     2.8s   2.8s
      8     2.2s   2.2s
     12     2.0s   2.0s
```

One worker takes about nine seconds, the same as one at a time. More workers help, up to a point, and threads and async match within a tenth of a second. The run is never shorter than its slowest link (the timeout), so beyond about eight or twelve workers there is little left to gain.

### What breaks

**1. Too many at once.** Lesson 5 showed a flood. If twelve workers are good, surely 24 are better. Asha runs the async version with 24 workers:

```bash
python linkcheck.py async 24
```

```
broken   503    26 ms  /old/classes
broken   404    19 ms  /gone/regex-course
broken   500    22 ms  /api/payments
broken   503    25 ms  /old/git
timeout    -  2017 ms  /hang/report
broken   503    25 ms  /old/sql
broken   404    21 ms  /gone/rust-course
broken   503    21 ms  /course/typing
down       -    12 ms  http://localhost:8627/up
24 links checked in 2.1 s
15 ok, 7 broken, 1 timeout, 1 down
```

It is a bit faster, but look at the summary: seven links are broken now, and before there were only three. Several lines show status 503, and every one of them is a page that was fine a moment ago. The server only allows 16 at a time and answered `503 too busy` to the rest. A checker that floods the server reports problems that are not real. Be polite: pick a number the server can take.

**2. An error that nobody catches.** This version of `check` has no `try`. `pool.map` hands the results over one by one, and when it reaches the link that times out, the error is raised right there. Guess what we see.

```python
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

from core import LINKS, OPTIONS, from_response

client = httpx.Client(**OPTIONS)


def check(url):
    start = time.perf_counter()
    response = client.get(url)
    return from_response(url, response, start)


with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(check, LINKS))
print(len(results), "links checked")
```

```bash
python nocatch.py
```

```
    ~~~~~~~~~~~~~~^^^^^^^
  File ".venv/lib/python3.14/site-packages/httpx/_transports/default.py", line 118, in map_httpcore_exceptions
    raise mapped_exc(message) from exc
httpx.ReadTimeout: timed out
```

No results at all (only the last lines of the long traceback are shown). The traceback is long, because the error travels through HTTPX and through the thread pool; at the bottom: `ReadTimeout`. One slow link killed the whole run and the 20 links that were fine are lost. Every job must turn its own errors into results.

**3. A blocking call in async code.** This file looks like the async version, but the request line uses `httpx.get` without `await`: an ordinary blocking call (lesson 5). Guess the time.

```python
import asyncio
import time

import httpx

from core import LINKS, OPTIONS, from_error, from_response, report


async def check(limit, url):
    async with limit:
        start = time.perf_counter()
        try:
            response = httpx.get(url, **OPTIONS)
        except httpx.HTTPError as error:
            return from_error(url, error, start)
        return from_response(url, response, start)


async def main():
    limit = asyncio.Semaphore(8)
    jobs = [check(limit, url) for url in LINKS]
    return await asyncio.gather(*jobs)


began = time.perf_counter()
results = asyncio.run(main())
report(results, time.perf_counter() - began)
```

```bash
python blocking.py
```

```
24 links checked in 9.2 s
16 ok, 3 moved, 3 broken, 1 timeout, 1 down
```

About nine seconds. The same as one at a time. A blocking call stops the whole event loop: the cook stands at one pot and stares at it. In async code, every call that waits must be an awaited one.

### Upgrades to try yourself

Pick one and try it.

- **Retry**: wrap `check` in the retry decorator from module 9, build 5, so that a link that fails once gets another chance.
- Ask with `head` instead of `get`, so the server sends only the headers and not the whole page.
- Add a command-line flag for the timeout.
- Print the slowest link.
- Read the links from a web page instead of a file.

## Common mistakes

1. Using more workers than the server can take: it answers `503` and your report shows fake problems.

2. Letting one error escape a worker: the whole run is lost. Catch `httpx.HTTPError` inside `check` and return a result.

3. Calling `httpx.get` (blocking) inside `async def`: no speed-up at all. Use the async client and `await`.

4. Creating a new client for every link instead of sharing one.

5. Forgetting the exit code: a robot cannot tell that the checker found problems.

## Clean up

Stop `server.py` with Control-C in its terminal window. `linkcheck.py` creates `report.json` next to the files, and the virtual environment is the `.venv` folder you made: delete both when you are done (`rm -f report.json; rm -rf .venv`).

## Next

Next module: [M13-L01 · Your First pytest Tests](../../m13-testing/m13-l01-your-first-pytest-tests/README.md). A checker like this deserves tests.
