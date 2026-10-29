# M17-L03 · Authorisation and the OWASP API Top 10

> Video: Module 17, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- The difference between authentication (who are you) and authorisation (what may you do)
- Roles (`student`, `instructor`, `admin`) and a `require_role` dependency that guards routes
- Broken object level authorisation (BOLA): why changing `/students/1/...` to `/students/2/...` must fail, and the two-line fix
- When to answer 401, 403 and 404
- Mass assignment: how one extra field in the sign-up model made a stranger an admin, and the fix with separate input models and `extra="forbid"`
- A short tour of the OWASP API Security Top 10 (2023), and tests that keep the fixes in place

## Before you start

- Python 3.14 or newer (`python --version`) and Docker running.
- The backend continues from lesson 2 (login and tokens). This lesson's folders hold the whole project, so you do not need the earlier folder.
- All passwords and secrets here are demo values (for example `lukas-demo-pass`).

Start Postgres 17 (pinned image, demo password) and install the packages:

```bash
docker run -d --name pyrepo-m17-l03-pg -e POSTGRES_PASSWORD=devpass -e POSTGRES_DB=allcs -p 17403:5432 postgres:17.11
docker exec pyrepo-m17-l03-pg psql -U postgres -c "create database allcs_test"
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install "fastapi[standard]==0.162.0" sqlalchemy==2.1.6 "psycopg[binary]==3.3.6" alembic==1.20.1 argon2-cffi==25.1.0 pyjwt==2.15.1 httpx pytest==9.1.1
export JWT_SECRET=demo-only-not-a-real-secret-4f2a
```

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/` | The backend AFTER the fixes: `app/permissions.py` (`require_role`), `app/routers/admin.py`, the ownership check in `routers/students.py`, `extra="forbid"` in `schemas.py`, the migration `2814c3ac1b9d_student_roles.py`, tests |
| `allcs_bug/` | The same backend BEFORE the fixes (no role guard, no ownership check, sign-up accepts a `role`), with the new tests copied in so you can watch them fail |
| `seed.py` | Resets the database to Lukas, Priya (students), Meera (instructor), Asha (admin) and four courses |
| `files/client.py` | A tiny `login(email, password)` helper that returns the `Authorization` header |
| `files/hook.py` | Lukas reads two students' enrollments |
| `files/roles.py` | Lukas, Meera and Asha each try to create a course |
| `files/peek.py` | Lukas asks for students 1, 2 and 999 |
| `files/codes.py` | The three status codes 401, 403, 404 side by side |
| `files/limits.py` | Asking for 1000 courses in one request |
| `files/mass.py` | The mass assignment attack: sign up with `"role": "admin"` |

## Follow along

### 1. Add the role column

The migration was written by `alembic revision --autogenerate -m "student roles"` (it printed `Detected added column 'students.role'`). Apply it and load the demo data. Run the first from `allcs/`, the second from this folder:

```bash
cd allcs
alembic upgrade head
cd ..
python seed.py
```

```
INFO  [alembic.runtime.migration] Running upgrade 1063bd8736a4 -> 2814c3ac1b9d, student roles
seeded
```

The column is `role`, a short string with the default `student`, so existing students all become students.

### 2. See the bugs: run the app BEFORE the fixes

Start the old app in one terminal (`allcs_bug` folder), and run the scripts from `files/` in another:

```bash
cd allcs_bug
uvicorn app.main:app --port 8173
```

```bash
cd files
python hook.py
python roles.py
```

```
1 200 ['Python Basics', 'SQL in Two Weeks']
2 200 ['SQL in Two Weeks', 'Docker for Developers']
lukas student 201
meera instructor 201
asha admin 201
```

Lukas (logged in as himself) read Priya's enrollments just by changing the number, and a student created a course. The server knew who Lukas was and never asked whether he may do that.

### 3. See mass assignment

Reset the data (`python seed.py` from the lesson folder), then:

```bash
python mass.py
```

```
sign up 201 role admin
admin list 200 5 students
```

A stranger became an admin with two requests. Stop the old server (Ctrl+C).

### 4. The fixes

Read these files in `allcs/`:

- `app/permissions.py`: `require_role(*allowed)` returns a dependency that depends on `get_current_user` and raises `HTTPException(403, "Your role may not do this")` if the role is not allowed.
- `app/routers/courses.py`: `teacher = Depends(require_role("instructor", "admin"))` is listed under `dependencies=` on create, update, delete and add-lesson. Reading courses stays open.
- `app/routers/admin.py`: the whole router has `dependencies=[Depends(require_role("admin"))]`, so a new admin route cannot be forgotten.
- `app/routers/students.py`: two lines at the top of `list_enrollments`: if the caller is not that student and not an admin, raise `NotFound`.
- `app/schemas.py`: `SignUp` has only name, email and password, with `model_config = ConfigDict(extra="forbid")`. `NewUser` adds `role`, and only the admin route uses it.

Reset the data, start the FIXED app and run the scripts again:

```bash
cd ../allcs
uvicorn app.main:app --port 8173
```

```bash
cd ../files
python peek.py
python roles.py
```

```
1 200 ['Python Basics', 'SQL in Two Weeks']
2 404 Student 2 not found
999 404 Student 999 not found
lukas student 403
meera instructor 201
asha admin 201
```

Priya's list and a student that does not exist give the same 404 in the same words, so Lukas cannot tell which ids exist.

### 5. 401, 403 and 404

```bash
cd ..
python seed.py
cd files
python codes.py
```

```
401 no token Not authenticated
403 new course Your role may not do this
404 Priya's list Student 2 not found
```

- 401: I do not know who you are (no token, bad token, expired).
- 403: I know who you are and you may not do this.
- 404: for private objects, say "not found" rather than "forbidden", because 403 would confirm the object exists.

### 6. Limits (OWASP number 4)

```bash
python limits.py
```

```
422 Input should be less than or equal to 50
```

The course list has a maximum `limit` of 50, so one request cannot ask the database for everything.

### 7. Mass assignment, fixed

```bash
cd ..
python seed.py
cd files
python mass.py
```

```
sign up 422 Extra inputs are not permitted
```

The route code did not change. The danger lived in the model. Without `extra="forbid"` the extra `role` would be silently ignored, which is also safe, but a loud error shows you an attack is going on. Stop the server (Ctrl+C).

### 8. Tests: they must be able to fail

First the new tests against the OLD code:

```bash
cd ../allcs_bug
pytest -rf --tb=no tests/test_authz.py tests/test_signup.py
```

```
FAILED tests/test_authz.py::test_student_cannot_read_anothers_enrollments
FAILED tests/test_authz.py::test_student_cannot_create_a_course
FAILED tests/test_signup.py::test_sign_up_cannot_choose_a_role
3 failed, 3 passed
```

(The video shows the two files separately: 2 failed, 3 passed, and then 1 failed.) Now the same tests against the fixed code:

```bash
cd ../allcs
pytest -v
```

```
tests/test_authz.py::test_student_cannot_read_anothers_enrollments PASSED
tests/test_authz.py::test_student_reads_own_enrollments PASSED
tests/test_authz.py::test_admin_reads_any_enrollments PASSED
tests/test_authz.py::test_student_cannot_create_a_course PASSED
tests/test_authz.py::test_no_token_means_401 PASSED
tests/test_signup.py::test_sign_up_cannot_choose_a_role PASSED

