# Module 23 practice sheet: 50 interview questions and 10 build-it-yourself tasks

The last sheet of the course. **Part 1** is fifty questions that Python interviewers really ask (Q1 to Q40 and the ten gotchas G1 to G10), each with a model answer you can say out loud and a small program that proves it. **Part 2** is ten programs you build yourself, from a 30-line function to a short-link service with a database and a cache. Do it after the lessons [M23-L01](../../m23-interviews-and-capstone/m23-l01-the-python-gotchas/) to [M23-L04](../../m23-interviews-and-capstone/m23-l04-mock-interview-and-roadmap/) and the capstone [M23-B16](../../m23-interviews-and-capstone/m23-b16-capstone-course-copilot-lite/).

## How to use this sheet

1. Open [sheet.md](sheet.md). Read a question, answer it out loud in 30 seconds, and only then open the answer.
2. For code questions, predict the output first, then compare with the real output in the sheet.
3. For the ten tasks in Part 2, write your own solution and its tests before you open the worked answer.
4. The same code is in [solutions/](solutions/) as ready-to-run files.

## Before you start

- Python 3.14 or newer. Check with `python --version` (on Mac or Linux the command may be `python3`).
- Most questions use only the standard library. A few need packages (pytest, hypothesis, FastAPI, pydantic, SQLAlchemy, psycopg, argon2-cffi, Redis, httpx, uvicorn). Make a virtual environment and install the pinned versions:

```bash
cd practice/m23-interviews-and-capstone/solutions
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

- Docker (running) is needed only for Q34 to Q36, Q37, Q39 and tasks 9 and 10. The sheet shows the two demo containers (Postgres 17 and Redis 8, demo passwords) and how to remove them. Remove them when you finish: `docker rm -f -v m23p04-pg m23p04-redis`.

## Run a solution

From inside `solutions/` with the virtual environment active:

```bash
python Q01.py
python -m pytest test_Q16_fixtures.py test_Q16_mock.py test_Q30.py -v
python -m pytest T01_word_stats -v
sh Q39.sh                          # needs Docker
```

Timings (Q4, Q17, Q29, Q33, Q36, G10) and the race-condition count in Q17 are different on every machine. Look at the shape (which is faster), not the digits. A `StarletteDeprecationWarning` about `httpx` is only a warning.

## Files in this folder

| File | What it is |
|------|------------|
| `sheet.md` | The sheet: questions, model answers, code, real output, and the ten tasks |
| `solutions/requirements.txt`, `solutions/pytest.ini` | Pinned packages, and the setting that lets each test import its own module |
| `solutions/Q01.py` to `Q15.py`, `Q17.py` to `Q29.py`, `Q31.py`, `Q32.py`, `Q38.py`, `Q40.py` | One script per question (standard library, or the pinned packages) |
| `solutions/test_Q16_fixtures.py`, `test_Q16_mock.py`, `Q16_app/` | Q16: pytest fixtures, parametrize and mocking |
| `solutions/test_Q30.py` | Q30: what makes a good test |
| `solutions/Q33.py`, `Q33_server.py` | Q33: `def` or `async def`, measured against a real local server |
| `solutions/Q34.py` to `Q36.py` | Q34 to Q36: N+1 queries, transactions, indexes (Postgres in Docker) |
| `solutions/Q37.py` | Q37: cache-aside (Redis in Docker) |
| `solutions/Q39.sh`, `Q39_docker/` | Q39: a non-root container configured by environment variables (Docker) |
| `solutions/G01_default.py` to `G10_gil.py` | The ten gotchas (two files for gotcha 6) |
| `solutions/T01_word_stats/` to `T07_async_checker/` | Tasks 1 to 7: code plus tests, no services |
| `solutions/T08_catalog_api/` | Task 8: a FastAPI catalogue API |
| `solutions/T09_enrollment_db/`, `T10_short_links/` | Tasks 9 and 10: Postgres, and Postgres plus Redis (Docker) |

## Next

You have finished the course. Go back to the [repository root](../../README.md).
