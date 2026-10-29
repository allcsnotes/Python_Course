# M06-L05 · Dates, Times and the Standard Library Tour

> Video: Module 6, Lesson 5. Watch it first, then follow along here.

## What you'll learn
- Work with `date`, `datetime` and `timedelta`: places and distances on a calendar.
- Turn a datetime into text with `strftime`, and text into a datetime with `strptime`.
- Tell naive from aware datetimes, convert with `zoneinfo` and `astimezone`, and store times in UTC.
- Tour four ready-made drawers of the standard library: `random`, `collections`, `itertools` and `re`.

## Before you start
- Python 3.14 or newer. Check with `python --version`.
- No packages and no Docker. (On Windows only, `zoneinfo` also needs `pip install tzdata`; see step 12.)
- Helpful: M06-L03 and M06-L04 (errors with `try` and `except`) and M05-L03 (dictionaries).
- Run every command from inside this folder.
- In the "you should see" blocks, traceback file paths are shortened to the file name. Yours show the full path.

## Files in this folder
| File | What it is |
| --- | --- |
| `hook.py` | the hook: 18:00, but where? |
| `dates.py`, `badday.py` | `date` and an impossible date |
| `dt.py` | `datetime`, `.hour`, `.minute`, `.date()` |
| `nowdemo.py` | `date.today()` and `datetime.now()` (output changes) |
| `gap.py`, `addtd.py`, `endtime.py`, `late.py` | `timedelta` maths |
| `codes.py`, `fmt.py` | `strftime` codes and patterns |
| `parse.py`, `parsebad.py`, `order.py`, `safe.py` | `strptime`, a bad pattern, day-first trap, safe reading |
| `iso.py` | ISO format round trip |
| `aware.py`, `zones.py`, `summer.py`, `naive.py` | time zones with `zoneinfo` |
| `utc.py`, `nowutc.py` | store in UTC, show in a local zone |
| `rand.py`, `seeded.py`, `shufnone.py` | `random`, seeds, and the `shuffle` pitfall |
| `counter.py`, `plain.py`, `dd.py` | `Counter`, a missing key, `defaultdict` |
| `chain.py`, `combo.py`, `combo10.py` | `itertools` |
| `re1.py`, `renone.py`, `refind.py`, `rawbad.py` | regular expressions with `re` |
| `together.py` | `strptime` plus `Counter`: events per hour |
| `birthday_try.py` | one possible answer to "try it yourself" |

## Follow along

### 1. The hook: six in the evening, where?
Asha saves the start of the next class on allcsvideos.com: 2 November 2026 at 18:00. Python prints exactly what she typed. But Lukas in Frankfurt joins at six his time and the room is empty. The lesson answers why.

`hook.py`:
```python
from datetime import datetime

start = datetime(2026, 11, 2, 18, 0)
print("Class starts:", start)
```
```bash
python hook.py
```
You should see:
```
Class starts: 2026-11-02 18:00:00
```

### 2. Dates: one square on the calendar
`date` has a year, a month and a day. Import just one tool from the `datetime` drawer. Dates always print year first. A date that does not exist is an error.

`dates.py`:
```python
from datetime import date

today = date(2026, 10, 25)
print(today)
print(today.year)
print(today.month)
print(today.day)
```
```bash
python dates.py
```
You should see:
```
2026-10-25
2026
10
25
```

`badday.py`:
```python
from datetime import date

print(date(2026, 2, 30))
```
```bash
python badday.py
```
You should see:
```
Traceback (most recent call last):
  File "badday.py", line 3, in <module>
    print(date(2026, 2, 30))
          ~~~~^^^^^^^^^^^^^
ValueError: day 30 must be in range 1..28 for month 2 in year 2026
```

Python knows the calendar: you cannot build an impossible date.

### 3. Datetimes: a date plus a time of day
`datetime` adds hours and minutes (24 hour clock). `.date()` gives back just the date part.

