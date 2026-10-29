# M15-L06 · Async Endpoints, Background Tasks and Docs

> Video: Module 15, Lesson 6. Watch it first, then follow along here.

## What you'll learn

- When to write `async def` and when a plain `def`, and how one blocking line can freeze a whole server
- Four ways to wait one second, and how to measure which ones are good
- Background tasks: send the email after the reply
- File upload with `UploadFile`, and why you never trust the file name
- The automatic docs page (`/docs`) and the `openapi.json` file behind it

## Before you start

- Python 3.14 or newer (`python --version`) and `uv`. No Docker is needed.
- A project with FastAPI added: `uv add "fastapi[standard]"`. That also installs `httpx` (used by the test scripts) and `python-multipart` (needed for file upload). Run below: FastAPI 0.162.0, uvicorn 0.54.0.
- Follows [M15-L05](../m15-l05-dependencies-routers-and-middleware/). `asyncio` and `gather` are from Module 12.
- Run from inside this folder. Each demo is one server file (started with `uv run fastapi dev <file>.py --port 8156`) and one client script (run in a second terminal with `uv run python <script>.py`). Stop the server with Control C before the next demo.
- Timings depend on your machine, and all the email addresses are fake demo values.

## Files in this folder

| File | What it is |
|------|------------|
| `speed.py`, `burst.py` | The problem: a plain `def` and an `async def` with `time.sleep(1)`, and Priya's ten-requests timer |
| `fix.py`, `burst_all.py` | Four ways to wait one second, plus a `/health` endpoint, and the timer for all four |
| `freeze.py` | Sends three slow requests and times a `/health` call |
| `welcome.py`, `enrol.py` | Sending the welcome email inline versus as a background task, and the timer |
| `upload.py`, `send_file.py` | Upload a PNG thumbnail; sends `thumb.png` and `notes.txt` |
| `thumb.png`, `notes.txt` | The picture (502 bytes) and a text file for the upload demo |
| `catalog.py`, `peek.py` | A documented API for the docs page, and a script that reads `openapi.json` |
| `forgot.py`, `ask.py` | Mistake: `asyncio.sleep(1)` without `await` |
| `welcome_fail.py`, `enrol_once.py` | Mistake: a background task that fails |
| `evil.py` | Mistake: trusting the file name |

## Follow along

### 1. The problem: `async` made it ten times slower (`speed.py`, `burst.py`)

Asha's two endpoints ask a (pretend) slow rating service, which needs one second:

```python
@app.get("/rating/plain")
def rating_plain():
    time.sleep(1)  # pretend: ask a slow rating service
    return {"rating": 4.8}


@app.get("/rating/async")
async def rating_async():
    time.sleep(1)  # the same slow service
    return {"rating": 4.8}
```

```bash
uv run fastapi dev speed.py --port 8156
```

In the second terminal, `burst.py` sends ten requests at once to each path with `asyncio.gather` and a stopwatch:

```bash
uv run python burst.py
```

```
/rating/plain: ten requests took 1.1 seconds
/rating/async: ten requests took 10.1 seconds
```

Your numbers will be close. The plain `def` ran in ten helper threads side by side. The `async def` ran on the one event loop, and `time.sleep` is not an `await`, so while it sleeps the whole server sleeps: a staircase of ten seconds.

The two deals:

- A plain `def` runs in a thread from a pool. A waiting thread does not stop the others.
- An `async def` runs right on the event loop (the one cook of Module 12), and it must `await` at every wait. At an `await` the cook turns to the next customer.

### 2. Four ways to wait (`fix.py`, `burst_all.py`)

```python
@app.get("/rating/plain")
def rating_plain():
    time.sleep(1)
    return {"rating": 4.8}


@app.get("/rating/await")
async def rating_await():
    await asyncio.sleep(1)
    return {"rating": 4.8}


@app.get("/rating/blocked")
async def rating_blocked():
    time.sleep(1)
    return {"rating": 4.8}


@app.get("/rating/thread")
async def rating_thread():
    await asyncio.to_thread(time.sleep, 1)
    return {"rating": 4.8}
```

