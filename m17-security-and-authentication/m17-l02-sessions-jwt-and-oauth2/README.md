# M17-L02 · Sessions, JWT and OAuth2

> Video: Module 17, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- Why a server needs to know who is calling on every request, and the two ways to do it: a server session and a signed token (JWT)
- What a JWT really is: readable payload, signature, expiry. Signed does not mean secret
- How to build a login with FastAPI (`OAuth2PasswordRequestForm`, `OAuth2PasswordBearer`) and a `get_current_user` dependency
- Short access tokens plus revocable refresh tokens, and what logout really does
- The "Sign in with Google" flow (OAuth2 code flow), shown with a local stand-in for Google
- Three JWT pitfalls: secrets in the payload, decoding without `algorithms`, a number as `sub`

## Before you start

- Python 3.14 or newer (`python --version`) and Docker running.
- The backend continues from the previous lesson (`../m17-l01-passwords-done-right/`). The folder `allcs/` here is the finished project for this lesson.
- Everything is local. The "Google" in this lesson is a small FastAPI app we wrote (`standin_google.py`), so no Google account, no credentials and no internet are used. All secrets are demo values.

Start Postgres (pinned image, demo password) and install the packages:

```bash
docker run -d --name pyrepo-m17-l02-pg -e POSTGRES_USER=allcs -e POSTGRES_PASSWORD=allcs -e POSTGRES_DB=allcs -p 17402:5432 postgres:17.11
docker exec pyrepo-m17-l02-pg psql -U allcs -c "create database allcs_test"
cd allcs
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pyjwt==2.15.1 cryptography httpx==0.28.1 argon2-cffi==25.1.0 "fastapi[standard]==0.162.0" "psycopg[binary]==3.3.6" sqlalchemy==2.1.6 alembic==1.20.1 pytest==9.1.1
export SECRET_KEY=demo-secret-not-for-real-use-0123456
export DATABASE_URL=postgresql+psycopg://allcs:allcs@localhost:17402/allcs
export GOOGLE_CLIENT_SECRET=standin-client-secret-not-real
```

(The video uses `uv add pyjwt` and `uv run`; `pip` gives the same result. `cryptography` is only needed for the stand-in Google, which signs with an RSA key.)

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/hook.py` | The broken idea: one global `current_user` |
| `allcs/session_demo.py` | A session with a cookie and a dictionary "notebook" |
| `allcs/jwt_parts.py`, `jwt_tamper.py`, `jwt_expiry.py` | Looking inside a JWT, forging one, expiring one |
| `allcs/app/tokens.py` | `make_access_token` (with a `now` parameter for tests) and `read_access_token` |
| `allcs/app/deps.py` | `get_current_user` dependency with `OAuth2PasswordBearer` |
| `allcs/app/auth.py` | `/auth/login`, `/auth/refresh`, `/auth/logout`, refresh tokens stored as hashes |
| `allcs/app/models.py` | Adds the `RefreshToken` model |
| `allcs/migrations/versions/70441325551c_refresh_tokens.py` | The migration Alembic generated for `refresh_tokens` |
| `allcs/app/google.py` | `/auth/google/login` and `/auth/google/callback` (state check, code swap, ID token check) |
| `allcs/standin_google.py` | LOCAL stand-in for Google (port 8272). Not real Google |
| `allcs/oauth_flow.py`, `peek_id_token.py` | A script that plays the browser, and one that prints the ID token claims |
| `allcs/pit_readable.py`, `pit_algorithms.py`, `pit_subject.py` | The three pitfalls |
| `allcs/seed_demo.py` | Seeds two courses and two students (Lukas, Priya) with demo passwords |
| `allcs/tests/test_auth.py` | Four auth tests with a frozen clock. (`tests/test_api.py` is the old API test file, now sending a password at sign up) |

## Follow along

### 1. The first idea: a global variable

```bash
python hook.py
```

```
{'you_are': 'Priya'}
```

Lukas logged in, then Priya logged in, and Lukas asks "who am I?" and gets Priya. One variable has room for one name.

### 2. Way one: a server session

```bash
python session_demo.py
```

```
sid=9baMQX_OsuujI5INmPFBUg; HttpOnly; Path=/; SameSite=lax
{'you_are': 'Lukas'}
401
```

The cookie value is random (yours will differ). Each person holds their own ticket. After `SESSIONS.clear()`, which imitates a server restart, Lukas gets 401: the notebook lived in memory.

### 3. Way two: a signed token (JWT)

```bash
python jwt_parts.py
python jwt_tamper.py
python jwt_expiry.py
```

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzkzMDk1MDE2fQ.-veUuBwsxUur5tB6kSU-P1_MYHlbg_7Zbi2Ujqrq7Bg
{'alg': 'HS256', 'typ': 'JWT'}
{'sub': '1', 'exp': 1793095016}
43 characters of signature
1
InvalidSignatureError - Signature verification failed
now: 1
ExpiredSignatureError - Signature has expired
```