`dt.py`:
```python
from datetime import datetime

start = datetime(2026, 11, 2, 18, 30)
print(start)
print(start.hour, start.minute)
print(start.date())
```
```bash
python dt.py
```
You should see:
```
2026-11-02 18:30:00
18 30
2026-11-02
```

### 4. The current moment
`date.today()` and `datetime.now()` give the real date and time, so the output changes on every run. Your output will differ: this one changes every time you run it. Yours will show your own date and time. The long tail is millionths of a second. When a lesson needs the same output every time, it uses fixed dates like 25 October 2026.

`nowdemo.py`:
```python
from datetime import date, datetime

print(date.today())
print(datetime.now())
```
```bash
python nowdemo.py
```
You should see:
```
2026-10-29
2026-10-29 21:42:47.244402
```

### 5. timedelta: the distance between dates
Town minus town gives a distance (a `timedelta`). Town plus a distance gives another town. Town plus town makes no sense, so Python refuses to add two dates.

`gap.py`:
```python
from datetime import date

today = date(2026, 10, 25)
class_day = date(2026, 11, 2)
gap = class_day - today
print(gap)
print(gap.days)
```
```bash
python gap.py
```
You should see:
```
8 days, 0:00:00
8
```

`addtd.py`:
```python
from datetime import date, timedelta

class_day = date(2026, 11, 2)
print(class_day + timedelta(days=7))
print(class_day - timedelta(days=1))
print(class_day + timedelta(days=100))
```
```bash
python addtd.py
```
You should see:
```
2026-11-09
2026-11-01
2027-02-10
```

`endtime.py`:
```python
from datetime import datetime, timedelta

start = datetime(2026, 11, 2, 18, 0)
length = timedelta(hours=1, minutes=30)
end = start + length
print(end)
print(length)
print(end > start)
```
```bash
python endtime.py
```
You should see:
```
2026-11-02 19:30:00
1:30:00
True
```

`late.py`:
```python
from datetime import datetime, timedelta

start = datetime(2026, 11, 2, 23, 30)
length = timedelta(hours=1, minutes=30)
print(start + length)
```
```bash
python late.py
```
You should see:
```
2026-11-03 01:00:00
```

Three rules: a date minus a date is a `timedelta`; a date plus a `timedelta` is a date; `.days` turns a `timedelta` into a plain number.

### 6. strftime: datetime to text
`strftime` (string from time) takes a pattern. A percent sign with a letter is a code, and every other character is copied. First, the codes one by one:

`codes.py`:
```python
from datetime import datetime

start = datetime(2026, 11, 2, 18, 0)
for code in ["%Y", "%m", "%d", "%H", "%M", "%A", "%B"]:
    print(code, start.strftime(code))
```
```bash
python codes.py
```
You should see:
```
%Y 2026
%m 11
%d 02
%H 18
%M 00
%A Monday
%B November
```

`fmt.py`:
```python
from datetime import datetime

start = datetime(2026, 11, 2, 18, 0)
print(start.strftime("%d/%m/%Y"))
print(start.strftime("%H:%M"))
print(start.strftime("%A, %d %B %Y"))
print(f"Class: {start:%d %B, %H:%M}")
```
```bash
python fmt.py
```
You should see:
```
02/11/2026
18:00
Monday, 02 November 2026
Class: 02 November, 18:00
```

The last line is an f-string with the same pattern after a colon.

### 7. strptime: text to datetime
`strptime` (string to time) uses the same codes, but they describe the shape of the text you already have.

`parse.py`:
```python
from datetime import datetime

text = "2026-11-02 18:00"
when = datetime.strptime(text, "%Y-%m-%d %H:%M")
print(when)
print(type(when))
```
```bash
python parse.py
```
You should see:
```
2026-11-02 18:00:00
<class 'datetime.datetime'>
```

The result is a real `datetime`, no longer text, so you can add `timedelta`s, compare and convert it.