(`fix.py` also has `/health`, which answers at once.) Stop the old server, then:

```bash
uv run fastapi dev fix.py --port 8156
```

```bash
uv run python burst_all.py
```

```
/rating/plain: ten requests took 1.0 seconds
/rating/await: ten requests took 1.0 seconds
/rating/blocked: ten requests took 10.0 seconds
/rating/thread: ten requests took 1.0 seconds
```

Three good ways and one trap. The fourth endpoint is an `async def`, but the blocking call was moved to a thread, so nothing freezes.

The rule: can you `await` every slow call inside the endpoint? An async library (for example the async httpx client) means `async def`. An ordinary library (a database driver without async, a file read, plain `requests`) means a plain `def`.

### 3. The freeze is worse than the lost time (`freeze.py`)

`freeze.py` sends three slow requests, waits 0.2 seconds, and times one `/health` call:

```bash
uv run python freeze.py
```

```
/rating/blocked: health took 2.8 seconds
/rating/thread: health took 0.0 seconds
```

The health check, which needs no time at all, stood in the queue behind the sleeping requests. A health check that waits is how a busy server looks dead to the tools that watch it. Do not conclude that a plain `def` is always best: threads cost memory and a pool has a limit, and neither choice speeds up heavy counting (that needs processes, Module 12, Lesson 3).

### 4. Background tasks (`welcome.py`, `enrol.py`)

Sending the welcome email takes two seconds (pretended with `time.sleep(2)`). `enrol_slow` does it inline. `enrol` asks FastAPI for a `BackgroundTasks` object and only names the function:

```python
@app.post("/enrolments", status_code=201)
def enrol(
    enrolment: Enrolment, background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        send_welcome_email,
        enrolment.email,
        enrolment.course_id,
    )
    return {"status": "enrolled"}
```

Note the function is not called with `()`: it is only named, with its arguments.

```bash
uv run fastapi dev welcome.py --port 8156
```

```bash
uv run python enrol.py
```

```
/enrolments/slow: 201 in 2.0 seconds
/enrolments: 201 in 0.0 seconds
```

In the server window, for the slow path the email line comes before the log line of the reply. For the background path the reply is logged first, and the email line appears two seconds later:

```
email sent to lukas@example.com for course 7
INFO:     127.0.0.1:62714 - "POST /enrolments/slow HTTP/1.1" 201 Created
INFO:     127.0.0.1:62926 - "POST /enrolments HTTP/1.1" 201 Created
email sent to lukas@example.com for course 7
```

(Ports will differ.) A background task follows the endpoint's rules: a plain `def` runs in a thread, an `async def` runs on the event loop. It runs in the same process, right after the reply: if the server stops at that moment the task is lost, nobody retries it, and its result never returns to Lukas. Use it for small, quick work (an email, a log line, clearing a cache). For important jobs use a queue (Module 18).

### 5. File upload (`upload.py`, `send_file.py`)

Files arrive as multipart form data, which needs the `python-multipart` package. With plain `fastapi` (no `standard` extras) and `uvicorn upload:app`, the server refuses to start and prints (the traceback after it is long):

```
Form data requires "python-multipart" to be installed. 
You can install "python-multipart" with: 

pip install python-multipart
```

With `fastapi[standard]` it is already there. The endpoint takes the file from the form with the type `UploadFile`, refuses anything that is not a PNG, and saves with a name of its own:

```python
@app.post("/courses/{course_id}/thumbnail")
async def upload_thumbnail(course_id: int, file: UploadFile):
    if file.content_type != "image/png":
        raise HTTPException(
            status_code=415, detail="Only PNG images"
        )
    data = await file.read()
    target = UPLOADS / f"course-{course_id}.png"
    await asyncio.to_thread(target.write_bytes, data)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(data),
    }
```

