# M15-L01 · How the Web Works and Your First Endpoint

> Video: Module 15, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- What travels in a request (method, path, headers) and in a response (status code, headers, body)
- What a server program (uvicorn) and a web framework (FastAPI) each do
- How to write and run your first endpoints with `@app.get(...)`
- How to call your own server with `curl`, a browser and `httpx`
- Four classic mistakes: running the file like a script, `print` instead of `return`, server not running, port already taken

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- `uv` installed (Module 7, Lesson 3). No Docker is needed.
- No earlier lesson folder is needed.
- Make a project and add FastAPI. The `standard` extra brings uvicorn and the `fastapi` command along:

```bash
mkdir m15-l01 && cd m15-l01
uv init
uv add "fastapi[standard]"
uv run python -c "import fastapi, uvicorn; print(fastapi.__version__, uvicorn.__version__)"
```

You should see:

```
0.162.0 0.54.0
```

Any recent version behaves the same in this lesson. (If you do not use `uv`: create a venv, activate it, and run `pip install "fastapi[standard]"`; then drop `uv run` from the commands below.)

## Files in this folder

| File | What it is |
|------|------------|
| `courses.py` | The hook: a plain function `list_courses()` that only works on Asha's computer |
| `v1/main.py` | The first endpoint: `GET /` returns a welcome message |
| `main.py` | The final app: `GET /` and `GET /courses` |
| `client.py` | A Python client (httpx) that asks the server for the courses |
| `peek.py` | Prints what `home()` returns and the path of every route |
| `pitfall-print-instead-of-return/main.py` | The `print`-instead-of-`return` mistake |

## Follow along

### 1. The problem: a function nobody else can call

```bash
python courses.py
```

You should see:

```
['Python', 'SQL', 'Docker']
```

It works on Asha's computer. Lukas's phone cannot reach inside her program, so something on her side must wait for questions. That is a server.

### 2. Read the shape of a request and a response

A request has three parts that matter: the method (`GET` means "give me information, change nothing"), the path (such as `/courses`) and headers (small labelled notes). A response has a status code (200, 404, 500), headers and a body. Between them sit uvicorn (listens at a port, reads the raw text) and FastAPI (a routing table that pairs a method and a path with your function). Your function only returns plain Python data.

### 3. The first endpoint

Open `v1/main.py`. Line 1 imports the class, line 3 makes the `app` object that holds the routing table, and `@app.get("/")` registers `home` for the method GET and the path `/`:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to allcsvideos"}
```

### 4. Start the server

Copy `v1/main.py` to `main.py` in your project (or use this folder's `main.py`, which also has the second endpoint), then:

```bash
uv run fastapi dev main.py --port 8151
```

`dev` means development mode: the server restarts when you save. We pick port 8151 so it never clashes with another program. You should see (the folder path and process ids will differ):

```
 ⚡️ Starting FastAPI in development mode
 🐍 Using import string: main:app
 🌐 Server started at http://127.0.0.1:8151
    Documentation at http://127.0.0.1:8151/docs
  Logs:
INFO:     Will watch for changes in these directories: ['/path/to/your/folder']
INFO:     Uvicorn running on http://127.0.0.1:8151 (Press CTRL+C to quit)
INFO:     Started reloader process [2861] using WatchFiles
INFO:     Started server process [2889]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The prompt does not come back: the server is waiting. Leave this terminal alone. `127.0.0.1` means "this computer only".

### 5. Ask with curl (open a second terminal)

```bash
curl -i localhost:8151/
```

The flag `-i` also shows the response headers:

```
HTTP/1.1 200 OK
date: Mon, 26 Oct 2026 04:51:28 GMT
server: uvicorn
content-length: 36
content-type: application/json

{"message":"Welcome to allcsvideos"}
```

The date will differ. Your function returned a Python dictionary; the framework turned it into JSON and added the `content-type` header. In the first terminal the server logged the visit:

```
INFO:     127.0.0.1:55412 - "GET / HTTP/1.1" 200 OK
```

### 6. Add the courses endpoint

Now use the final `main.py` of this folder. It adds the data and a second route:

```python
from fastapi import FastAPI

app = FastAPI()

COURSES = [
    {"id": 1, "title": "Python", "price": 499, "level": "beginner"},
    {"id": 2, "title": "SQL", "price": 399, "level": "beginner"},
    {"id": 3, "title": "Docker", "price": 449, "level": "intermediate"},
]


@app.get("/")
def home():
    return {"message": "Welcome to allcsvideos"}


@app.get("/courses")
def list_courses():
    return COURSES
```