### 8. When the pattern does not fit
The pattern must fit the text exactly. Here the text uses slashes but the pattern uses dashes.

`parsebad.py`:
```python
from datetime import datetime

text = "02/11/2026"
when = datetime.strptime(text, "%Y-%m-%d")
print(when)
```
```bash
python parsebad.py
```
You should see:
```
Traceback (most recent call last):
  File "parsebad.py", line 4, in <module>
    when = datetime.strptime(text, "%Y-%m-%d")
  ...
ValueError: time data '02/11/2026' does not match format '%Y-%m-%d'
```

The middle of the real traceback lives inside Python's own files, so it is trimmed here (`...`). Read the first line that names your file, and the last line.

### 9. The silent trap: day first or month first
The text `03/11/2026` is 3 November in India and Germany, but 11 March in the United States. No error, only a different date.

`order.py`:
```python
from datetime import datetime

text = "03/11/2026"
print(datetime.strptime(text, "%d/%m/%Y").date())
print(datetime.strptime(text, "%m/%d/%Y").date())
```
```bash
python order.py
```
You should see:
```
2026-11-03
2026-03-11
```

Agree on the order before you read the text, and prefer the year first.

### 10. Catch bad text with try and except
Wrap the reading in a small function that returns `None` for bad text. The caller decides what to do (catch where you can decide).

`safe.py`:
```python
from datetime import datetime


def read_day(text):
    try:
        return datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return None


print(read_day("2026-11-02"))
print(read_day("02/11/2026"))
```
```bash
python safe.py
```
You should see:
```
2026-11-02 00:00:00
None
```

The good text becomes a `datetime` with midnight as the time, because the pattern had no hours.

### 11. ISO format
Year, month, day, a capital `T`, then the time. `isoformat` writes it and `fromisoformat` reads it back with no pattern. When you save a datetime as text, ISO format is the safest choice.

`iso.py`:
```python
from datetime import datetime

start = datetime(2026, 11, 2, 18, 0)
text = start.isoformat()
print(text)
print(datetime.fromisoformat(text) == start)
```
```bash
python iso.py
```
You should see:
```
2026-11-02T18:00:00
True
```

### 12. Naive and aware: six, where?
A datetime without a place is naive. One that knows its place is aware. The place is an offset from UTC, the world's reference clock (it never changes for daylight saving). Mumbai is UTC+05:30, Frankfurt in winter is UTC+01:00. The `zoneinfo` module gives zones names such as `Asia/Kolkata` (all of India) and `Europe/Berlin` (all of Germany).

On Windows, `zoneinfo` needs an extra package called `tzdata` (you learn to install packages in module 7). If you see `ZoneInfoNotFoundError` on Windows, that is the reason.

`aware.py`:
```python
from datetime import datetime
from zoneinfo import ZoneInfo

kolkata = ZoneInfo("Asia/Kolkata")
start = datetime(2026, 11, 2, 18, 0, tzinfo=kolkata)
print(start)
```
```bash
python aware.py
```
You should see:
```
2026-11-02 18:00:00+05:30
```

Look at the end: `+05:30`. The datetime is aware.

### 13. Lukas's clock
`astimezone` converts the same moment into another zone.

`zones.py`:
```python
from datetime import datetime
from zoneinfo import ZoneInfo

kolkata = ZoneInfo("Asia/Kolkata")
berlin = ZoneInfo("Europe/Berlin")
start = datetime(2026, 11, 2, 18, 0, tzinfo=kolkata)
print(start)
print(start.astimezone(berlin))
print(start == start.astimezone(berlin))
```
```bash
python zones.py
```
You should see:
```
2026-11-02 18:00:00+05:30
2026-11-02 13:30:00+01:00
True
```

When Asha's clock says 18:00, Lukas's says 13:30, so he joined four and a half hours late. The last line is `True`: aware datetimes compare by the moment, not by the digits.

