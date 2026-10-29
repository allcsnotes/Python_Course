# M15-L03 · Pydantic Models

> Video: Module 15, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- Why a `dict` body lets bad data far into your program, and how a Pydantic model checks data at the door
- Models with typed fields, defaults, `Field` rules, enums and nested models
- How errors are reported (all at once, with a location, a message and a type)
- Using a model as the request body, and a separate output model as `response_model` so a password never leaves
- Reading settings from environment variables with `BaseSettings`
- Four mistakes: assigning later, ignored extra fields, forgetting the response model, treating a model like a dict

## Before you start

- Python 3.14 or newer (`python --version`) and `uv`. No Docker is needed.
- A project with FastAPI added: `uv add "fastapi[standard]"`. That also installs Pydantic and `pydantic-settings`, which this lesson uses. (Versions in the run below: Pydantic 2.14.1, FastAPI 0.162.0, pydantic-settings 2.16.2.)
- Follows [M15-L02](../m15-l02-parameters-bodies-and-responses/) (the `dict` body that accepted anything).
- Copy the files you need into your project folder. Every `.py` file here runs on its own, from this folder: `uv run python first_model.py`. The server demos use port 8153, and need a second terminal for the client.

## Files in this folder

| File | What it is |
|------|------------|
| `hook_app.py`, `send_hook.py` | The problem: a `dict` body and a `/total` route, and Priya's client |
| `kinds.py`, `compare.py` | The same course as a `TypedDict`, a dataclass and a Pydantic model |
| `first_model.py` | The first model, `Course`, with a default level |
| `bad_input.py` | Missing field plus wrong type: both errors reported together |
| `from_json.py` | `model_validate_json` and `model_validate` |
| `rules.py` | `Field(min_length=..., gt=...)` rules |
| `levels.py`, `level_run.py` | An `Enum` as a field type |
| `defaults.py` | List default (no shared-default trap) and an optional field |
| `catalog.py`, `nested_run.py` | Models inside models, and the error location |
| `app_models.py`, `send_models.py` | `CourseIn` as the request body, and a bad request |
| `dump.py` | `model_dump`, `model_dump_json`, `mode="json"`, `exclude` |
| `students.py`, `app_out.py`, `send_out.py` | `StudentIn` and `StudentOut`: the password is never returned |
| `app_leak.py` | The mistake: no response model, the password leaks |
| `settings.py` | `BaseSettings` reading `ALLCS_...` environment variables |
| `assign.py`, `assign_fix.py` | Changing a field after creation, and `validate_assignment` |
| `extra.py` | Ignored extra fields versus `extra="forbid"` |
| `not_dict.py` | A model is not a dictionary |

## Follow along

### 1. The problem

Start the hook app, then in a second terminal run the client:

```bash
uv run python -m uvicorn hook_app:app --port 8153 --log-level warning
```

```bash
uv run python send_hook.py
```

`hook_app.py` takes `body: dict`, appends it to a list, and `/total` adds up the prices. The client sends a good course, one with price `"free"`, and one with no price:

```
201 {'title': 'Python Basics', 'price': 1499}
201 {'title': 'Pydantic', 'price': 'free'}
201 {'title': 'Oops'}
500 Internal Server Error
```

Everything was accepted, and then `/total` crashed on the text `free`. Bad data went far inside before anything broke. Stop the server (Control C).

### 2. Three tools for three jobs

```bash
uv run python compare.py
```

```
TypedDict: free
dataclass: free
BaseModel: 1 error
```

A `TypedDict` describes a dictionary for the type checker, before the program runs. A dataclass is a tidy object for your own code. Only a Pydantic model checks data that comes from outside (a request, a file, the environment) while the program runs.

### 3. Your first model

```python
from pydantic import BaseModel


class Course(BaseModel):
    title: str
    price: int
    level: str = "beginner"
```

```bash
uv run python first_model.py
```

```
title='Python Basics' price=1499 level='beginner'
Python Basics 1499
1499 <class 'int'>
```

The text `"1499"` was turned into the number 1499. Pydantic converts when the text clearly means the number.

### 4. Bad data: every problem at once

```bash
uv run python bad_input.py
```

```
2 problems
('title',) Field required
  type: missing  input: {'price': 'free'}
('price',) Input should be a valid integer, unable to parse string as an integer
  type: int_parsing  input: free
```

`msg` is for people, `type` is a short code for programs. Reporting everything at once lets the sender fix it in one go.

### 5. From JSON text or a dictionary

```bash
uv run python from_json.py
```

```
title='Pydantic' price=999
Input should be a valid integer, got a number with a fractional part
```

`999.0` would be accepted, but `999.5` would lose half a rupee, so it is refused.

### 6. Rules with Field

```python
class Course(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    price: int = Field(gt=0, le=100000)
```

```bash
uv run python rules.py
```

```
title -> String should have at least 3 characters
price -> Input should be greater than 0
```

Also available: `ge`, `lt` and many more.

### 7. Enums and defaults

```bash
uv run python level_run.py
uv run python defaults.py
```