Save the file and watch the server terminal. It reloads by itself:

```
WARNING:  WatchFiles detected changes in 'main.py'. Reloading...
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [2889]
INFO:     Started server process [2947]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

```bash
curl localhost:8151/courses
```

```
[{"id":1,"title":"Python","price":499,"level":"beginner"},{"id":2,"title":"SQL","price":399,"level":"beginner"},{"id":3,"title":"Docker","price":449,"level":"intermediate"}]
```

A browser is a client too: open `http://localhost:8151/courses` and you see the same text.

### 7. Ask from Python

```bash
python client.py
```

`client.py` is the Module 7 client, nearly unchanged (it needs `httpx`, which `fastapi[standard]` already installed; use `uv run python client.py` inside the project):

```
200
application/json
Python 499
SQL 399
Docker 449
```

JSON is the shared language: a Python list became text on the server and a Python list again on the client.

### 8. See what really travelled

```bash
curl -sv localhost:8151/ 2>&1 | grep '^[<>]'
```

Lines starting with `>` were sent, lines starting with `<` were received:

```
> GET / HTTP/1.1
> Host: localhost:8151
> User-Agent: curl/8.7.1
> Accept: */*
> 
< HTTP/1.1 200 OK
< date: Mon, 26 Oct 2026 04:51:28 GMT
< server: uvicorn
< content-length: 36
< content-type: application/json
< 
```

Your curl version and the date will differ. A request is only text: method, path, protocol, then headers.

### 9. A wrong path gives 404

```bash
curl -i localhost:8151/lessons
```

```
HTTP/1.1 404 Not Found
date: Mon, 26 Oct 2026 04:51:33 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

### 10. A wrong method gives 405

Our routes only know GET:

```bash
curl -i -X POST localhost:8151/courses
```

```
HTTP/1.1 405 Method Not Allowed
date: Mon, 26 Oct 2026 04:51:33 GMT
server: uvicorn
allow: GET
content-length: 31
content-type: application/json

{"detail":"Method Not Allowed"}
```

The `allow: GET` header tells the visitor what this path accepts. The common methods: GET (look), POST (hand in something new), PUT (replace), PATCH (fix a part), DELETE (remove). Status codes you will meet soon: 201 created, 204 no content, 400 bad request, 401 who are you, 403 not allowed, 409 conflict, 422 wrong shape, 500 our mistake.

### 11. Look inside the app

```bash
python peek.py
```

```
{'message': 'Welcome to allcsvideos'}
/openapi.json
/docs
/docs/oauth2-redirect
/redoc
/
/courses
```

You can call `home()` directly because the decorator only registers it and hands it back. Four routes were added by FastAPI itself. Open `http://localhost:8151/docs` to see an interactive page built from your two routes.

## Common mistakes

1. Running the file like a script. `python main.py` prints nothing and exits with code 0: the file only builds the routing table. The `app` object is not a server. Use `fastapi dev main.py` (or `uvicorn`).
2. `print` instead of `return`. Copy `pitfall-print-instead-of-return/main.py` over `main.py` and ask for `/`:

   ```bash
   curl -i localhost:8151/
   ```

   ```
   HTTP/1.1 200 OK
   date: Mon, 26 Oct 2026 04:51:37 GMT
   server: uvicorn
   content-length: 4
   content-type: application/json

   null
   ```

   The function returned `None`, which becomes `null` with a success status. The dictionary was printed on the server terminal instead. A function answers with `return`, never with `print`.
3. The server is not running. Stop it with Control C, then ask again:

   ```
   curl: (7) Failed to connect to localhost port 8151 after 0 ms: Couldn't connect to server
   ```

   `client.py` ends with `httpx.ConnectError: [Errno 61] Connection refused` (the number can differ on other systems). Nobody listens at that door: start the server.
4. The port is taken. Starting a second server on 8151 while the first runs fails with `ERROR:    [Errno 48] Address already in use`. One port, one listener. Stop the old one, or choose another port.

## Clean up

Press Control C in the server terminal (you should see `Application shutdown complete.`). Delete the `m15-l01` project folder if you do not need it.

## Next

[M15-L02 · Parameters, Bodies and Responses](../m15-l02-parameters-bodies-and-responses/)