### 14. Daylight saving
Berlin is one hour ahead of UTC in winter and two in summer. India never changes its clocks. The same Mumbai time gives a different Berlin time, and Python knows the rule for that year.

`summer.py`:
```python
from datetime import datetime
from zoneinfo import ZoneInfo

kolkata = ZoneInfo("Asia/Kolkata")
berlin = ZoneInfo("Europe/Berlin")
winter = datetime(2026, 11, 2, 18, 0, tzinfo=kolkata)
summer = datetime(2027, 7, 1, 18, 0, tzinfo=kolkata)
print(winter.astimezone(berlin))
print(summer.astimezone(berlin))
```
```bash
python summer.py
```
You should see:
```
2026-11-02 13:30:00+01:00
2027-07-01 14:30:00+02:00
```

Never add five and a half hours by hand. Let `zoneinfo` do the work.

### 15. Do not mix naive and aware
`naive.py`:
```python
from datetime import datetime
from zoneinfo import ZoneInfo

kolkata = ZoneInfo("Asia/Kolkata")
naive = datetime(2026, 11, 2, 18, 0)
aware = datetime(2026, 11, 2, 18, 0, tzinfo=kolkata)
print(naive.tzinfo)
print(aware.tzinfo)
print(aware - naive)
```
```bash
python naive.py
```
You should see:
```
None
Asia/Kolkata
Traceback (most recent call last):
  File "naive.py", line 9, in <module>
    print(aware - naive)
          ~~~~~~^~~~~~~
TypeError: can't subtract offset-naive and offset-aware datetimes
```

Python refuses to guess where your naive time lived. The fix: make both aware.

### 16. Store times in UTC
Store times in UTC and show a local zone only when a person looks at them. Then every server and every person agrees on the same moment.

`utc.py`:
```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

saved = datetime(2026, 11, 2, 12, 30, tzinfo=timezone.utc)
print(saved)
print(saved.astimezone(ZoneInfo("Asia/Kolkata")))
print(saved.astimezone(ZoneInfo("Europe/Berlin")))
```
```bash
python utc.py
```
You should see:
```
2026-11-02 12:30:00+00:00
2026-11-02 18:00:00+05:30
2026-11-02 13:30:00+01:00
```

One saved time, two readings on two screens.

### 17. The current moment in UTC
Use this when you save a timestamp.

`nowutc.py`:
```python
from datetime import datetime, timezone

print(datetime.now(timezone.utc))
```
```bash
python nowutc.py
```
You should see:
```
2026-10-29 16:12:47.283792+00:00
```

Your output will differ: this one changes every time you run it. Yours will show your own date and time.

### 18. random: a dice, a winner, finalists
`random.choice` picks one item, `random.sample` picks several different ones, `random.shuffle` mixes a list in place.

`rand.py`:
```python
import random

students = ["Lukas", "Priya", "Meera", "Rahul"]
print(random.randint(1, 6))
print(random.choice(students))
print(random.sample(students, 2))
random.shuffle(students)
print(students)
```
```bash
python rand.py
```
You should see:
```
4
Meera
['Rahul', 'Priya']
['Priya', 'Rahul', 'Lukas', 'Meera']
```
Run it again and you get different numbers and names. Your output will differ: every run is a fresh draw.

### 19. Repeatable randomness with a seed
`random.seed(42)` sets the starting point, so the same seed always gives the same draws.

`seeded.py`:
```python
import random

random.seed(42)
students = ["Lukas", "Priya", "Meera", "Rahul"]
print(random.randint(1, 6))
print(random.choice(students))
print(random.sample(students, 2))
random.shuffle(students)
print(students)
```
```bash
python seeded.py
```
You should see:
```
6
Lukas
['Lukas', 'Meera']
['Priya', 'Rahul', 'Lukas', 'Meera']
```

Run it twice: identical. The exact names depend on the Python version, but with the same version and the same seed, the draws repeat.

### 20. collections: Counter
A `Counter` counts everything in one go. It is a dictionary with extra powers, and a missing key counts as `0` instead of raising `KeyError`.