```
title='Python' price=1499 level=<Level.BEGINNER: 'beginner'>
title='Python' price=1499 level=<Level.ADVANCED: 'advanced'>
Input should be 'beginner' or 'advanced'
```

```
['new'] []
None
```

The text `"advanced"` became the real `Level.ADVANCED` member, and `"expert"` is refused with the allowed values listed. A list default is copied for every object, so the shared-default trap from Module 4 is gone and no `default_factory` is needed.

### 8. Models inside models

`catalog.py` has `Instructor`, `Lesson` (`minutes` must be greater than 0) and `Course`, which uses them as types: `instructor: Instructor` and `lessons: list[Lesson] = []`.

```bash
uv run python nested_run.py
```

```
lessons.1.minutes -> Input should be a valid integer, unable to parse string as an integer
```

The location reads: field `lessons`, item number 1 (counting from 0), field `minutes`. You wrote no loops and no checks for the inner dictionaries.

### 9. A model as the request body

```python
class CourseIn(BaseModel):
    title: str = Field(min_length=3, max_length=60)
    price: int = Field(gt=0)


@app.post("/courses", status_code=201)
def add_course(course: CourseIn):
    courses.append(course)
    return course
```

```bash
uv run python -m uvicorn app_models:app --port 8153 --log-level warning
```

In a second terminal:

```bash
uv run python send_models.py
```

```
422
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "body",
        "price"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "free"
    }
  ]
}
```

Your function never ran, and you wrote no checking code. Stop the server.

### 10. Models going out

```bash
uv run python dump.py
```

```
{'title': 'Python', 'price': 1499, 'level': <Level.ADVANCED: 'advanced'>}
{'title': 'Python', 'price': 1499, 'level': 'advanced'}
{"title":"Python","price":1499,"level":"advanced"}
{'title': 'Python', 'level': 'advanced'}
```

`mode="json"` turns the enum member into plain text, so it can be written as JSON. `exclude` leaves chosen fields out.

### 11. Different shapes in and out

`students.py` has `StudentIn` (name, email, password) and `StudentOut` (id, name, email only). `app_out.py` takes the first and names the second as `response_model`; the function returns too much on purpose:

```python
@app.post("/students", status_code=201, response_model=StudentOut)
def join(student: StudentIn):
    return {"id": 1, **student.model_dump()}
```

```bash
uv run python -m uvicorn app_out:app --port 8153 --log-level warning
```

```bash
uv run python send_out.py
```

```
201 {'id': 1, 'name': 'Lukas', 'email': 'lukas@example.com'}
```

No password. (The password in the demo is a made-up value. Real apps never store plain passwords: Module 17.) Stop the server.

### 12. Settings from the environment

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ALLCS_")

    app_name: str = "allcsvideos"
    page_size: int = 20
    debug: bool = False
    secret_key: SecretStr
```

```bash
ALLCS_SECRET_KEY=demo-secret ALLCS_PAGE_SIZE=50 ALLCS_DEBUG=yes uv run python settings.py
```

```
allcsvideos 50 True
**********
```

The word `yes` became `True`, `50` became a number, and the secret prints as stars so it cannot leak into a log. (`demo-secret` is a demo value.) Now two bad starts:

```bash
ALLCS_SECRET_KEY=demo-secret ALLCS_PAGE_SIZE=many uv run python settings.py
uv run python settings.py
```

Both stop at once with a long traceback. Its last lines (the paths in the middle of yours will differ):

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
page_size
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='many', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/int_parsing
```

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
secret_key
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/missing
```

A wrong setting is caught at start-up, not at 3 a.m. when the first customer arrives.

## Common mistakes

1. Changing a field later is not checked.

   ```bash
   uv run python assign.py
   uv run python assign_fix.py
   ```

   ```
   free
   freefree
   ```

   ```
   Input should be a valid integer, unable to parse string as an integer
   1499
   ```

   Pydantic checks when the object is created. Add `model_config = ConfigDict(validate_assignment=True)` (as in `assign_fix.py`) and the bad value is refused and the price stays 1499.
2. Extra data is ignored. `extra.py` sends `sale_prise` (a typo):

   ```
   title='Python' sale_price=None
   Extra inputs are not permitted
   ```

   The loose model silently drops the typo; the strict one (`extra="forbid"`) raises an error you can see.
3. Forgetting the response model. Run `app_leak.py` (it returns the input model, with no `response_model`) and send the same request with `send_out.py`:

   ```bash
   uv run python -m uvicorn app_leak:app --port 8153 --log-level warning
   ```

   ```
   201 {'name': 'Lukas', 'email': 'lukas@example.com', 'password': 's3cret-demo'}
   ```

   The password comes back and nothing warns you. Always write a separate output model and name it as `response_model`.
4. A model is not a dictionary. `uv run python not_dict.py` fails at `course["title"]`:

   ```
   TypeError: 'Course' object is not subscriptable
   ```

   Read fields with a dot (`course.title`), or ask for a dictionary with `model_dump()`.

## Clean up

Stop any server that is still running (Control C). Nothing else was created.

## Next

[M15-L04 · Errors Done Right](../m15-l04-errors-done-right/)