The token and the `exp` number differ on your machine. Anyone can read the payload (base64 is not a lock). The signature stops anyone from changing it. Remember: signing says "nobody changed this", encrypting says "nobody can read this", and a JWT only does the first.

### 4. Set up the database and the backend

```bash
alembic upgrade head
python seed_demo.py
```

```
INFO  [alembic.runtime.migration] Running upgrade 6d1d3956ce21 -> 24530b3dbf92, student password hash
INFO  [alembic.runtime.migration] Running upgrade 24530b3dbf92 -> 70441325551c, refresh tokens
seeded
```

(`70441325551c_refresh_tokens.py` was produced in the video by `alembic revision --autogenerate -m "refresh tokens"`, which printed `Detected added table 'refresh_tokens'`.) Start the servers, each in its own terminal, with an access token life of 5 seconds so you can watch it expire:

```bash
uvicorn standin_google:app --port 8272 --log-level warning
ACCESS_SECONDS=5 uvicorn app.main:app --port 8172 --log-level warning
```

### 5. Log in and use the token

```bash
curl -s -i -d 'username=lukas@example.com&password=lukas-demo-password' localhost:8172/auth/login
```

```
HTTP/1.1 200 OK
content-type: application/json

{"access_token":"eyJhbGci...","refresh_token":"...","token_type":"bearer"}
```

(The tokens are long and differ for you; some headers like `date` are also printed.) Save the two tokens in `TOKEN` and `REFRESH` shell variables, then:

```bash
curl -s -i localhost:8172/me
curl -s -i localhost:8172/me -H "Authorization: Bearer $TOKEN"
curl -s -i localhost:8172/me -H "Authorization: Bearer not.a.token"
curl -s -i -d 'username=lukas@example.com&password=wrong-password' localhost:8172/auth/login
```

```
HTTP/1.1 401 Unauthorized
www-authenticate: Bearer
{"detail":"Not authenticated"}

HTTP/1.1 200 OK
{"name":"Lukas","email":"lukas@example.com","id":1,"courses":[{"id":1,"title":"Python Basics"}]}

HTTP/1.1 401 Unauthorized
{"detail":"Invalid token"}

HTTP/1.1 401 Unauthorized
{"detail":"Wrong email or password"}
```

The `/me` answer has no password and no hash.

### 6. Refresh, reuse, logout

Log in again to get a young pair, then use the refresh token once, try the OLD refresh token again, log out with the newest one, and try to refresh once more:

```bash
curl -s -i --json "{\"refresh_token\": \"$REFRESH\"}" localhost:8172/auth/refresh      # 200, a new pair
curl -s -i --json "{\"refresh_token\": \"$OLD\"}" localhost:8172/auth/refresh          # the old one
curl -s -i --json "{\"refresh_token\": \"$REFRESH\"}" localhost:8172/auth/logout       # newest one
curl -s -i --json "{\"refresh_token\": \"$REFRESH\"}" localhost:8172/auth/refresh      # after logout
```

(Put the first refresh token in `OLD` and the new one in `REFRESH` after the first call.) The statuses are:

```
200 OK                                   a new access token and a new refresh token
401 {"detail":"Invalid refresh token"}   the old one was used up
204 No Content                           logout
401 {"detail":"Invalid refresh token"}   refresh after logout
```

Look at the table. Only hashes are stored, never the tokens (the ids and hashes differ for you):