6 passed
```

(You may see a few warnings after the summary; the pass count is what matters. Timings differ.)

### 9. The OWASP API Top 10 (2023), in one line each

1. Broken object level authorisation: today's bug.
2. Broken authentication: weak login, no attempt limits (lessons 1 and 2).
3. Broken object property level authorisation: mass assignment, today's second bug.
4. Unrestricted resource consumption: limits on size, count and speed.
5. Broken function level authorisation: roles on functions.
6. Unrestricted access to sensitive business flows: scripts that enrol thousands of fake students.
7. Server side request forgery.
8. Security misconfiguration.
9. Improper inventory management: forgotten old endpoints.
10. Unsafe consumption of other APIs.

Five questions for every endpoint: who may call it, which object, which fields, how much, how often.

## Common mistakes

- Hiding a button in the web page and calling that a rule. Every rule lives on the server.
- Checking only the GET route. Check every method and every route that takes an id, and test each.
- Putting the role inside the token. A token stays valid until it expires, so a demoted admin would keep power.
- Copying all fields of an input model into the database (`**data.model_dump()`) when the model has fields the client should not set. Use separate models and `extra="forbid"`.
- Using 403 for private objects: it confirms the object exists.
- Good habit: a route like `/me/enrollments` takes the id from the token, so there is no number to change.

## Clean up

```bash
docker rm -f -v pyrepo-m17-l03-pg
rm -rf .venv
```

## Next

[M17-L04 · Input Attacks and Secrets](../m17-l04-input-attacks-and-secrets/README.md)
