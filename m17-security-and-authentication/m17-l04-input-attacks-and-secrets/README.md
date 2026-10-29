# M17-L04 · Input Attacks and Secrets

> Video: Module 17, Lesson 4. Watch it first, then follow along here.

## What you'll learn

- The golden rule: input is data, never instructions
- SQL injection, step by step, and the fix with bound parameters (plus an allow list for column names)
- Cross-site scripting (a script inside a web page) and why escaping on output fixes it
- Server-side request forgery (a server tricked into fetching secret pages) and the allow list fix
- Why `pickle.loads` and `eval` on outside data are dangerous, and the safe tools (`json`, `ast.literal_eval`)
- `pip-audit` for old libraries, and what to do when a secret leaks into git

## Before you start

- Python 3.14 or newer (`python --version`) and Docker running (one Postgres container).
- No earlier lesson folder is needed. Everything in this lesson runs on a throwaway database on your laptop.
- All keys and addresses are made up for the demo ("demo-only-key" and `example.com` addresses).
- `pip-audit` asks the Python package index for known problems, so it needs internet. Everything else is local.

Start Postgres and install the packages:

```bash
docker run -d --name pyrepo-m17-l04-pg -e POSTGRES_PASSWORD=devpass -e POSTGRES_DB=allcs -p 17404:5432 postgres:17.11
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install sqlalchemy==2.1.6 "psycopg[binary]==3.3.6" jinja2==3.1.6 httpx==0.28.1 "fastapi[standard]==0.162.0" pip-audit==2.10.1
cd files
python seed.py
```

`seed.py` makes a `courses` table (three published courses and two hidden drafts) and a `students` table (Lukas, Priya, Ben) in the throwaway database.

## Files in this folder

| File | What it is |
|------|------------|
| `files/db.py` | The engine for the demo database (port 17404) |
| `files/seed.py` | Creates and fills the two demo tables |
| `files/search_bad.py` | Priya's search that glues the typed text into the SQL |
| `files/hook.py` | Searches for `python` and for a strange text |
| `files/show_query.py`, `files/union.py` | Print the exact SQL the database received, and a data-leaking `UNION` text |
| `files/search_good.py`, `files/fix.py`, `files/echo_good.py` | The fix with a bound parameter, the three searches again, and the SQL echo |
| `files/sort_by.py` | An allow list for the column to sort by |
| `files/xss.py`, `files/jinja_demo.py`, `files/json_not_html.py` | Escaping by hand, Jinja2 auto-escape, and a JSON response |
| `files/servers.py`, `files/ssrf_bad.py`, `files/fetch_good.py`, `files/ssrf_good.py` | Two tiny local servers, the fetch that trusts any address, and the allow-listed fetch |
| `files/pickle_bad.py`, `files/eval_bad.py`, `files/safe_load.py` | Code that runs while loading data, and the safe loaders |
| `files/old.txt`, `files/new.txt` | A requirements file with an old PyYAML, and the fixed one |
| `files/settings_env.py` | Reads a key from the environment |

## Follow along

All commands run in `files/` with the virtual environment active.

### 1. SQL injection

```bash
python hook.py
```

```
'python': 1 found
    Python Basics
"zzz' OR true --": 5 found
    Python Basics
    SQL in Two Weeks
    FastAPI in Practice
    Draft: Launch Plan
    Draft: Price Review
```

The strange text returned every course, including the two drafts that were meant to stay hidden. Now look at the SQL sentence the database received:

```bash
python show_query.py
```

```
SELECT title FROM courses
WHERE published
  AND title ILIKE '%python%'

SELECT title FROM courses
WHERE published
  AND title ILIKE '%zzz' OR true --%'
```

The visitor's single quote closed the quote Priya opened. `OR true` is always true, so the `published` check protects nothing, and `--` starts a comment that hides the rest of the line. With a `UNION` the typed text can even pull data from another table:

```bash
python union.py
```

```
priya@example.com
ben@example.com
lukas@example.com
```

(The order of the rows may differ.) A search box just leaked the students' emails, printed as if they were course titles.

### 2. The fix: bound parameters

`search_good.py` keeps the SQL fixed (`ILIKE :pattern`) and sends the value separately in a dictionary (the `%` signs belong to the value).

```bash
python fix.py
```

```
1 found for 'python'
0 found for "zzz' OR true --"
0 found for "zzz' UNION SELECT email FROM students --"
```

Nothing was cleaned. Postgres simply looked for a course whose title really contains a quote, the letters OR and two dashes. See what travels:

```bash
python echo_good.py
```

```
select pg_catalog.version()
[raw sql] {}
select current_schema()
[raw sql] {}
show standard_conforming_strings
[raw sql] {}
BEGIN (implicit)
SELECT title FROM courses
WHERE published
  AND title ILIKE %(pattern)s
[generated in 0.00011s] {'pattern': "%zzz' OR true --%"}
ROLLBACK
```

The sentence arrives with its blank, the value arrives on the last line, quote and all. (The `generated in` time differs for you.) SQLAlchemy's `select()`, `where()` and `ilike()` bind values the same way. The danger starts when you glue text yourself with an f-string, `+` or `%`.

A blank can hold a value, never a table or column name. For that, check against an allow list:

```bash
python sort_by.py
```

