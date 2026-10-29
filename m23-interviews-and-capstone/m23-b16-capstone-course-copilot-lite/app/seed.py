import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import engine
from app.models import Lesson, User
from app.search import index_lesson
from app.security import hash_password

TOPICS = """
M02-L01|Variables as Labels on Boxes|variable, label, assignment, name, value, box
M03-L01|Making Decisions with if|if, else, condition, branch, True, False
M03-L04|Repeating with for and range|loop, range, iteration, counter, repeat, body
M04-L01|Functions as Recipes|function, def, return, argument, call, recipe
M05-L01|Lists|list, append, index, slice, sort, items
M05-L03|Dictionaries|dictionary, key, value, lookup, get, pairs
M05-L06|Names, Objects and Mutability|mutable, copy, object, identity, alias, name
M06-L03|Exceptions|exception, try, except, traceback, error, finally
M07-L03|Virtual Environments and uv Projects|virtual environment, uv, package, lock file, install, project
M08-L01|Classes and Objects|class, object, method, instance, attribute, self
M09-L02|Generators|generator, yield, lazy, iterator, memory, stream
M09-L03|Closures and Decorators|decorator, closure, wrapper, function, timer, retry
M10-L01|Type Hints|type hint, annotation, checker, mistake, signature, pyright
M11-L03|The GIL and Free-Threaded Python|GIL, thread, lock, free-threaded, parallel, cores
M11-L04|Measuring and Improving Speed|speed, profile, timeit, slow code, measure, faster
M12-L02|Threads|thread, waiting, network, pool, shared data, race
M12-L04|asyncio from Scratch|asyncio, await, coroutine, event loop, waiting, tasks
M13-L01|Your First pytest Tests|test, assert, pytest, failure, fixture, green
M13-L03|Mocking|mock, fake, patch, dependency, test, isolate
M14-L03|Logging the Right Way|logging, level, handler, message, structured, debug
M15-L01|How the Web Works and Your First Endpoint|request, response, endpoint, route, status code, server
M15-L03|Pydantic Models|pydantic, validation, model, field, schema, error
M15-L05|Dependencies, Routers and Middleware|dependency, router, middleware, Depends, request, shared
M16-L01|SQL and PostgreSQL in Docker|SQL, table, select, index, row, Postgres
M16-L03|Relationships and the N+1 Problem|relationship, join, query, loading, foreign key, slow
M16-L04|Migrations with Alembic and Transactions|migration, alembic, schema, transaction, rollback, commit
M17-L01|Passwords Done Right|password, hash, salt, argon, login, secret
M17-L02|Sessions, JWT and OAuth2|token, JWT, session, login, signature, expiry
M17-L03|Authorisation and the OWASP API Top 10|role, permission, owner, access, attack, check
M18-L01|Redis and Caching|cache, Redis, expiry, stale, hit, invalidate
M18-L02|Background Jobs with Celery|Celery, worker, queue, job, retry, broker
M18-L04|Rate Limiting and Resilience|rate limit, window, 429, retry, backoff, timeout
M19-L01|Docker for Python Apps|Docker, image, container, Dockerfile, layer, non-root
M19-L02|Configuration the 12-Factor Way|settings, environment, secret, config, twelve factor, default
M19-L03|CI-CD with GitHub Actions|workflow, pipeline, job, matrix, green build, deploy
M20-L01|Health Checks, Metrics and Dashboards|health check, metric, counter, dashboard, latency, alert
M20-L04|Making It Faster|bottleneck, index, query, speed, profile, measure
M21-L01|Command-Line Tools|command line, argument, option, typer, help, script
M22-L01|Automating the Boring Stuff|automation, files, schedule, cron, email, spreadsheet
M22-L03|Data Analysis Taster|pandas, dataframe, column, groupby, chart, numbers
"""
OPENERS = [
    "This lesson is about {a} and {b}.",
    "Start with {a}: it is the heart of the lesson.",
    "Here you learn how {a} works with {b}.",
]
MIDDLES = [
    "Remember that {a} and {b} always go together.",
    "A common mistake is to forget {a} when you use {b}.",
    "Try a small example with {a}, then change {b}.",
]
CLOSERS = [
    "In an interview, explain {a} in one plain sentence.",
    "Practise {a} until it feels boring, then add {b}.",
    "Next time, check {a} before you touch {b}.",
]


def make_notes(rng, words):
    words = rng.sample(words, len(words))
    parts = []
    for options in (OPENERS, MIDDLES, CLOSERS):
        a, b = words.pop(), words.pop()
        parts.append(rng.choice(options).format(a=a, b=b))
    return " ".join(parts)


def seed_lessons(session):
    rng = random.Random(23)
    for row in TOPICS.strip().splitlines():
        code, title, words = row.split("|")
        notes = make_notes(rng, words.split(", "))
        found = session.scalar(
            select(Lesson).where(Lesson.code == code)
        )
        if found:
            continue
        lesson = Lesson(code=code, title=title, notes=notes)
        session.add(lesson)
        session.flush()
        index_lesson(session, lesson.id)


def seed_users(session):
    people = [
        ("meera@allcsvideos.com", "Meera", "admin"),
        ("lukas@allcsvideos.com", "Lukas", "student"),
        ("priya@allcsvideos.com", "Priya", "student"),
    ]
    for email, name, role in people:
        if session.scalar(
            select(User).where(User.email == email)
        ):
            continue
        password = hash_password("demo-password-23")
        session.add(
            User(
                email=email,
                name=name,
                role=role,
                password_hash=password,
            )
        )


def main():
    with Session(engine) as session:
        seed_lessons(session)
        seed_users(session)
        session.commit()


if __name__ == "__main__":
    main()
