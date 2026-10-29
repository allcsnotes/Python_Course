# M07-L04 · Third-Party Packages and PyPI

> Video: Module 7, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- What third-party packages are, and that PyPI (the Python Package Index) is the public warehouse they come from
- How `uv add` installs a package together with its helpers (dependencies), and records the order in `pyproject.toml` and `uv.lock`
- Five quick checks before you trust a package: name, alive, used, license, people (and why typosquatting matters)
- How to read documentation in order: first paragraph, quickstart, API reference
- Your first web request with `httpx`: `httpx.get`, the status code, `.json()`, a `timeout`, and `raise_for_status()`
- How to turn network failures into one clear error of your own, plus three pitfalls (shadowing, install name versus import name, copied commands)

## Before you start

- Python 3.14 or newer: `python --version` (on some systems `python3`).
- `uv` installed (Module 1, lesson 2). The video used uv 0.13.5. Check with `uv --version`.
- Internet access to download `httpx`, `pillow` and `requests` from PyPI. No Docker is needed.
- Lesson M07-L03 (virtual environments and `uv add`, `uv run`, `uv sync`) is assumed. Each project folder here is a uv project like the ones in that lesson.
- Two terminals. The lesson uses a small practice service on your own computer (`server.py`), so every result is repeatable and nothing leaves your machine.

## Files in this folder

| File | What it is |
|------|------------|
| `server.py` | The practice service: serves `/courses`, a slow `/slow` (3 seconds), a broken `/oops` (500), and 404 for everything else, on `localhost:8074` |
| `allcs-api/` | The main uv project (`httpx` installed): `pyproject.toml`, `uv.lock`, `.python-version`, `main.py` and the example programs below |
| `allcs-api/fetch1.py` | `httpx.get`, print the status code |
| `allcs-api/fetch2.py` | Also print the response text |
| `allcs-api/fetch3.py` | `response.json()` and a loop over the courses |
| `allcs-api/slow.py` | A one second `timeout` against the slow door |
| `allcs-api/missing1.py` | A 404, then `.json()` crashes |
| `allcs-api/missing2.py` | Same, with `raise_for_status()` |
| `allcs-api/svc.py` | `fetch_courses` wraps `httpx` errors in your own `CourseServiceError` |
| `allcs-api/use.py` | Calls `fetch_courses` for five cases |
| `allcs-api/family.py` | Shows that all `httpx` errors share the parent `HTTPError` |
| `allcs-api/tryit.py` | A model answer for "Try it yourself" |
| `pitfalls/httpx.py` | A file named like the package (pitfall 1) |
| `allcs-pic/` | uv project with `pillow`, `pil1.py` and `pil2.py` (pitfall 2) |
| `allcs-old/` | uv project with `requests` and `req.py` (the older, famous package) |

Replace `python` with `python3` if needed. Each project folder is already set up, so you can skip the "from scratch" commands and run `uv sync` inside the folder instead (see step 2). Traceback paths below are shortened to `~`.

## Follow along

### 1. Start the practice service

Open a terminal in this folder and keep it open:

```bash
python server.py
```

It prints nothing. It waits for requests on `http://localhost:8074`. Use a second terminal for everything else. (Stop the service later with Ctrl+C.)

### 2. Place the order: `uv add httpx`

Asha's program asks Priya's service for the list of courses, using `httpx`. Creating the project from scratch, as in the last lesson:

```bash
mkdir allcs-api
cd allcs-api
uv init --no-package
uv add httpx
```

```
Initialized project `allcs-api`
Using CPython 3.14.9 interpreter at: /usr/local/bin/python3.14
Creating virtual environment at: .venv
Resolved 8 packages in 188ms
Prepared 7 packages in 113ms
Installed 7 packages in 93ms
 + anyio==4.15.1
 + certifi==2026.10.23
 + h11==0.16.0
 + httpcore==1.0.9
 + httpx==0.28.1
 + idna==3.20
 + typing-extensions==4.16.0
```

(Your Python version and the timings differ.) Seven packages, when we asked for one: `httpx` needs helpers of its own, called dependencies, and helpers can need helpers. `uv tree` draws who needs whom:

```bash
uv tree
```