```bash
uv run fastapi dev upload.py --port 8156
```

```bash
uv run python send_file.py
```

```
thumb.png 200
{'filename': 'thumb.png', 'content_type': 'image/png', 'size': 502}
notes.txt 415
{'detail': 'Only PNG images'}
```

The server creates an `uploads/` folder next to `upload.py` and writes `course-7.png` into it. `UploadFile` is a file object (name, declared content type, `read`), not a lump of memory: big files go to disk past a size limit.

### 6. The free docs page (`catalog.py`, `peek.py`)

```bash
uv run fastapi dev catalog.py --port 8156
```

Open `http://localhost:8156/docs` in a browser. Nobody drew that page: FastAPI built it from the routes, type hints and models. `catalog.py` shows how to control the words:

- `FastAPI(title=..., description=..., version=...)` for the top of the page
- `Field(description="In rupees", examples=[999])` for one field of a model
- `tags=[...]` and `summary=...` per endpoint, which group and name it
- the docstring under the function becomes the description
- `responses={404: {"description": "No such course"}}` documents an extra answer

Click `GET /courses/{course_id}`, press Try it out, enter `7` and Execute: you get a real `200` answer from your own server. The page knows `course_id` is an integer in the path, from your hint. There is a second style at `http://localhost:8156/redoc`.

Behind the page stands `/openapi.json`, a plain JSON file in a standard called OpenAPI. Other tools read it too, to build test clients or code for other languages. `peek.py` reads it:

```bash
uv run python peek.py
```

```
allcsvideos catalog API 1.0.0
GET /courses/{course_id} - Get one course
POST /enrolments - Enrol a student
['Course', 'Enrolment', 'HTTPValidationError', 'ValidationError']
```

The start of the file, from `curl localhost:8156/openapi.json`:

```
{"openapi":"3.1.0","info":{"title":"allcsvideos catalog API","description":"Courses and enrolments for allcsvideos.com.","version":"1.0.0"},"paths":{"/courses/{course_id}":{"get":{"tags":["courses"],"
```

(cut after 200 characters). A warning: these pages are public, on the same address as your API. In production switch them off or protect them: `FastAPI(docs_url=None, redoc_url=None, openapi_url=None)` makes `/docs`, `/redoc` and `/openapi.json` all answer `404`.

## Common mistakes

1. Forgetting the `await`. `forgot.py` has `asyncio.sleep(1)` with no `await`. Start it (`uv run fastapi dev forgot.py --port 8156`) and run `uv run python ask.py`:

   ```
   200 {'rating': 4.8} 0.03 seconds
   ```

   Suspiciously fast: nobody waited. The server window prints the warning from Module 12, Lesson 4:

   ```
   forgot.py:10: RuntimeWarning: coroutine 'sleep' was never awaited
     asyncio.sleep(1)  # pretend: ask a slow rating service
   ```

   The fix is one word: `await`.
2. A background task that fails. In `welcome_fail.py` the email function raises `ConnectionError("the email service is down")`. Start it and run `uv run python enrol_once.py`:

   ```
   201 {'status': 'enrolled'}
   ```

   Lukas sees success. The server window shows a long traceback that ends with `ConnectionError: the email service is down`. The reply was already sent, so nobody is left to answer with an error: the failure lives only in the log. Log your own errors inside a background task.
3. Trusting the file name. `evil.py` sends the picture with the name `../../evil.png`:

   ```
   {'filename': '../../evil.png', 'content_type': 'image/png', 'size': 502}
   ```

   The name comes from the client, so anybody can write anything there. Used as a path it could escape the folder. That is why `upload.py` saves as `course-<id>.png`, a name the server chose.

## Clean up

Stop the server with Control C. The upload demo created an `uploads/` folder: delete it (`rm -r uploads`).

## Next

[M15-B08 · Build a Course Catalog API](../m15-b08-build-a-course-catalog-api/)