`counter.py`:
```python
from collections import Counter

orders = ["Python", "SQL", "Python", "Docker", "Python", "SQL"]
counts = Counter(orders)
print(counts)
print(counts.most_common(2))
print(counts["Python"], counts["Rust"])
```
```bash
python counter.py
```
You should see:
```
Counter({'Python': 3, 'SQL': 2, 'Docker': 1})
[('Python', 3), ('SQL', 2)]
3 0
```

### 21. collections: defaultdict
With a plain empty dictionary, the first `append` fails because there is no list under `Python` yet.

`plain.py`:
```python
by_course = {}
by_course["Python"].append("Lukas")
```
```bash
python plain.py
```
You should see:
```
Traceback (most recent call last):
  File "plain.py", line 2, in <module>
    by_course["Python"].append("Lukas")
    ~~~~~~~~~^^^^^^^^^^
KeyError: 'Python'
```

`defaultdict(list)` creates a new empty list for a missing key (the word `list`, without brackets, is the recipe for a fresh value). `zip` walks through the two lists together.

`dd.py`:
```python
from collections import defaultdict

courses = ["Python", "SQL", "Python", "SQL"]
names = ["Lukas", "Priya", "Meera", "Rahul"]
by_course = defaultdict(list)
for course, name in zip(courses, names):
    by_course[course].append(name)
for course, group in by_course.items():
    print(course, group)
```
```bash
python dd.py
```
You should see:
```
Python ['Lukas', 'Meera']
SQL ['Priya', 'Rahul']
```

Counter counts things. `defaultdict` groups things.

### 22. itertools: chain and count
`chain` walks through several lists as if they were one, without building a new list. `count(101)` counts upwards for ever, and `zip` stops at the shorter list.

`chain.py`:
```python
from itertools import chain, count

morning = ["Lukas", "Priya"]
evening = ["Meera", "Rahul"]
for name in chain(morning, evening):
    print(name)
for ticket, name in zip(count(101), morning):
    print(ticket, name)
```
```bash
python chain.py
```
You should see:
```
Lukas
Priya
Meera
Rahul
101 Lukas
102 Priya
```

### 23. itertools: combinations
All the different pairs from a team, for pair programming. The second number is the size of each group.

`combo.py`:
```python
from itertools import combinations

team = ["Lukas", "Priya", "Meera"]
for pair in combinations(team, 2):
    print(pair)
```
```bash
python combo.py
```
You should see:
```
('Lukas', 'Priya')
('Lukas', 'Meera')
('Priya', 'Meera')
```

`combo10.py`:
```python
from itertools import combinations

print(len(list(combinations(range(10), 2))))
```
```bash
python combo10.py
```
You should see:
```
45
```

Order does not matter, so Priya with Lukas is not a new pair. Ten people already make 45 pairs.

### 24. re: finding a shape in text
A regular expression is a pattern for text. `ORD-\d{4}-\d{4}` reads as: `ORD-`, four digits, a dash, four digits. `re.search` finds the first match and gives back a match object, and `.group()` gives the matched text.

`re1.py`:
```python
import re

text = "Order ORD-2026-0042 shipped to lukas@example.com"
found = re.search(r"ORD-\d{4}-\d{4}", text)
print(found)
print(found.group())
```
```bash
python re1.py
```
You should see:
```
<re.Match object; span=(6, 19), match='ORD-2026-0042'>
ORD-2026-0042
```

The `span` tells you where the match was found (position 6 to 19).

### 25. search gives None when nothing matches
`renone.py`:
```python
import re

found = re.search(r"ORD-\d{4}-\d{4}", "no order here")
print(found)
print(found.group())
```
```bash
python renone.py
```
You should see:
```
None
Traceback (most recent call last):
  File "renone.py", line 5, in <module>
    print(found.group())
          ^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'group'
```

You cannot ask `None` for a group. Always check first: `if found:`.