```
Resolved 8 packages in 7ms
allcs-api v0.1.0
└── httpx v0.28.1
    ├── anyio v4.15.1
    │   ├── idna v3.20
    │   └── typing-extensions v4.16.0
    ├── certifi v2026.10.23
    ├── httpcore v1.0.9
    │   ├── certifi v2026.10.23
    │   └── h11 v0.16.0
    └── idna v3.20
```

`pyproject.toml` got its shopping list line, and `uv.lock` holds the exact version of all seven:

```toml
dependencies = [
    "httpx>=0.28.1",
]
```

If you would rather use the ready-made project in this repo, skip the commands above and run, from this lesson's folder:

```bash
cd allcs-api
uv sync
```

`uv sync` installs the exact versions from `uv.lock`.

The older tool is `pip install requests`, and both fetch from the same warehouse (PyPI). `uv add` also writes the order into your project file, which is why this course uses it.

### 3. Should you trust it? Five checks

Installing a package means running somebody else's code on your computer. PyPI is open to everybody: most packages are excellent, a few are broken, abandoned or harmful. Before every new package, spend two minutes on these, using the package's page on PyPI:

1. **Name.** Bad people upload packages with names that look almost right (typosquatting). Copy the name from the project's own documentation and read it letter by letter. Do not install a look-alike, even to test.
2. **Alive.** Open the release history. `httpx` has published releases regularly since 2019. A package last released many years ago may never get a security fix.
3. **Used.** A statistics site shows downloads. `httpx` is downloaded hundreds of millions of times a month, so problems get noticed fast. Popular is a hint, not a proof.
4. **License.** The written rule about what you may do with the code. `httpx` uses the BSD license: use it freely, even in a product you sell. No license means no permission. Your company may have its own list of allowed licenses.
5. **People.** A link to the source code (on GitHub) and the documentation. Open source means anyone can read the code. No source link, no documentation, no history: be careful.

One more habit: count the helpers. `httpx` brought six. A package that drags in hundreds deserves a second thought. For `httpx` all five answers are good, so we use it.

### 4. Read the documentation

`httpx` keeps its manual at `python-httpx.org`. Most documentation sites have three parts: the quickstart (a short tour with examples to copy), the guides (longer chapters, one topic each, like timeouts) and the API reference (every function, its inputs and its result). Read in this order:

1. The first paragraph, to confirm it is the right tool.
2. The first quickstart example, run exactly as written.
3. When you need more, search the reference for the function you use and read its inputs. Not every line, only the one you need.

Try it with `httpx.get`: the first input is the URL, followed by optional ones, each with a default (the value used when you say nothing). One is `timeout`, default five seconds; you pass it by name as a keyword argument.

### 5. Your first request

A request goes to a service, which sends back a response. Think of a library desk: you ask for the list of courses, and the librarian hands over the answer with a slip saying how it went. The address is a URL: `http://localhost:8074/courses`. `localhost` means this very computer, `8074` is the port (the numbered door of the program), and `/courses` is the question. `get` means "just give me information, change nothing".

`allcs-api/fetch1.py`:

```python
import httpx

response = httpx.get("http://localhost:8074/courses")
print(response.status_code)
```

```bash
uv run fetch1.py
```

```
200
```

The number on the slip is the status code. 200 means all good, 404 means "not found", 500 means "something broke on the server". A number starting with 2 is success; 4 is your mistake; 5 is the server's mistake.

`allcs-api/fetch2.py` also prints the text:

```python
import httpx

url = "http://localhost:8074/courses"
response = httpx.get(url)
print(response.status_code)
print(response.text)
```

```bash
uv run fetch2.py
```

```
200
[{"id": "C101", "title": "Python", "price": 499}, {"id": "C102", "title": "SQL", "price": 399}, {"id": "C103", "title": "Docker", "price": 449}]
```

That is JSON, plain text: not yet a list. `response.json()` does the `json.loads` you know and returns real Python data. `allcs-api/fetch3.py`:

```python
import httpx

url = "http://localhost:8074/courses"
response = httpx.get(url)
courses = response.json()
print(type(courses))
for course in courses:
    print(course["title"], course["price"])
```

```bash
uv run fetch3.py
```

```
<class 'list'>
Python 499
SQL 399
Docker 449
```

A list of dictionaries, ready for the loops and key lookups you already know.

### 6. The older package: `requests`

`requests` is the older, very famous package for the same job, and you will meet it in many tutorials. `allcs-old/` is a bare uv project with it (made with `uv init --bare` and `uv add requests`):