```
[('SQL in Two Weeks', 399), ('Python Basics', 449)]
Traceback (most recent call last):
  ...
ValueError: cannot sort by 'price; DROP TABLE courses'
```

### 3. Scripts inside web pages (XSS)

```bash
python xss.py
python jinja_demo.py
python json_not_html.py
```

```
<p>Nice! <script>alert(1)</script></p>
<p>Nice! &lt;script&gt;alert(1)&lt;/script&gt;</p>
<p>Nice! &lt;script&gt;alert(1)&lt;/script&gt;</p>
application/json
{"description":"Nice! <script>alert(1)</script>"}
```

The first line is a real script tag that a browser would run for every visitor. `html.escape` (second line) and Jinja2 with `autoescape=True` (third line) turn the angle brackets into harmless codes. A JSON API is not the problem, because a browser does not run a script that sits inside JSON. The problem is the page that shows the data, so keep auto-escape on.

### 4. A server tricked into fetching (SSRF)

`servers.py` starts two tiny servers: a stand-in for the outside web on port 8174 (a public logo) and an "internal" page on port 8274 (staff notes).

```bash
python ssrf_bad.py
```

```
PNG-bytes-of-a-public-image
internal only: staff notes, never public
```

Our server fetched the internal page on the visitor's behalf. Now the allow list (`fetch_good.py`: only `http` or `https`, and only host and port pairs on the list):

```bash
python ssrf_good.py
```

```
PNG-bytes-of-a-public-image
Traceback (most recent call last):
  ...
ValueError: host not allowed: localhost:8274
```

A list of bad addresses is not enough, because there are too many ways to write the same address. A list of good ones is.

### 5. Data that runs code

```bash
python pickle_bad.py
python eval_bad.py
python safe_load.py
```

```
received 73 bytes
this ran just by loading the data
800.0
3
True
{'course': 1, 'seats': 2}
[10, 20, 30]
ValueError: refused to run code
```

Loading the pickle ran the attacker's function. The "discount formula" passed to `eval` wrote a file (`proof.txt`) on disk: the third line `True` says the file exists. Delete it afterwards (`rm proof.txt`). Never unpickle or `eval` outside data. `json.loads` and `ast.literal_eval` only read data, and `literal_eval` refuses to run a call.

### 6. Old libraries: pip-audit

```bash
pip-audit -r old.txt --no-deps --disable-pip
pip-audit -r new.txt --no-deps --disable-pip
```

```
Found 2 known vulnerabilities in 1 package
Name   Version ID             Fix Versions
------ ------- -------------- ------------
pyyaml 5.3.1   PYSEC-2021-142 5.4
pyyaml 5.3.1   PYSEC-2021-142 5.4
No known vulnerabilities found
```

(Lines starting with `WARNING` are also printed. The same entry appears twice because the data source lists it twice. The database of known problems changes over time, so your result may differ.) `old.txt` pins `pyyaml==5.3.1`, `new.txt` pins `pyyaml==6.0.3`. `pip-audit` only knows about problems that are already known, so run it regularly.

### 7. Secrets and git

A key read from the environment, and the failure when it is missing:

```bash
python settings_env.py
PAYMENT_KEY=demo-only-key python settings_env.py
```

```
Traceback (most recent call last):
  ...
KeyError: 'PAYMENT_KEY'
key loaded, length 13
```

Now what happens when a key is committed once. Use a throwaway folder and a made-up key:

```bash
mkdir /tmp/leakdemo && cd /tmp/leakdemo
git init -q -b main
git config user.name Asha && git config user.email asha@example.com
printf 'API_KEY = "demo-only-key-f5197d14"\n' > settings.py
git add settings.py
git commit -m "add settings"
printf 'import os\n\nAPI_KEY = os.environ["API_KEY"]\n' > settings.py
git commit -am "remove the key"
git log --oneline
git show HEAD~1:settings.py
```

```
[main (root-commit) b7dbb53] add settings
 1 file changed, 1 insertion(+)
 create mode 100644 settings.py
[main 1958a06] remove the key
 1 file changed, 3 insertions(+), 1 deletion(-)
1958a06 remove the key
b7dbb53 add settings
API_KEY = "demo-only-key-f5197d14"
```

(The commit ids differ for you.) The key is still in the history. Deleting is not enough: treat it as leaked, rotate it (new key, switch the app, revoke the old one). Prevent it instead: put `.env` in `.gitignore` before the first commit, never print or log a secret, give each key only the power it needs, and use a secret scanner on every commit.

## Common mistakes

- Cleaning input by hand (removing quotes, banning the word `select`). Attackers find another spelling. Use bound parameters, escaping on output and allow lists.
- Checking only in the browser. Every check must be repeated on the server (for example with Pydantic models).
- Showing the attacker details: a full SQL sentence or a traceback in an error page. Log the details, return a short plain message.
- Pasting a column name into SQL without an allow list.
- Using `pickle.loads` or `eval` on bytes or text from outside.
- Committing a secret and "fixing" it with a new commit.

## Clean up

```bash
rm -f proof.txt
rm -rf /tmp/leakdemo
docker rm -f -v pyrepo-m17-l04-pg
cd .. && rm -rf .venv
```

## Next

[M17-B10 · Build Secure allcsvideos](../m17-b10-build-secure-allcsvideos/README.md)