### 26. findall
`findall` gives back a plain list of every match. `\w+` is one or more letters, digits or underscores, and `\.` is a real dot (a plain dot means any character). This email pattern is simplified, since real emails are wilder.

`refind.py`:
```python
import re

log = "ORD-2026-0042 paid, ORD-2026-0043 refunded"
print(re.findall(r"ORD-\d{4}-\d{4}", log))
mail = "write to lukas@example.com or priya@example.com"
print(re.findall(r"\w+@\w+\.com", mail))
```
```bash
python refind.py
```
You should see:
```
['ORD-2026-0042', 'ORD-2026-0043']
['lukas@example.com', 'priya@example.com']
```

### 27. Raw strings: always put the r in front
Without the `r`, Python tries to read `\d` itself. The file below leaves the `r` out.

`rawbad.py`:
```python
import re

log = "ORD-2026-0042 paid"
print(re.findall("ORD-\d{4}-\d{4}", log))
```
```bash
python rawbad.py
```
You should see:
```
rawbad.py:4: SyntaxWarning: "\d" is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\d"? A raw string is also an option.
  print(re.findall("ORD-\d{4}-\d{4}", log))
['ORD-2026-0042']
```

Run with the default settings, a recent Python prints the warning like this. It still finds the match this time, but the warning says it will stop working in the future, so write patterns as raw strings.

### 28. Putting it together: events per hour
`strptime` reads the time, `.hour` picks out the hour, and `Counter` counts the hours. This is the skeleton of the log analyser in the next video.

`together.py`:
```python
from collections import Counter
from datetime import datetime

times = ["18:05:10", "18:40:02", "19:01:55", "18:59:59"]
hours = []
for t in times:
    when = datetime.strptime(t, "%H:%M:%S")
    hours.append(when.hour)
print(Counter(hours))
```
```bash
python together.py
```
You should see:
```
Counter({18: 3, 19: 1})
```

### 29. Pitfall: shuffle returns None
`random.shuffle` changes the list itself and returns `None`, the same trap as `sort`.

`shufnone.py`:
```python
import random

students = ["Lukas", "Priya", "Meera"]
result = random.shuffle(students)
print(result)
```
```bash
python shufnone.py
```
You should see:
```
None
```

Shuffle the list itself, then use the list afterwards.

### 30. Try it yourself: days until your birthday
Write a script that prints how many days are left until your next birthday using `date` and `timedelta`, then prints that birthday as a weekday, a day and a month name. The video leaves this to you. One possible answer is below.

### Try it answer
`birthday_try.py` (not shown in the video; one possible answer, with a fixed "today" so the output repeats):
```python
from datetime import date

today = date(2026, 10, 25)  # fixed so the output repeats; use date.today() for real
birthday = date(today.year, 3, 14)  # Asha's birthday: 14 March
if birthday < today:
    birthday = date(today.year + 1, 3, 14)  # already passed this year: use next year

gap = birthday - today
print(f"{gap.days} days until my birthday")
print(birthday.strftime("%A, %d %B"))
```
```bash
python birthday_try.py
```
You should see:
```
140 days until my birthday
Sunday, 14 March
```

## Common mistakes
- `random.shuffle` changes the list and returns `None`: `result = random.shuffle(x)` makes `result` `None`.
- Mixing a naive and an aware datetime is a `TypeError`. Make both aware, or better, keep every stored time in UTC.
- A pattern that does not fit the text is a `ValueError`. And day first or month first changes the date silently, so agree on the order or use ISO format.
- `re.search` gives `None` when nothing matches. Check with `if found:` before calling `.group()`.
- Writing regex patterns without the `r` in front (raw string).
- Adding or subtracting hours by hand to change a time zone. Convert with `astimezone`.

## Clean up
Nothing to clean up. These scripts create no files.

## Next
[M06-B03 · Build a Log File Analyser](../m06-b03-build-a-log-file-analyser/)