```bash
cd ../allcs-old
uv sync
uv run req.py
cd ../allcs-api
```

```python
import requests

response = requests.get("http://localhost:8074/courses")
print(response.status_code)
print(response.json()[0])
```

```
200
{'id': 'C101', 'title': 'Python', 'price': 499}
```

Same status, same JSON. We use `httpx` because it is newer and has a safe default timeout, which `requests` does not. The ideas are identical.

### 7. Always set a timeout

A program that asks and then waits forever is a frozen program. `/slow` waits three seconds before answering. With a limit of one second, `allcs-api/slow.py`:

```python
import httpx

url = "http://localhost:8074/slow"
response = httpx.get(url, timeout=1)
print(response.status_code)
```

```bash
uv run slow.py
```

The traceback is long (most of it lives inside `httpx`). Read the last line:

```
httpx.ReadTimeout: timed out
```

The program did not hang; it told us. `httpx` waits five seconds by default; `requests` waits forever unless you set a timeout. Always choose one yourself.

### 8. A missing page: 404 is not an error (yet)

`allcs-api/missing1.py`:

```python
import httpx

response = httpx.get("http://localhost:8074/missing")
print(response.status_code)
print(response.json())
```

```bash
uv run missing1.py
```

```
404
Traceback (most recent call last):
  File "~/allcs-api/missing1.py", line 5, in <module>
    print(response.json())
...
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```

`404` prints with no error on the `get` line: `httpx` did its job; the answer happened to be "not found". Then `.json()` crashes, because the answer was a page of text. The real problem is the 404, but the crash blames the JSON line (a quiet failure that shows up far from its cause). Fail early and loudly with `raise_for_status()`: nothing happens for a 2xx status, and it raises for 4xx and 5xx. `allcs-api/missing2.py`:

```python
import httpx

response = httpx.get("http://localhost:8074/missing")
response.raise_for_status()
print(response.json())
```

```bash
uv run missing2.py
```

```
Traceback (most recent call last):
  File "~/allcs-api/missing2.py", line 4, in <module>
    response.raise_for_status()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "~/allcs-api/.venv/lib/python3.14/site-packages/httpx/_models.py", line 829, in raise_for_status
    raise HTTPStatusError(message, request=request, response=self)
httpx.HTTPStatusError: Client error '404 Not Found' for url 'http://localhost:8074/missing'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404
```

The habit: `get`, then `raise_for_status()`, then use the data.

### 9. Wrap the errors in your own: `svc.py` and `use.py`

The network goes wrong in three ways: the service is down (`httpx.ConnectError`), too slow (a timeout error) or answers 4xx/5xx (`httpx.HTTPStatusError`). All are exceptions, so you can catch them as in the exceptions lessons. `allcs-api/svc.py`:

```python
import httpx


class CourseServiceError(Exception):
    pass


def fetch_courses(url):
    try:
        response = httpx.get(url, timeout=2)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as error:
        code = error.response.status_code
        raise CourseServiceError(f"server said {code}") from error
    except httpx.TimeoutException as error:
        raise CourseServiceError("server too slow") from error
    except httpx.ConnectError as error:
        raise CourseServiceError("cannot reach server") from error
```

The calling code no longer needs to know anything about `httpx`. Raise where you detect, catch where you decide. `allcs-api/use.py` imports it (a file is a module) and tries four paths, plus a port where nothing runs:

```python
from svc import CourseServiceError, fetch_courses

BASE = "http://localhost:8074"
paths = ["/courses", "/missing", "/oops", "/slow"]
for path in paths:
    try:
        courses = fetch_courses(BASE + path)
        print(path, "ok,", len(courses), "courses")
    except CourseServiceError as error:
        print(path, "failed:", error)

try:
    fetch_courses("http://localhost:8099/courses")
except CourseServiceError as error:
    print("port 8099 failed:", error)
```

```bash
uv run use.py
```

```
/courses ok, 3 courses
/missing failed: server said 404
/oops failed: server said 500
/slow failed: server too slow
port 8099 failed: cannot reach server
```

(It takes about two seconds, waiting for `/slow`.) Five different problems, five clear sentences, no traceback, and the program keeps going.

A shortcut: all of `httpx`'s errors share one parent, `httpx.HTTPError`. When you do not need to tell them apart, one `except httpx.HTTPError` catches them all. `allcs-api/family.py` checks it:

