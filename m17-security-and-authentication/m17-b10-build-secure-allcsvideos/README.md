# M17-B10 · Build Secure allcsvideos

> Video: Module 17, Build 10. Watch it first, then follow along here.

## What you'll build

The allcsvideos backend from build 9 (Module 16), now secured with everything from lessons 1 to 4:

- Sign up with an Argon2-hashed password, login with a short access token and a refresh token, refresh and logout
- Roles (student, instructor, admin) and ownership (a course belongs to its instructor)
- Input models that refuse fields a client must not set, and a log of failed logins that never holds a password
- 24 tests, one for each rule

The seven rules (each one is a test): a password is never stored, only its hash; login gives a short access token and a refresh token; logout cancels the refresh token; only instructors and admins create courses; only the owner of a course changes it; a client can never set a role or an owner; a failed login goes into the log, without the password.

## Before you start

- Python 3.14 or newer (`python --version`), Docker running.
- The project of build 9 is the starting point. This folder already holds the finished project (`allcs/`), and the steps below show what each step adds.
- Every password, key and email here is a demo value.

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/app/security.py` | `hash_password`, `verify_password` (returns False on a mismatch), `needs_rehash`, a dummy hash |
| `allcs/app/tokens.py` | `make_access_token` and `read_access_token`; the secret comes from the `SECRET_KEY` environment variable |
| `allcs/app/deps.py` | `get_current_user`: reads the token, loads the student on every request |
| `allcs/app/permissions.py` | `require_role`, `own_student`, `own_course` |
| `allcs/app/routers/auth.py` | `/auth/login`, `/auth/refresh`, `/auth/logout`, the failed-login counter and log lines |
| `allcs/app/routers/admin.py` | Admin-only routes (creating instructors) |
| `allcs/app/routers/courses.py`, `enrollments.py`, `students.py` | The build 9 routes, now guarded |
| `allcs/app/models.py`, `schemas.py`, `errors.py`, `main.py`, `db.py`, `domain.py` | Models (`password_hash`, `role`, `owner_id`, `RefreshToken`), input and output models with `extra="forbid"`, error shapes, `/me` |
| `allcs/migrations/versions/f149f9b699de_passwords_roles_owners.py` | Adds password hash, role and course owner |
| `allcs/migrations/versions/d1a467cf69aa_refresh_tokens.py` | Adds the `refresh_tokens` table |
| `allcs/make_admin.py` | Creates the first admin (Asha) from a script on the server, never through the API |
| `allcs/get_token.py` | Small helper: logs in and prints one field of the answer |
| `allcs/tests/` | `conftest.py` and two test files (13 + 11 tests) |
| `allcs/pyproject.toml`, `allcs/uv.lock` | Dependencies (added with `uv add argon2-cffi pyjwt`) |

## Run it

```bash
docker run -d --name pyrepo-m17-b10-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 17410:5432 postgres:17.11
cd allcs
uv sync                                  # or: python -m venv .venv, source .venv/bin/activate, pip install -e . pytest
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
uv run alembic upgrade head
uv run python make_admin.py
uv run fastapi dev app/main.py --port 8680
```

(With pip instead of uv, drop `uv run`. The `pyproject.toml` lists the exact packages: alembic, argon2-cffi, fastapi[standard], psycopg[binary], pyjwt, sqlalchemy, and pytest for tests.)

Expected:

```
admin created: asha@example.com
```

Now two requests to delete Python Basics (after you have created a course and a student, see below): with no token you get `401`, and with a student token you get `403`:

```bash
curl -s -i -X DELETE localhost:8680/courses/1
curl -s -i -H "Authorization: Bearer $LUKAS" -X DELETE localhost:8680/courses/1
```

```
{"error":{"code":"not_authenticated","message":"Not authenticated"}}
{"error":{"code":"forbidden","message":"Your role may not do this"}}
```

(The headers `HTTP/1.1 401 Unauthorized` and `HTTP/1.1 403 Forbidden` are printed first, with a `date` header.)

## Build it step by step

The video builds the project in six steps. Every command is run from `allcs/`, with the server running on port 8680 in another terminal.

### Setup: the project of build 9, plus two packages

```bash
uv add argon2-cffi pyjwt
```

```
 + argon2-cffi==25.1.0
 + pyjwt==2.15.1
