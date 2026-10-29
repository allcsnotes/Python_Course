# M22-L02 · Web Scraping and APIs

> Video: Module 22, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- What a web page really is (HTML text, tags, attributes, CSS selectors) and when to scrape it
- Ask a site for its data the polite way, with an API: a token from the environment and a loop that follows `next`
- Read a page with Beautiful Soup: `select`, `select_one`, `get_text`, attributes, and following a "next page" link
- Be a good guest: `robots.txt`, a User-Agent, a delay, a cache, and `Retry-After` on a 429 answer
- Survive a page that changes (fail loudly instead of saving an empty file)
- Meet a page that only a real browser can read (Playwright), and find the shortcut behind it

## Before you start

- Python 3.14 or newer (`python --version`) and [uv](https://docs.astral.sh/uv/) (Module 7).
- Docker Desktop running. The "website" in this lesson is a local copy of allcsvideos.com that runs in a container on
  your laptop. **Nothing in this lesson touches the real internet.**
- `httpx` and the idea of a status code from M07-L04, and `csv` from M06-L02. No earlier lesson folder is needed.
- About 100 MB of disk for the browser Playwright downloads (step 14). It stays inside this folder.
- Everything here (the token, the e-mail address in the User-Agent, the courses) is a made-up demo value.

Work in a copy so that your clone stays clean:

```bash
cp -R m22-l02-web-scraping-and-apis ~/scrape
cd ~/scrape
uv sync
```

## Files in this folder

| File | What it is |
|------|------------|
| `pyproject.toml`, `uv.lock` | The project: httpx 0.28.1, beautifulsoup4 4.15.0, playwright 1.64.1 (pinned in the lock file) |
| `site/site.py` | The local copy of the site (standard library only): pages on port 22280, a token-protected API on port 22281 |
| `peek.py` | Fetch page 1 and print the HTML of one course box |
| `api_nokey.py` | Ask the API without a token |
| `api_first.py` | Ask the API with a token and follow `next` |
| `scrape1.py` | Beautiful Soup on one page |
| `scrape_all.py` | All four pages, with no politeness (it gets rate-limited) |
| `hammer.py` | Six requests in a row, to see the 429 answers |
| `robots.py` | Read `robots.txt` with the standard library |
| `polite.py` | `get(url)`: robots rules, User-Agent, cache, delay, Retry-After |
| `read_page.py` | `read_page(html)`: picks out the courses, with defences against a changed page |
| `scrape_polite.py` | The polite scraper: writes `courses.csv` |
| `rush.py` | The polite scraper with a tiny delay and an empty cache, to trigger a 429 on purpose |
| `fragile.py` | The old scraper code on the redesigned page (it breaks) |
| `sturdy.py`, `broken.py` | `read_page` on the new page, and on a maintenance page |
| `live_httpx.py` | httpx on the live-sessions page (sees nothing) |
| `live_pw.py` | Playwright on the same page (sees everything, slowly) |
| `live_net.py` | Playwright lists every answer the page received |
| `live_json.py` | The shortcut: call the address directly with httpx |

## Follow along

### 1. Start the local copy of the site

The container runs `site/site.py` with the official Python image. Run this in the project folder:

```bash
docker run -d --name m22l02-site -p 22280:22280 -p 22281:22281 \
  -v "$PWD/site":/site -w /site python:3.14-slim python site.py
```

The pages are at <http://localhost:22280/courses> (open it in your browser first: 8 courses on a page, 4 pages) and the
API is on port 22281. Every command below runs in your project folder on your laptop.

### 2. What a web page really is

```bash
uv run python peek.py
```

```
200
<h1>All courses</h1>
  <div class="course" data-id="1">
    <h2 class="title"><a href="/courses/python-from-zero-to-production">Python: From Zero to Production</a></h2>
    <span class="price">Rs 1499</span>
    <span class="level">Beginner</span>
    <span class="rating">4.8</span>
  </div>
```

The page is just text, written in HTML. Words in angle brackets are tags; a tag opens and closes with a slash. Inside one
course box an `h2` holds the title and three `span` tags hold the price, level and rating. The word `class` inside a tag
is an attribute: a label ("this is the price").

A scraper uses those labels. A CSS selector says which tags you mean: `.course` is every tag with the class `course`;
`.price` is the tag with the class `price`. Web scraping means: a program reads the text of a page and picks out the pieces
it wants. It is the second choice. **If the site offers an API, use that first.**

### 3. The API door, and its lock

The copy of the site has an API at `/api/courses`: ten courses per call, and a field called `next` (the address of the next
batch). First ask without a key:

```bash
uv run python api_nokey.py
```

```
401 {'detail': 'Missing or wrong token'}
```

401 means a missing or wrong token. A token is a secret word that proves who is asking. It must never be typed into the
code file, so it comes from the environment (M17). Here is a throw-away token for this local copy (it is the value the
`site.py` container uses by default):

```bash
export ALLCS_TOKEN=demo-token-4f2a9c
```

On Windows PowerShell: `$env:ALLCS_TOKEN = "demo-token-4f2a9c"`.

### 4. Use the API

`api_first.py` reads the token from the environment, builds the header `Authorization: Bearer <token>`, and loops while
there is an address. `raise_for_status()` stops the program on any error, `.json()` gives a dictionary, `extend` adds the
batch, and `url = data["next"]` ends the loop when it is `None`.

```bash
uv run python api_first.py
```

```
200 10 so far
200 20 so far
200 30 so far
200 32 so far
32 courses
{'id': 1, 'title': 'Python: From Zero to Production', 'price': 1499, 'level': 'Beginner', 'lessons': 120, 'rating': 4.8, 'students': 9120}
```

Four calls, 32 courses, with every field, even the number of students, which the page never shows. If there is an API,
use it: it is stable (the site promises it), its answers are already data, and it often has more fields than the page.

> The site slows down visitors who ask for pages too fast (step 7). If a command below prints a 429 answer or a surprising
> result, wait three seconds and run it again.

### 5. Beautiful Soup, one page

For the days when there is no door. Beautiful Soup takes HTML text and gives you a tree to search (it was added with
`uv add beautifulsoup4`, as in Module 7).

```bash
uv run python scrape1.py
```

```
Python: From Zero to Production Rs 1499
Python Data Structures Made Simple Rs 799
Git and GitHub for Beginners Rs 499
SQL and Postgres in Docker Rs 899
FastAPI from Scratch Rs 999
Docker for Python Apps Rs 799
Redis and Caching in Practice Rs 699
Testing with pytest Rs 599
/courses/testing-with-pytest
```

`BeautifulSoup(r.text, "html.parser")` makes the soup with Python's own HTML reader. `soup.select(".course")` gives one
item for each box. `box.select_one(".title a")` is the first match inside the box. `get_text(strip=True)` gives the
visible words without extra spaces, and `link["href"]` reads an attribute. Three ideas did all the work: select, get text
and attributes.

### 6. All four pages (and a quiet, wrong answer)

At the bottom of each page is a link with the class `next`. The loop: read a page, collect its courses, look for a next
link and follow it; when there is none, stop. The site has 32 courses. How many does the loop collect?

```bash
uv run python scrape_all.py
```

```
200 http://localhost:22280/courses?page=1 8
200 http://localhost:22280/courses?page=2 16
200 http://localhost:22280/courses?page=3 24
429 http://localhost:22280/courses?page=4 24
24 courses
```

Twenty-four. The fourth answer was 429 ("Too Many Requests"): a message, not a list, so the loop found no next link and
stopped. No crash, no error, just a quiet, wrong total. A scraper that does not look at the status code gives wrong data
without telling you.

### 7. Why a program must slow down

```bash
uv run python hammer.py
```

```
1 200 None
2 200 None
3 200 None
4 429 2
5 429 2
6 429 2
```

Three answers of 200, then 429 three times, each with `Retry-After: 2` (wait two seconds). A person never reads four pages
in a quarter of a second. A program does, and thousands of programs can knock a busy site over. Wait a few seconds before
the next step.

Four habits of a polite scraper: (1) read `robots.txt`; (2) say who you are; (3) slow down and remember what you fetched;
(4) obey 429.

### 8. Habit one: robots.txt

```bash
uv run python robots.py
```

```
/courses True
/admin/students False
delay: 1
```

Almost every site has a file at `/robots.txt` where the owners say which paths robots may visit.
`urllib.robotparser.RobotFileParser` (standard library) reads it: `can_fetch(bot_name, url)` answers yes or no, and
`crawl_delay` returns the pause the site asks for (here one second). Nothing forces you to obey: nothing stops a program
from fetching the forbidden page. We obey because that is the agreement of the web, and because sites block the bots that
ignore it.

### 9. Habits two to four: the `get` function

`polite.py` sets up a User-Agent (your bot's name, a version and a contact address, so the owner can write to you:
`allcsv-bot/1.0 (asha@allcsvideos.com)`, a demo address), a `cache` folder, and the delay from `robots.txt` (or one second).
`get(url)`:

1. checks the rules and raises `PermissionError` if `robots.txt` says no;
2. looks in the cache: the file name is made from the address with `quote(url, safe="")`; if the file exists it is read from
   disk and the site is not bothered again;
3. otherwise sleeps for the delay and asks, with the User-Agent and a timeout;
4. on a 429, reads `Retry-After`, waits that long and tries again; only a good answer is checked, cached and returned.

`read_page(html)` (in `read_page.py`) does the picking, and `scrape_polite.py` writes a CSV file with `csv.DictWriter`.
Remove any old cache, then run it twice:

```bash
rm -rf cache
uv run python scrape_polite.py
uv run python scrape_polite.py
ls cache
head -3 courses.csv | cut -c1-64
```

```
8 courses so far
16 courses so far
24 courses so far
32 courses so far
saved 32 courses in 4.2 s
8 courses so far
16 courses so far
24 courses so far
32 courses so far
saved 32 courses in 0.2 s
http%3A%2F%2Flocalhost%3A22280%2Fcourses%3Fpage%3D1
http%3A%2F%2Flocalhost%3A22280%2Fcourses%3Fpage%3D2
http%3A%2F%2Flocalhost%3A22280%2Fcourses%3Fpage%3D3
http%3A%2F%2Flocalhost%3A22280%2Fcourses%3Fpage%3D4
title,price,url
Python: From Zero to Production,Rs 1499,http://localhost:22280/c
Python Data Structures Made Simple,Rs 799,http://localhost:22280
```

The first run takes about four seconds (one second before every request, so your time will differ a little). The second
run is almost instant because nothing was fetched: the cache has four files. `courses.csv` has a header and 32 rows:
title, price and address. This is the kind of file pandas analyses in the next lesson.

### 10. If we rush on purpose

`rush.py` sets the delay to 0.1 seconds and uses an empty cache folder:

```bash
uv run python rush.py
```

```
8 rows
8 rows
8 rows
429: waiting 2 seconds
8 rows
```

Three pages go through, then the site says 429. Our code prints it, waits two seconds and goes on. The scraper slowed
itself down.

### 11. Pages change: the fragile scraper

Next month the site is redesigned. Same courses, new look, new names: the boxes are called `card`, the title is
`card-title`, the price is `card-price`. Run the old scraper code on the new page (`/new/courses`):

```bash
uv run python fragile.py
```

```
200 0 courses
Traceback (most recent call last):
  File "fragile.py", line 10, in <module>
    price = soup.select_one(".price").get_text(strip=True)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get_text'
```

(The path in your traceback is longer.) Status 200 and zero courses: no error, because `select` found nothing and returned
an empty list. The first failure is the dangerous one because nothing complains.

### 12. Three defences

`read_page.py` has three defences: if nothing is found, raise an error that names the likely cause; a selector can list
alternatives separated by commas (`.course, .card`, `.price, .card-price`, `a.next, a[rel=next]`); and if a box is missing a
piece, stop with a message instead of saving a half-empty row.

```bash
uv run python sturdy.py
uv run python broken.py
```

```
8 courses; first: Python: From Zero to Production Rs 1499
next page: http://localhost:22280/new/courses?page=2
Traceback (most recent call last):
  File "broken.py", line 3, in <module>
    read_page("<html><body><p>Maintenance</p></body></html>")
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "read_page.py", line 10, in read_page
    raise ValueError("no courses found: did the page change?")
ValueError: no courses found: did the page change?
```

A clear message today, not a silent empty file next week. Still be honest: a scraper is a guess about somebody else's page,
and one day the guess breaks. Check your counts, fail loudly, and when an API exists, prefer it.

### 13. A page that JavaScript fills in

Open <http://localhost:22280/live> in a browser: five live sessions. But a moment after the page opens it only says
"Loading...". A small JavaScript program inside the page asks the site for the sessions and fills the list in. What does
httpx see? It gets the page as the server sent it, before any JavaScript runs:

```bash
uv run python live_httpx.py
```

```
200 0 sessions
<ul class="live" id="sessions"></ul>
0.24 s
```

Fast, and useless: zero sessions and an empty list. (The time is a fraction of a second; yours will differ.)

### 14. A real browser: Playwright

Playwright drives a real browser with code. Install the browser into this project folder, so nothing is global:

```bash
export PLAYWRIGHT_BROWSERS_PATH="$PWD/.pw-browsers"
uv run playwright install chromium
```

On Windows PowerShell: `$env:PLAYWRIGHT_BROWSERS_PATH = "$PWD\.pw-browsers"`. The download is about 100 MB. Then:

```bash
uv run python live_pw.py
```

```
Ask Meera Anything: Python - Sat 19:00
Live Code Review: FastAPI - Sun 18:00
Docker Office Hours - Tue 20:00
Mock Interview Night - Thu 21:00
SQL Q and A - Fri 19:30
6.15 s
```

`p.chromium.launch()` starts the browser, `page.goto(...)` opens the page, `page.wait_for_selector("li.session")` waits
until the sessions exist, and then `page.locator("li.session").all_text_contents()` reads them. It works, but a browser has
to start, load the page, run the JavaScript and draw it: about 5 to 6 seconds on a laptop, against a fraction of a second
for httpx. For 32 pages that is minutes and a lot of memory.

### 15. Look for the shortcut

The page itself asked the site for something. Playwright can list every answer it saw:

```bash
uv run python live_net.py
```

```
200 document http://localhost:22280/live
200 fetch http://localhost:22280/live-sessions.json
```

The sessions were never inside the page: they come from a small API of their own. Call that address directly with plain
httpx:

```bash
uv run python live_json.py
```

```
Ask Meera Anything: Python - Sat 19:00
Live Code Review: FastAPI - Sun 18:00
Docker Office Hours - Tue 20:00
Mock Interview Night - Thu 21:00
SQL Q and A - Fri 19:30
0.47 s
```

The same five sessions, about ten times faster. Order of preference: an API, then plain pages with Beautiful Soup, and only
then a real browser.

### 16. The rules, in plain words (this is not legal advice)

- Read the site's terms of service: some sites forbid scraping.
- Check `robots.txt`.
- Do not collect personal data (names, e-mail addresses) without a good reason and a clear right.
- Do not overload a site.
- Do not publish a site's work as your own: facts are one thing, creative work is another.
- When you are unsure, ask the owner, or use the API.

## Common mistakes

- Scraping when an API exists. Check for an API first (and look at the browser's network list for one behind the page).
- Not checking the status code: a 429 page has no courses, so the loop ends early and gives a quiet, wrong total.
- Fetching fast and forgetting the delay, the cache and the User-Agent.
- Ignoring `robots.txt`. Python does not stop you, but the site may block you.
- A scraper that returns an empty list when the page changes. Fail loudly, with a message that names the likely cause.
- Typing a token into the code. It comes from the environment.
- Reaching for a browser (Playwright) before looking for the API behind the page.

## Clean up

```bash
docker rm -f -v m22l02-site
rm -rf cache cache_rush courses.csv .pw-browsers .venv
```

If you worked in a copy (`~/scrape`), delete that folder when you are done.

## Next

[M22-L03 · Data Analysis Taster](../m22-l03-data-analysis-taster/)