```bash
docker exec pyrepo-m17-l02-pg psql -U allcs allcs -c "SELECT id, student_id, left(token_hash, 12) AS token_hash, revoked FROM refresh_tokens ORDER BY id"
```

```
 id | student_id |  token_hash  | revoked 
----+------------+--------------+---------
  1 | ...        | c2a2816a49a9 | f
  2 | ...        | 077927c9141b | t
```

### 7. The honest part: logout does not kill an access token

Right after logout, send the OLD access token to `/me`:

```bash
curl -s -i localhost:8172/me -H "Authorization: Bearer $OLD_ACCESS"   # still 200
sleep 6
curl -s -i localhost:8172/me -H "Authorization: Bearer $OLD_ACCESS"   # 401
```

```
HTTP/1.1 200 OK
{"name":"Lukas",...}
HTTP/1.1 401 Unauthorized
{"detail":"Token expired"}
```

A JWT cannot be deleted because the server never wrote it down. Logout revokes the refresh token, so no new access tokens, and the one already out dies by itself. That is why access tokens are short.

### 8. Sign in with Google (local stand-in)

```bash
python oauth_flow.py
python peek_id_token.py
curl -s -i 'localhost:8172/auth/google/callback?code=abc&state=forged'
```

```
1. 307 to Google
   client_id = allcs-demo-client
   redirect_uri = http://localhost:8172/auth/google/callback
   response_type = code
   scope = openid email
   state = jA1Q611Slu3bR65X9-zlww
2. 307 back to our app
   code = EjdwjL-mdiD7sgUg
   state = jA1Q611Slu3bR65X9-zlww
3. 200 our own tokens
   ['access_token', 'refresh_token', 'token_type']
iss = http://localhost:8272
aud = allcs-demo-client
sub = standin-1234
email = priya@example.com
iat = 1793094130
exp = 1793094430
HTTP/1.1 400 Bad Request
{"detail":"Unknown state"}
```

`state` and `code` are random, yours will differ. The five steps: send the browser to Google with client id, redirect address, scope and a random state; the person agrees; Google sends the browser back with a short code and the same state; our server swaps the code (plus the client secret) for an ID token; we check the signature with Google's public key and that the token is for our client id, then read the email and issue our own tokens. A made-up `state` is refused.

Stop both servers (Ctrl+C).

### 9. Tests

```bash
pytest -q tests/test_auth.py
pytest -q
```

```
....                                                                     [100%]
4 passed in 0.41s
................                                                         [100%]
16 passed in 1.14s
```

The tamper test spoils two letters of the token body. The expired test builds a token "made an hour ago" through the `now` parameter, so no test has to sleep.

### 10. The three pitfalls

```bash
python pit_readable.py
python pit_algorithms.py 2>&1 | tail -1
python pit_subject.py 2>&1 | tail -1
SECRET_KEY=short-secret python jwt_parts.py 2>&1 | head -2
```

```
{'sub': '1', 'email': 'lukas@example.com', 'password_hash': '$argon2id$v=19$...'}
jwt.exceptions.DecodeError: It is required that you pass in a value for the "algorithms" argument when calling decode().
jwt.exceptions.InvalidSubjectError: Subject must be a string
...InsecureKeyLengthWarning: The HMAC key is 12 bytes long, which is below the minimum recommended length of 32 bytes for SHA256...
```

Only put the student id in a token. Always pass `algorithms=[...]` yourself. Write `sub` as text (`str(id)`) and convert back with `int`. Use a secret of at least 32 bytes.

## Common mistakes

- Putting secrets (email, password hash) in the JWT payload: anyone can read it.
- Calling `jwt.decode` without `algorithms`.
- Writing the student id as a number in `sub`: encoding works, decoding fails.
- Expecting logout to kill an access token. Keep access tokens short (15 minutes by default here).
- Storing refresh tokens as they are. Store a hash.
- Writing tests that `sleep`. Pass `now` into `make_access_token`.
- Logging a token: it works like a password until it expires. Send tokens only over HTTPS.

## Clean up

```bash
docker rm -f -v pyrepo-m17-l02-pg
rm -rf .venv
```

## Next

[M17-L03 · Authorisation and the OWASP API Top 10](../m17-l03-authorisation-and-the-owasp-api-top-10/README.md)