```

Start the database, build the two old migrations, and add the data of "version 1": three courses and one student, Priya, who has no password.

```bash
docker run -d --name pyrepo-m17-b10-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 17410:5432 postgres:17.11
uv run alembic upgrade 6d1d3956ce21        # the two old migrations (courses and lessons, students and enrollments)
docker exec pyrepo-m17-b10-pg psql -U allcs -c "insert into courses (title, price, level) values ('Python Basics', 499, 'beginner'), ('SQL in Two Weeks', 599, 'beginner'), ('Git and GitHub', 299, 'beginner')"
docker exec pyrepo-m17-b10-pg psql -U allcs -c "insert into students (name, email) values ('Priya', 'priya@example.com')"
```

```
INSERT 0 3
INSERT 0 1
```

(In the finished folder the next migrations already exist, so `alembic upgrade head` later applies them. To see Alembic write them yourself, move `f149f9b699de_...` and `d1a467cf69aa_...` out of `migrations/versions/` and run `alembic revision --autogenerate -m "..."` at steps 1 and 3.)

The secret key that signs tokens is never in the code. Create it before you start the server:

```bash
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
```

### Step 1: passwords and sign up

Files: `models.py` (Student gets `password_hash`, nullable, and `role` with the default `student`; Course gets `owner_id`, a foreign key), `security.py`, `schemas.py` (`SignUp` with a 10 to 128 character password, `repr=False`; `StudentOut` with `role`, never a password), `routers/students.py`.

The migration `f149f9b699de_passwords_roles_owners.py` adds three columns and one foreign key. Apply it and look at the table:

```bash
uv run alembic upgrade head
docker exec pyrepo-m17-b10-pg psql -U allcs -c "\d students"
```

```
                                       Table "public.students"
    Column     |          Type          | Collation | Nullable |               Default                
---------------+------------------------+-----------+----------+--------------------------------------
 id            | integer                |           | not null | nextval('students_id_seq'::regclass)
 name          | character varying(60)  |           | not null | 
 email         | character varying(120) |           | not null | 
 password_hash | character varying(255) |           |          | 
 role          | character varying(12)  |           | not null | 'student'::character varying
Indexes:
    "students_pkey" PRIMARY KEY, btree (id)
    "students_email_key" UNIQUE CONSTRAINT, btree (email)
Referenced by:
    TABLE "courses" CONSTRAINT "courses_owner_id_fkey" FOREIGN KEY (owner_id) REFERENCES students(id)
    TABLE "enrollments" CONSTRAINT "enrollments_student_id_fkey" FOREIGN KEY (student_id) REFERENCES students(id)
```

Start the server (`uv run fastapi dev app/main.py --port 8680`) and sign up:

```bash
curl -s -i --json '{"name": "Lukas", "email": "lukas@example.com", "password": "lukas-demo-pw"}' localhost:8680/students
curl -s -i --json '{"name": "Asha", "email": "asha@example.com", "password": "short"}' localhost:8680/students
docker exec pyrepo-m17-b10-pg psql -U allcs -c "select id, email, role, left(password_hash, 31) as hash from students order by id"
```

```
HTTP/1.1 201 Created
{"name":"Lukas","email":"lukas@example.com","id":2,"role":"student","courses":[]}
HTTP/1.1 422 Unprocessable Content
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"password","problem":"String should have at least 10 characters"}]}}
 id |       email       |  role   |              hash               
----+-------------------+---------+---------------------------------
  1 | priya@example.com | student | 
  2 | lukas@example.com | student | $argon2id$v=19$m=65536,t=3,p=4$
