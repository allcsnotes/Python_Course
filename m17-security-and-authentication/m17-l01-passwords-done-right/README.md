# M17-L01 · Passwords Done Right

> Video: Module 17, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- Why a password must never be stored as typed, and what a hash is
- Why a plain fast hash (SHA-256) is not enough, and what a salt does
- How to use Argon2 in Python (`argon2-cffi`): `hash`, `verify`, `check_needs_rehash`
- How to add a `password_hash` column to the allcsvideos backend with an Alembic migration
- How to keep secrets out of responses, logs and git

## Before you start

- Python 3.14 or newer. Check with `python --version`.
- Docker running. The backend from Module 16 uses Postgres; here it runs in a container on port 17401.
- This lesson continues the allcsvideos backend (Module 16, build lesson 9). The folder `allcs/` already contains the finished project for this lesson, so you do not need the earlier folder.
- All passwords and keys in this lesson are demo values. Never reuse them.

Start Postgres 17 once (Docker image pinned, demo password):

```bash
docker run -d --name pyrepo-m17-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 17401:5432 postgres:17.11
docker exec pyrepo-m17-pg psql -U allcs -c "create database allcs_test"
```

Make a virtual environment and install the packages (versions as in the video):

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install argon2-cffi==25.1.0 "fastapi[standard]==0.162.0" "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1 pytest==9.1.1
```

(In the video this is `uv add argon2-cffi`, `uv sync` and `uv run ...` inside `allcs/`; plain `pip` gives the same result.)

## Files in this folder

| File | What it is |
|------|------------|
| `files/plain.py` | Reads a throwaway table that stores passwords as typed |
| `files/fast_hash.py`, `files/fp.py` | A SHA-256 `fingerprint` function (`fp.py` is the same function as a module) |
| `files/crack.py` | A dictionary attack on three stolen hashes |
| `files/speed.py`, `files/clock.py`, `files/timing.py` | Timing: SHA-256 against Argon2 |
| `files/salt.py` | Salted SHA-256 with `secrets.token_hex` |
| `files/argon.py`, `files/wrong.py`, `files/rehash.py` | Argon2: hashing, verify (True or raise), `check_needs_rehash` |
| `files/log_leak.py`, `files/log_fixed.py` | Pitfall 1: a password in a log line, and the `repr=False` fix |
| `files/leaky.py`, `files/sample.py` | Pitfall 2: a response model that leaks the hash |
| `files/secret.py` | Reads `SECRET_KEY` from the environment |
| `gitdemo/` | A `.gitignore`, a demo `.env` and `app.py` for the git ignore demo |
| `allcs/` | The backend at the end of the lesson: `app/security.py`, the migration `24530b3dbf92_student_password_hash.py`, `SignUp` in `schemas.py`, the sign-up route, `tests/test_passwords.py` |

## Follow along

### 1. The obvious (bad) idea: a plain password column

Create a throwaway table with three students, passwords saved exactly as typed:

```bash
docker exec pyrepo-m17-pg psql -U allcs -c "create table students_plain (name text, email text, password text); insert into students_plain values ('Lukas', 'lukas@example.com', 'password123'), ('Priya', 'priya@example.com', 'password123'), ('Meera', 'meera@example.com', 'Monsoon-Chai-Lamp-84')"
cd files
python plain.py
```

```
the table a thief copies tonight:
('Lukas', 'lukas@example.com', 'password123')
('Priya', 'priya@example.com', 'password123')
('Meera', 'meera@example.com', 'Monsoon-Chai-Lamp-84')
```

A thief who copies this table can log in as everybody, and Lukas and Priya share a password.

### 2. A hash is a one-way fingerprint

```bash
python fast_hash.py
```

```
ef92b778bafe771e89245b89ecbc08a4
ef92b778bafe771e89245b89ecbc08a4
008c70392e3abfbd0fa47bbc2ed96aa9
```

The same word always gives the same fingerprint, and one capital letter changes it completely. (This is a password hash, not the hash that Python dictionaries use for lookups, Module 8.)

### 3. A fast hash can be guessed

```bash
python crack.py
python speed.py
```

```
Lukas password123
Priya password123
Meera not found
one million guesses: 0.62 seconds
guesses per second: 1,608,459
```

A weak password is found with one dictionary lookup, a strong one is not. The speed line depends on your computer, yours will differ. SHA-256 was made to be fast, which is the wrong goal for passwords.

### 4. A salt makes every hash different

```bash
python salt.py
```

```
Lukas e479b6ccd9984bda c0077124ededc38f...
Priya eab8620f1ee9311d f17ba6e4bb0677bc...
```

The salt is random each run, so yours will differ. Same password, different salt, different hash. The salt is not secret: you store it next to the hash.

### 5. Argon2: salted, slow and memory hungry

```bash
python argon.py
```

```
$argon2id$v=19$m=65536,t=3,p=4$Fe9hdYRLgCK6o0AKLtM...
$argon2id$v=19$m=65536,t=3,p=4$Wn2uhFg2cxRZsr3zLlp...
same? False
['argon2id', 'v=19', 'm=65536,t=3,p=4']
True
```

The salt part is random, yours will differ. One string holds the algorithm (`argon2id`), the version, the settings (64 MB of memory, 3 passes, 4 lanes) and the salt, so the database needs just one column.

### 6. verify answers True or raises

```bash
python wrong.py
```

```
True
Traceback (most recent call last):
  ...