```bash
uv run family.py
```

```
True
True
True
```

### 10. Try it yourself

Using the practice service: get `/courses` with a timeout of 2, call `raise_for_status()`, print the title of every course with a price under 450, all inside `try`, catching `httpx.HTTPError` with a friendly message. A model answer is `allcs-api/tryit.py`:

```python
import httpx

url = "http://localhost:8074/courses"
try:
    response = httpx.get(url, timeout=2)
    response.raise_for_status()
    for course in response.json():
        if course["price"] < 450:
            print(course["title"])
except httpx.HTTPError as error:
    print("Could not load the courses:", error)
```

```bash
uv run tryit.py
```

```
SQL
Docker
```

Stop `server.py` and run it again to see the friendly message: `Could not load the courses:` followed by the connection error text, which depends on your system.

### 11. Pitfall 1: naming your file like the package

Copy `pitfalls/httpx.py` into `allcs-api/` and run it:

```bash
cp ../pitfalls/httpx.py httpx.py
uv run httpx.py
```

```
Traceback (most recent call last):
  File "~/allcs-api/httpx.py", line 1, in <module>
    import httpx
  File "~/allcs-api/httpx.py", line 3, in <module>
    response = httpx.get("http://localhost:8074/courses")
               ^^^^^^^^^
AttributeError: module 'httpx' has no attribute 'get' (consider renaming '~/allcs-api/httpx.py' if it has the same name as a library you intended to import)
```

Python looks in your own folder first, so `import httpx` found Asha's file (the file itself) instead of the package. Never name your files after a package you use. Remove the file now:

```bash
rm httpx.py
```

### 12. Pitfall 2: the install name is not the import name

`allcs-pic/` is a uv project with `pillow` (the picture library) added:

```bash
cd ../allcs-pic
uv sync
uv run pil1.py
```

`pil1.py` is `import pillow` followed by `print(pillow.__name__)`:

```
Traceback (most recent call last):
  File "~/allcs-pic/pil1.py", line 1, in <module>
    import pillow
ModuleNotFoundError: No module named 'pillow'
```

The package is called `pillow` on PyPI, but the module inside is called `PIL`, in capital letters. Two names for one thing. The quickstart of the documentation shows the import line, so read it first and copy the import exactly. `pil2.py` is `import PIL` and `print(PIL.__name__)`:

```bash
uv run pil2.py
```

```
PIL
```

(While creating the project the video ran `uv init --no-package` and `uv add pillow`; the lock file pins `pillow==13.0.0`, which prints `+ pillow==13.0.0` on install.)

### 13. Pitfall 3: installing from a copied command

A blog post, a chat answer, even an AI answer can suggest a package name that is slightly wrong or does not exist, and someone may have registered that exact name on purpose. Check the name on PyPI and run the five checks before you add anything.

## Interview question

Rahul asks: a teammate wants to add a new third-party package to the production project. What do you check before you say yes? Model answer: I check that the name is the right one, to avoid typosquatting; that it is maintained, with recent releases; that it is widely used; that its license allows our use; and how many dependencies it brings. Then I add it with uv, so the exact version is pinned in the lock file, and I keep it behind our own small function so we can replace it later. For anything that talks to the network, I always set a timeout and handle the errors.

## Common mistakes

- Installing a package without checking its exact name, age, use, license and people.
- Naming your own file `httpx.py` (or `requests.py`, `random.py`): it shadows the real package.
- Assuming the install name is the import name (`pillow` installs `PIL`). Copy the import line from the quickstart.
- Calling `.json()` before `raise_for_status()`: the crash points at the wrong line.
- Forgetting a `timeout` (with `requests` the program can wait forever) and not catching network errors.
- Running `pip install` inside a uv project instead of `uv add` (lesson M07-L03).

## Clean up

Stop the practice service with Ctrl+C in its terminal. Then remove the virtual environments and any caches that `uv` created inside this lesson's folders:

```bash
rm -rf allcs-api/.venv allcs-pic/.venv allcs-old/.venv
find . -name __pycache__ -type d -exec rm -rf {} +
```

Run these from the lesson folder (`m07-l04-third-party-packages-and-pypi`). If you created the projects from scratch in another folder, delete that folder instead.

## Next

That finishes Module 7. Continue with [M08-L01 · Classes and Objects](../../m08-object-oriented-programming/m08-l01-classes-and-objects/README.md).