(2 rows)
```

Priya has an empty hash and Lukas has an Argon2 hash. No password is stored. Who is the first admin? Sign up always makes a student, so the first admin is made by a script that runs on the server:

```bash
uv run python make_admin.py
```

```
admin created: asha@example.com
```

Asha is student 3, role `admin` (password `asha-demo-pw`, a demo value).

### Step 2: login and the access token

Files: `tokens.py` (payload: `sub` as text, `iat`, `exp` 15 minutes later; a missing `SECRET_KEY` stops the app at start-up), `deps.py` (`get_current_user`), `errors.py` (every `HTTPException` becomes `{"error": {"code", "message"}}`, and 401 keeps `www-authenticate: Bearer`), `routers/auth.py` (login, which verifies against a dummy hash even when the email is unknown so the time stays about the same), `/me` in `main.py`.

```bash
curl -s -i -X POST localhost:8680/auth/login -d "username=lukas@example.com&password=lukas-demo-pw"
curl -s -i -X POST localhost:8680/auth/login -d "username=lukas@example.com&password=lukas-demo-PW"
curl -s -i -X POST localhost:8680/auth/login -d "username=nobody@example.com&password=whatever-1"
```

```
HTTP/1.1 200 OK
{"access_token":"eyJhbGciOi...
HTTP/1.1 401 Unauthorized
{"error":{"code":"not_authenticated","message":"Wrong email or password"}}
HTTP/1.1 401 Unauthorized
{"error":{"code":"not_authenticated","message":"Wrong email or password"}}
```

(The token is long and differs for you.) A wrong password and an unknown email look the same, so a thief learns nothing. Put the token in `LUKAS`, then:

```bash
curl -s -i localhost:8680/me
curl -s -i -H "Authorization: Bearer $LUKAS" localhost:8680/me
curl -s -i -H "Authorization: Bearer ${LUKAS}x" localhost:8680/me
```

```
HTTP/1.1 401 Unauthorized
www-authenticate: Bearer
{"error":{"code":"not_authenticated","message":"Not authenticated"}}
HTTP/1.1 200 OK
{"name":"Lukas","email":"lukas@example.com","id":2,"role":"student","courses":[]}
HTTP/1.1 401 Unauthorized
{"error":{"code":"not_authenticated","message":"Invalid token"}}
```

### Step 3: refresh and logout

The refresh token is random text (not a JWT) and only its hash is stored, in the new table `refresh_tokens` (migration `d1a467cf69aa_refresh_tokens.py`). `issue_pair` makes both tokens. Refresh finds the row by hash, refuses a missing, revoked or expired token, marks it revoked and issues a new pair, so every refresh token works once.

```bash
uv run alembic upgrade head
curl -s -i --json '{"refresh_token": "'$REFRESH'"}' localhost:8680/auth/refresh    # 200, a new pair
curl -s -i --json '{"refresh_token": "'$REFRESH'"}' localhost:8680/auth/refresh    # the old token again: 401
curl -s -i --json '{"refresh_token": "'$REFRESH'"}' localhost:8680/auth/logout     # newest token: 204
curl -s -i --json '{"refresh_token": "'$REFRESH'"}' localhost:8680/auth/refresh    # after logout: 401
curl -s -i -H "Authorization: Bearer $LUKAS" localhost:8680/me                     # old access token: still 200
```

(Set `REFRESH` to the right token before each call, as in the video: login, refresh once, reuse the old one, log in again, logout with the newest, refresh after logout.) Results: `200`, `401 invalid refresh token`, `204 No Content`, `401`, and `200` for the old access token, because a JWT cannot be taken back; it lives at most 15 minutes. The table (hash starts and ids differ for you):

```bash
docker exec pyrepo-m17-b10-pg psql -U allcs -c "select id, student_id, left(token_hash, 10) as token_hash, revoked from refresh_tokens order by id"
```

```
 id | student_id | token_hash | revoked 
----+------------+------------+---------
  1 |          2 | fc89599848 | f
  2 |          2 | cf4169411d | f
  3 |          2 | ef9a931e4b | t
  4 |          2 | f2efc1cd71 | f
  5 |          2 | 3641f2d67f | t
(5 rows)
```

### Step 4: roles and ownership

Files: `permissions.py` (`require_role(*roles)` gives 403; `own_student` lets a person through to their own number or an admin, otherwise 404; `own_course` asks for instructor or admin first, then checks `owner_id`; a course nobody owns can only be changed by an admin), `routers/courses.py` (`teacher = Depends(require_role("instructor", "admin"))`; create saves `owner_id` from the token; replace, delete and add lesson use `own_course`), `routers/admin.py` (the whole router is behind `require_role("admin")`), `routers/enrollments.py` (the student comes from the token, not the request body).

Lukas tries the admin door, then Asha uses it (put Asha's token in `ASHA`):

```bash
curl -s -i -H "Authorization: Bearer $LUKAS" --json '{"name": "Meera", "email": "meera@example.com", "password": "meera-demo-pw", "role": "instructor"}' localhost:8680/admin/students
curl -s -i -H "Authorization: Bearer $ASHA" --json '{"name": "Meera", "email": "meera@example.com", "password": "meera-demo-pw", "role": "instructor"}' localhost:8680/admin/students
```

```
HTTP/1.1 403 Forbidden
{"error":{"code":"forbidden","message":"Your role may not do this"}}
HTTP/1.1 201 Created
{"name":"Meera","email":"meera@example.com","id":4,"role":"instructor","courses":[]}
```

The course rules, as five requests (log Meera in and put her token in `MEERA`):

```bash
curl -s -i -X DELETE localhost:8680/courses/1                                                                    # no token: 401
curl -s -i -H "Authorization: Bearer $LUKAS" --json '{"title": "Web Basics", "price": 399}' localhost:8680/courses  # student: 403
curl -s -i -H "Authorization: Bearer $MEERA" --json '{"title": "Web Basics", "price": 399}' localhost:8680/courses  # instructor: 201
curl -s -i -H "Authorization: Bearer $MEERA" --json '{"title": "Web Basics", "price": 449}' -X PUT localhost:8680/courses/4
curl -s -i -H "Authorization: Bearer $MEERA" --json '{"title": "Git and GitHub", "price": 349}' -X PUT localhost:8680/courses/3
curl -s -i -H "Authorization: Bearer $ASHA" --json '{"title": "Git and GitHub", "price": 349}' -X PUT localhost:8680/courses/3
```

```
401  Not authenticated
403  Your role may not do this
201  {"title":"Web Basics","price":399,"level":"beginner","id":4,"owner_id":4,"lessons":[]}
200  {"title":"Web Basics","price":449,"level":"beginner","id":4,"owner_id":4,"lessons":[]}
403  {"error":{"code":"forbidden","message":"This is not your course"}}
200  (Asha is an admin and may change a course nobody owns)
```

Enrolling and reading lists. Lukas names Priya (student 1) in the body, and the body is ignored:

```bash
curl -s -i -H "Authorization: Bearer $LUKAS" --json '{"student_id": 1}' localhost:8680/courses/2/enrollments
curl -s -i -H "Authorization: Bearer $LUKAS" localhost:8680/students/1/enrollments
curl -s -i -H "Authorization: Bearer $LUKAS" localhost:8680/students/999/enrollments
curl -s -H "Authorization: Bearer $ASHA" localhost:8680/students/1/enrollments
```

```
HTTP/1.1 201 Created
{"student_id":2,"course_id":2,"enrolled_on":"2026-10-27"}
HTTP/1.1 404 Not Found
{"error":{"code":"not_found","message":"Student 1 not found"}}
HTTP/1.1 404 Not Found
(the same shape, "Student 999 not found")
[]
```

(`enrolled_on` is today's date for you.) The enrollment is Lukas's (student 2). Priya's list and a student that does not exist look the same to Lukas, and Asha, an admin, can read Priya's list.

### Step 5: input models and the log

`SignUp` and `CourseIn` get `model_config = ConfigDict(extra="forbid")`; `NewUser` extends `SignUp` with `role`, only for the admin route.

```bash
curl -s -i --json '{"name": "attacker", "email": "attacker@example.com", "password": "attacker-pw-1", "role": "admin"}' localhost:8680/students
curl -s -i -H "Authorization: Bearer $MEERA" --json '{"title": "Hacked Course", "price": 100, "owner_id": 1}' localhost:8680/courses
```

```
HTTP/1.1 422 Unprocessable Content
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"role","problem":"Extra inputs are not permitted"}]}}
HTTP/1.1 422 Unprocessable Content
{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"owner_id","problem":"Extra inputs are not permitted"}]}}
```

In `routers/auth.py`, `count_failure` keeps, for each email, the times of failures in the last minute. A failed login writes one warning, a good login clears the count. It is not a lock (rate limiting comes in Module 18); it gives you something to see and count. Three wrong passwords, then the real one:

```bash
for i in 1 2 3; do curl -s -o /dev/null -w "%{http_code}\n" -X POST localhost:8680/auth/login -d "username=lukas@example.com&password=guess$i"; done
curl -s -o /dev/null -w "%{http_code}\n" -X POST localhost:8680/auth/login -d "username=lukas@example.com&password=lukas-demo-pw"
```

```
401
401
401
200
```

The server terminal shows (the ports differ):

```
WARNING allcs.auth: login failed for lukas@example.com (1 in the last minute)
WARNING allcs.auth: login failed for lukas@example.com (2 in the last minute)
WARNING allcs.auth: login failed for lukas@example.com (3 in the last minute)
INFO allcs.auth: login ok for student 2
```

Not one password is in the log. (To see these lines, `main.py` sets the logging level to INFO.)

### Step 6: tests

`tests/conftest.py` sets `DATABASE_URL` (a test database) and a test `SECRET_KEY` before the app is imported, and adds the fixtures `make_user`, `login` and `headers`. Create the test database and run:

```bash
docker exec pyrepo-m17-b10-pg psql -U allcs -c "create database allcs_test"
uv run pytest -q
```

```
........................                                                                     [100%]
24 passed in 4.43s
```

(The time differs.) The 24 tests are named after the rules: `test_sign_up_never_returns_the_password_or_hash`, `test_the_password_is_stored_as_an_argon2_hash`, `test_the_same_email_twice_is_409`, `test_login_gives_both_tokens`, `test_wrong_password_and_unknown_email_look_the_same`, `test_an_old_student_without_a_password_cannot_log_in`, `test_login_upgrades_an_old_hash`, `test_no_token_is_401`, `test_a_changed_token_is_401`, `test_an_expired_token_is_401`, `test_a_refresh_token_is_not_an_access_token`, `test_refresh_gives_new_tokens_and_the_old_one_dies`, `test_logout_revokes_the_refresh_token` (file `test_accounts.py`), and in `test_access.py`: `test_a_student_cannot_create_a_course`, `test_an_instructor_creates_a_course_and_owns_it`, `test_instructors_edit_only_their_own_courses`, `test_deleting_needs_a_login`, `test_students_read_only_their_own_enrollments`, `test_enrolling_uses_the_token_not_the_body`, `test_only_an_admin_creates_instructors`, `test_signing_up_cannot_choose_a_role`, `test_a_course_cannot_be_given_an_owner`, `test_failed_logins_are_logged_without_the_password`, `test_courses_are_public_and_the_list_is_fast`.

In the video, the first run had one failure: the log test saw empty text, because Alembic's `env.py` calls `fileConfig(...)`, which by default switches off every existing logger, including ours. The fix is one argument, already in `migrations/env.py`: `fileConfig(config.config_file_name, disable_existing_loggers=False)`.

Do the tests really guard the rules? Remove the ownership check from `own_course` on purpose and run again:

```
..F.....................
FAILED tests/test_access.py::test_instructors_edit_only_their_own_courses - assert 200 == 403
1 failed, 23 passed
```

Put the two lines back and all 24 are green again.

## What is not here yet

HTTPS (so passwords never travel in plain text), rate limiting (Module 18, lesson 4), a password reset, real secret management (Module 19), and checking your libraries with `pip audit`.

## Common mistakes

- Starting the server without `SECRET_KEY`: the app refuses to start, on purpose.
- Putting the secret key in a file in git. Keep it in the environment (and `.env` in `.gitignore`).
- Making the first admin through the API. Use `make_admin.py` on the server.
- Taking the student's id from the request body or address when it belongs to the caller. Take it from the token.
- Forgetting `disable_existing_loggers=False` when Alembic runs inside tests.

## Clean up

```bash
docker rm -f -v pyrepo-m17-b10-pg
rm -rf .venv
```

## Next

[M18-L01 · Redis and Caching](../../m18-caching-background-jobs-and-messaging/m18-l01-redis-and-caching/README.md)