argon2.exceptions.VerifyMismatchError: The password does not match the supplied hash
```

The `print("done")` line never runs. That is why `app/security.py` wraps `verify` in a function that catches the error and returns `False`.

### 7. The price of slow

```bash
python timing.py
```

```
sha256: 0.2 microseconds
argon2: 54.3 milliseconds
1,000,000 guesses: 15.1 hours
```

Timings depend on your machine, yours will differ. The shape stays the same: Argon2 is hundreds of thousands of times slower per guess, and a student logging in barely notices 50 ms.

### 8. Old hashes and `check_needs_rehash`

```bash
python rehash.py
```

```
m=8192,t=1,p=4
True
m=65536,t=3,p=4
False
```

You can only upgrade a hash at login, the one moment you hold the real password: verify, then if `needs_rehash` is True, hash again and save.

### 9. Add it to the backend

The code is already in `allcs/`. Read `allcs/app/security.py` (three small functions: `hash_password`, `verify_password`, `needs_rehash`), then the new line in `allcs/app/models.py` (`password_hash`, a nullable string) and `SignUp` in `allcs/app/schemas.py` (10 to 128 characters). The route in `allcs/app/routers/students.py` builds the student with the hash and returns `StudentOut`, which has no password and no hash.

To reproduce the video exactly (Priya exists from version 1, before the migration):

```bash
cd ../allcs
alembic downgrade base
alembic upgrade 6d1d3956ce21
docker exec pyrepo-m17-pg psql -U allcs -c "insert into students (name,email) values ('Priya','priya@example.com')"
alembic upgrade head
```

The last command prints:

```
INFO  [alembic.runtime.migration] Running upgrade 6d1d3956ce21 -> 24530b3dbf92, student password hash
```

The migration `migrations/versions/24530b3dbf92_student_password_hash.py` was written by `alembic revision --autogenerate -m "student password hash"` ("Detected added column 'students.password_hash'"). The column is `nullable=True` because Priya already has a row and no password yet.

### 10. Try it with curl

```bash
uvicorn app.main:app --port 8171
```

In a second terminal:

```bash
curl -s -i --json '{"name": "Lukas", "email": "lukas@example.com", "password": "Monsoon-Chai-Lamp-84"}' localhost:8171/students
```

```
HTTP/1.1 201 Created
content-length: 64
content-type: application/json

{"name":"Lukas","email":"lukas@example.com","id":2,"courses":[]}
```

(The `date` header is also printed.) No password and no hash in the answer. A too short password:

```bash
curl -s -i --json '{"name": "Lukas", "email": "lukas2@example.com", "password": "short"}' localhost:8171/students
```

```
HTTP/1.1 422 Unprocessable Content
content-length: 144
content-type: application/json

{"error":{"code":"invalid_input","message":"Wrong input","fields":[{"field":"password","problem":"String should have at least 10 characters"}]}}
```

Look inside the database:

```bash
docker exec pyrepo-m17-pg psql -U allcs -c "select id, name, left(password_hash, 40) as hash from students order by id"
```

```
 id | name  |                   hash                   
----+-------+------------------------------------------
  1 | Priya | 
  2 | Lukas | $argon2id$v=19$m=65536,t=3,p=4$uflI+L9Nz
(2 rows)
```

Priya's hash is empty. Lukas has an Argon2 hash (the salt part differs for you). Stop the server with Ctrl+C.

### 11. Run the tests

```bash
pytest -q
```

```
.................                                                        [100%]
17 passed in 1.00s
```

The five new tests are in `tests/test_passwords.py`: the response has no password, the database row starts with `$argon2id$` and does not contain the password, `verify_password` works, and the two length limits return 422. (The tests use the database `allcs_test` on the same Postgres container.)

### 12. Secrets stay out of code and git

```bash
cd ../files
python secret.py
SECRET_KEY=demo-not-a-real-key python secret.py
```

```
KeyError: 'SECRET_KEY'
key loaded, length 19
```

The first run fails on purpose: no key, no start. On your laptop the key lives in a file named `.env` that git must skip:

```bash
cd ../gitdemo
git init -q
git check-ignore -v .env
git status --short
```

```
.gitignore:1:.env	.env
?? .gitignore
?? app.py
```

`.env` is ignored. (Delete the `.git` folder afterwards, see Clean up.)

### 13. Pitfall 1: a password in the log

```bash
cd ../files
python log_leak.py
python log_fixed.py
```

```
new sign up: name='Lukas' password='Monsoon-Chai-Lamp-84'
new sign up: name='Lukas'
```

Logging a whole model leaks the password. `Field(repr=False)` hides it from the printed form.

### 14. Pitfall 2: the response

```bash
python leaky.py
```

```
{'id': 2, 'name': 'Lukas', 'email': 'lukas@example.com', 'password_hash': '$argon2id$v=19$m=65536,t=3,p=4$8f8OjBolw3...'}
```

(The hash differs for you.) A hash in a response lets a thief guess offline, so `StudentOut` has no such field, and a test checks it.

## Common mistakes

- Storing the password as typed, or with a plain SHA-256. Use Argon2.
- Forgetting that `verify` raises on a wrong password. Wrap it once (`verify_password`).
- Making `password_hash` a required column when old rows exist. Use `nullable=True`.
- Logging a whole model that holds a password. Use `repr=False`.
- Returning the hash in a response. Use a response model without it.
- Committing `.env`. Put it in `.gitignore`.
- No maximum length: hashing a huge password would cost time, so the limit is 128 characters.

## Clean up

```bash
rm -rf ../gitdemo/.git ../.venv
docker rm -f -v pyrepo-m17-pg
```

(Keep the container if you continue with the next lesson.)

## Next

[M17-L02 · Sessions, JWT and OAuth2](../m17-l02-sessions-jwt-and-oauth2/README.md)
