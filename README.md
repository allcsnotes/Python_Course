# Python Course: From Zero to Production, Interview Ready

The companion repo for the **AllCsVideos Python course**: 23 modules, 120 videos, one running story (Asha, Lukas, Priya and Meera building the allcsvideos platform), from your first `print` to a tested, typed, secured, containerised Python backend and a coding interview.

Every video has a folder here with its files and a step-by-step guide, so you can repeat on your own laptop exactly what the video does.

---

## How to use this repo

1. **Clone it once:**
   ```bash
   git clone https://github.com/allcsnotes/Python_Course.git
   cd Python_Course
   ```
2. **Watch a lecture**, then open its folder (see the [lesson index](#lesson-index) below, or the **Resources** link on the lecture page).
3. **Open the folder's `README.md` and follow it top to bottom.** Every lesson README has the same parts:

   | Part | What it gives you |
   |---|---|
   | What you'll learn | the goal of the lecture in a few bullets |
   | Before you start | what to install, and which earlier lesson you need |
   | Files in this folder | what each file is for |
   | Follow along | every command, in the order the video runs it, with the output you should see |
   | Common mistakes | the traps the video warns about |
   | Clean up | how to remove only what this lesson created |
   | Next | a link to the next lecture |

   Lectures that are mostly ideas have **Key ideas** and **Try it yourself** instead.
4. **Get updates** later with `git pull`.

> Work on a **copy** when a lesson changes files. Your clone stays clean, and `git pull` keeps working.

---

## What to install, module by module

You do **not** need everything on day one.

| Modules | Install before you start | Notes |
|---|---|---|
| **M01-M12** | Python **3.14** (the course uses 3.14; newer works), a code editor (VS Code) | [M01-L02](m01-getting-started/m01-l02-setting-up-your-tools/) walks through it, including `uv` |
| **M13-M15** | Nothing new beyond the packages each lesson installs in a virtual environment | pytest, Ruff, FastAPI |
| **M16-M20** | **Docker Desktop** | PostgreSQL, Redis, mail catcher, Kafka and the observability tools run as pinned containers, so nothing else is installed on your laptop |
| **M19** | Optional: a free GitHub account | The AWS parts are shown, never required; each lesson says what costs money |
| **M21-M23** | Everything above | Packages are published only to a local test server, never to the real PyPI |

**On Windows**, use the Python installer from python.org, or WSL 2 with Docker Desktop's WSL integration. Commands say `python`; on macOS and Linux you may need `python3`.

**Versions are pinned.** Packages and Docker images use the exact versions from the video (never `:latest`). Numbers that depend on your machine (timings, ids, memory addresses, ports in use) will differ, and the READMEs say so.

---

## Safety first

- **Every password, key, token and email in this repo is fake** and labelled as a demo value. Never put real secrets in your copy.
- Scraping, email and publishing exercises use **local stand-ins** (a local site, a mail catcher, a local package server). Nothing here contacts a real site or sends real mail.
- **Clean up after Docker lessons.** Each README ends with commands that remove only what that lesson created.

---

## Repo layout

Each module has a folder (`m05-data-structures/`); each lesson has a folder named after its video (`m05-l03-dictionaries/`). In each module the lessons (L) come first, then the build (B) that puts them together.

**Practice:** after Modules 2, 5, 8 and 23 there are practice sheets with worked answers. See [`practice/`](practice/README.md).

---

## Lesson index


**M01 · Getting Started** · folder [`m01-getting-started/`](m01-getting-started/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | What is Programming and Why Python | Lesson | [m01-l01-what-is-programming-and-why-python](m01-getting-started/m01-l01-what-is-programming-and-why-python/) |
| L02 | Setting Up Your Tools | Lesson | [m01-l02-setting-up-your-tools](m01-getting-started/m01-l02-setting-up-your-tools/) |
| L03 | Your First Program | Lesson | [m01-l03-your-first-program](m01-getting-started/m01-l03-your-first-program/) |
| L04 | What Happens When You Run Python | Lesson | [m01-l04-what-happens-when-you-run-python](m01-getting-started/m01-l04-what-happens-when-you-run-python/) |

**M02 · Variables and Data Types** · folder [`m02-variables-and-data-types/`](m02-variables-and-data-types/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Variables as Labels on Boxes | Lesson | [m02-l01-variables-as-labels-on-boxes](m02-variables-and-data-types/m02-l01-variables-as-labels-on-boxes/) |
| L02 | Numbers | Lesson | [m02-l02-numbers](m02-variables-and-data-types/m02-l02-numbers/) |
| L03 | Text and Strings | Lesson | [m02-l03-text-and-strings](m02-variables-and-data-types/m02-l03-text-and-strings/) |
| L04 | True, False and None | Lesson | [m02-l04-true-false-and-none](m02-variables-and-data-types/m02-l04-true-false-and-none/) |
| L05 | Input and Output | Lesson | [m02-l05-input-and-output](m02-variables-and-data-types/m02-l05-input-and-output/) |

**M03 · Decisions and Loops** · folder [`m03-decisions-and-loops/`](m03-decisions-and-loops/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Making Decisions with if | Lesson | [m03-l01-making-decisions-with-if](m03-decisions-and-loops/m03-l01-making-decisions-with-if/) |
| L02 | Comparing and Combining | Lesson | [m03-l02-comparing-and-combining](m03-decisions-and-loops/m03-l02-comparing-and-combining/) |
| L03 | Repeating with while | Lesson | [m03-l03-repeating-with-while](m03-decisions-and-loops/m03-l03-repeating-with-while/) |
| L04 | Repeating with for and range | Lesson | [m03-l04-repeating-with-for-and-range](m03-decisions-and-loops/m03-l04-repeating-with-for-and-range/) |
| L05 | Nested Loops and match | Lesson | [m03-l05-nested-loops-and-match](m03-decisions-and-loops/m03-l05-nested-loops-and-match/) |
| B01 | A Number Guessing Game | Build | [m03-b01-build-a-number-guessing-game](m03-decisions-and-loops/m03-b01-build-a-number-guessing-game/) |

**M04 · Functions** · folder [`m04-functions/`](m04-functions/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Functions as Recipes | Lesson | [m04-l01-functions-as-recipes](m04-functions/m04-l01-functions-as-recipes/) |
| L02 | Parameters and Arguments | Lesson | [m04-l02-parameters-and-arguments](m04-functions/m04-l02-parameters-and-arguments/) |
| L03 | args and kwargs | Lesson | [m04-l03-args-and-kwargs](m04-functions/m04-l03-args-and-kwargs/) |
| L04 | Scope: What a Function Can See | Lesson | [m04-l04-scope-what-a-function-can-see](m04-functions/m04-l04-scope-what-a-function-can-see/) |
| L05 | Recursion and Lambdas | Lesson | [m04-l05-recursion-and-lambdas](m04-functions/m04-l05-recursion-and-lambdas/) |

**M05 · Data Structures** · folder [`m05-data-structures/`](m05-data-structures/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Lists | Lesson | [m05-l01-lists](m05-data-structures/m05-l01-lists/) |
| L02 | Tuples and Unpacking | Lesson | [m05-l02-tuples-and-unpacking](m05-data-structures/m05-l02-tuples-and-unpacking/) |
| L03 | Dictionaries | Lesson | [m05-l03-dictionaries](m05-data-structures/m05-l03-dictionaries/) |
| L04 | Sets | Lesson | [m05-l04-sets](m05-data-structures/m05-l04-sets/) |
| L05 | Comprehensions | Lesson | [m05-l05-comprehensions](m05-data-structures/m05-l05-comprehensions/) |
| L06 | Names, Objects and Mutability | Lesson | [m05-l06-names-objects-and-mutability](m05-data-structures/m05-l06-names-objects-and-mutability/) |
| B02 | An Expense Tracker | Build | [m05-b02-build-an-expense-tracker](m05-data-structures/m05-b02-build-an-expense-tracker/) |

**M06 · Files, Text and Errors** · folder [`m06-files-text-and-errors/`](m06-files-text-and-errors/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Reading and Writing Files | Lesson | [m06-l01-reading-and-writing-files](m06-files-text-and-errors/m06-l01-reading-and-writing-files/) |
| L02 | CSV and JSON | Lesson | [m06-l02-csv-and-json](m06-files-text-and-errors/m06-l02-csv-and-json/) |
| L03 | Exceptions | Lesson | [m06-l03-exceptions](m06-files-text-and-errors/m06-l03-exceptions/) |
| L04 | Raising and Designing Errors | Lesson | [m06-l04-raising-and-designing-errors](m06-files-text-and-errors/m06-l04-raising-and-designing-errors/) |
| L05 | Dates, Times and the Standard Library Tour | Lesson | [m06-l05-dates-times-and-the-standard-library-tour](m06-files-text-and-errors/m06-l05-dates-times-and-the-standard-library-tour/) |
| B03 | A Log File Analyser | Build | [m06-b03-build-a-log-file-analyser](m06-files-text-and-errors/m06-b03-build-a-log-file-analyser/) |

**M07 · Modules, Packages and Environments** · folder [`m07-modules-packages-and-environments/`](m07-modules-packages-and-environments/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Splitting Code into Modules | Lesson | [m07-l01-splitting-code-into-modules](m07-modules-packages-and-environments/m07-l01-splitting-code-into-modules/) |
| L02 | Packages and Project Layout | Lesson | [m07-l02-packages-and-project-layout](m07-modules-packages-and-environments/m07-l02-packages-and-project-layout/) |
| L03 | Virtual Environments and uv Projects | Lesson | [m07-l03-virtual-environments-and-uv-projects](m07-modules-packages-and-environments/m07-l03-virtual-environments-and-uv-projects/) |
| L04 | Third-Party Packages and PyPI | Lesson | [m07-l04-third-party-packages-and-pypi](m07-modules-packages-and-environments/m07-l04-third-party-packages-and-pypi/) |

**M08 · Object-Oriented Programming** · folder [`m08-object-oriented-programming/`](m08-object-oriented-programming/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Classes and Objects | Lesson | [m08-l01-classes-and-objects](m08-object-oriented-programming/m08-l01-classes-and-objects/) |
| L02 | Attributes and Methods | Lesson | [m08-l02-attributes-and-methods](m08-object-oriented-programming/m08-l02-attributes-and-methods/) |
| L03 | Encapsulation and Properties | Lesson | [m08-l03-encapsulation-and-properties](m08-object-oriented-programming/m08-l03-encapsulation-and-properties/) |
| L04 | Inheritance and Composition | Lesson | [m08-l04-inheritance-and-composition](m08-object-oriented-programming/m08-l04-inheritance-and-composition/) |
| L05 | Dunder Methods | Lesson | [m08-l05-dunder-methods](m08-object-oriented-programming/m08-l05-dunder-methods/) |
| L06 | Dataclasses, Enums and Abstract Classes | Lesson | [m08-l06-dataclasses-enums-and-abstract-classes](m08-object-oriented-programming/m08-l06-dataclasses-enums-and-abstract-classes/) |
| B04 | The allcsvideos Domain Model | Build | [m08-b04-build-the-allcsvideos-domain-model](m08-object-oriented-programming/m08-b04-build-the-allcsvideos-domain-model/) |

**M09 · Writing Pythonic Code** · folder [`m09-writing-pythonic-code/`](m09-writing-pythonic-code/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Iterables and Iterators | Lesson | [m09-l01-iterables-and-iterators](m09-writing-pythonic-code/m09-l01-iterables-and-iterators/) |
| L02 | Generators | Lesson | [m09-l02-generators](m09-writing-pythonic-code/m09-l02-generators/) |
| L03 | Closures and Decorators | Lesson | [m09-l03-closures-and-decorators](m09-writing-pythonic-code/m09-l03-closures-and-decorators/) |
| L04 | Context Managers | Lesson | [m09-l04-context-managers](m09-writing-pythonic-code/m09-l04-context-managers/) |
| L05 | Standard Library Power Tools | Lesson | [m09-l05-standard-library-power-tools](m09-writing-pythonic-code/m09-l05-standard-library-power-tools/) |
| B05 | A Decorator Toolkit | Build | [m09-b05-build-a-decorator-toolkit](m09-writing-pythonic-code/m09-b05-build-a-decorator-toolkit/) |

**M10 · Type Hints and Modern Python** · folder [`m10-type-hints-and-modern-python/`](m10-type-hints-and-modern-python/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Type Hints | Lesson | [m10-l01-type-hints](m10-type-hints-and-modern-python/m10-l01-type-hints/) |
| L02 | Checking Types with Pyright, Generics and Protocol | Lesson | [m10-l02-checking-types-with-pyright-generics-and-protocol](m10-type-hints-and-modern-python/m10-l02-checking-types-with-pyright-generics-and-protocol/) |
| L03 | TypedDict, Slots, NamedTuple and Pattern Matching | Lesson | [m10-l03-typeddict-slots-namedtuple-and-pattern-matching](m10-type-hints-and-modern-python/m10-l03-typeddict-slots-namedtuple-and-pattern-matching/) |
| L04 | What's New in Modern Python | Lesson | [m10-l04-whats-new-in-modern-python](m10-type-hints-and-modern-python/m10-l04-whats-new-in-modern-python/) |

**M11 · Python Under the Hood** · folder [`m11-python-under-the-hood/`](m11-python-under-the-hood/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Everything Is an Object | Lesson | [m11-l01-everything-is-an-object](m11-python-under-the-hood/m11-l01-everything-is-an-object/) |
| L02 | Memory and Garbage Collection | Lesson | [m11-l02-memory-and-garbage-collection](m11-python-under-the-hood/m11-l02-memory-and-garbage-collection/) |
| L03 | The GIL and Free-Threaded Python | Lesson | [m11-l03-the-gil-and-free-threaded-python](m11-python-under-the-hood/m11-l03-the-gil-and-free-threaded-python/) |
| L04 | Measuring and Improving Speed | Lesson | [m11-l04-measuring-and-improving-speed](m11-python-under-the-hood/m11-l04-measuring-and-improving-speed/) |

**M12 · Concurrency** · folder [`m12-concurrency/`](m12-concurrency/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | CPU-Bound vs IO-Bound | Lesson | [m12-l01-cpu-bound-vs-io-bound](m12-concurrency/m12-l01-cpu-bound-vs-io-bound/) |
| L02 | Threads | Lesson | [m12-l02-threads](m12-concurrency/m12-l02-threads/) |
| L03 | Processes | Lesson | [m12-l03-processes](m12-concurrency/m12-l03-processes/) |
| L04 | asyncio from Scratch | Lesson | [m12-l04-asyncio-from-scratch](m12-concurrency/m12-l04-asyncio-from-scratch/) |
| L05 | Async in Practice | Lesson | [m12-l05-async-in-practice](m12-concurrency/m12-l05-async-in-practice/) |
| B06 | A Concurrent Link Checker | Build | [m12-b06-build-a-concurrent-link-checker](m12-concurrency/m12-b06-build-a-concurrent-link-checker/) |

**M13 · Testing** · folder [`m13-testing/`](m13-testing/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Your First pytest Tests | Lesson | [m13-l01-your-first-pytest-tests](m13-testing/m13-l01-your-first-pytest-tests/) |
| L02 | Fixtures and Parametrize | Lesson | [m13-l02-fixtures-and-parametrize](m13-testing/m13-l02-fixtures-and-parametrize/) |
| L03 | Mocking | Lesson | [m13-l03-mocking](m13-testing/m13-l03-mocking/) |
| L04 | Coverage and Property-Based Testing | Lesson | [m13-l04-coverage-and-property-based-testing](m13-testing/m13-l04-coverage-and-property-based-testing/) |
| L05 | Test-Driven Development | Lesson | [m13-l05-test-driven-development](m13-testing/m13-l05-test-driven-development/) |
| B07 | A Shopping Cart with TDD | Build | [m13-b07-build-a-shopping-cart-with-tdd](m13-testing/m13-b07-build-a-shopping-cart-with-tdd/) |

**M14 · Code Quality, Logging and Debugging** · folder [`m14-code-quality-logging-and-debugging/`](m14-code-quality-logging-and-debugging/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Clean Code, Ruff and pre-commit | Lesson | [m14-l01-clean-code-ruff-and-pre-commit](m14-code-quality-logging-and-debugging/m14-l01-clean-code-ruff-and-pre-commit/) |
| L02 | Debugging | Lesson | [m14-l02-debugging](m14-code-quality-logging-and-debugging/m14-l02-debugging/) |
| L03 | Logging the Right Way | Lesson | [m14-l03-logging-the-right-way](m14-code-quality-logging-and-debugging/m14-l03-logging-the-right-way/) |
| L04 | Design Patterns the Python Way | Lesson | [m14-l04-design-patterns-the-python-way](m14-code-quality-logging-and-debugging/m14-l04-design-patterns-the-python-way/) |

**M15 · Web APIs with FastAPI** · folder [`m15-web-apis-with-fastapi/`](m15-web-apis-with-fastapi/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | How the Web Works and Your First Endpoint | Lesson | [m15-l01-how-the-web-works-and-your-first-endpoint](m15-web-apis-with-fastapi/m15-l01-how-the-web-works-and-your-first-endpoint/) |
| L02 | Parameters, Bodies and Responses | Lesson | [m15-l02-parameters-bodies-and-responses](m15-web-apis-with-fastapi/m15-l02-parameters-bodies-and-responses/) |
| L03 | Pydantic Models | Lesson | [m15-l03-pydantic-models](m15-web-apis-with-fastapi/m15-l03-pydantic-models/) |
| L04 | Errors Done Right | Lesson | [m15-l04-errors-done-right](m15-web-apis-with-fastapi/m15-l04-errors-done-right/) |
| L05 | Dependencies, Routers and Middleware | Lesson | [m15-l05-dependencies-routers-and-middleware](m15-web-apis-with-fastapi/m15-l05-dependencies-routers-and-middleware/) |
| L06 | Async Endpoints, Background Tasks and Docs | Lesson | [m15-l06-async-endpoints-background-tasks-and-docs](m15-web-apis-with-fastapi/m15-l06-async-endpoints-background-tasks-and-docs/) |
| B08 | A Course Catalog API | Build | [m15-b08-build-a-course-catalog-api](m15-web-apis-with-fastapi/m15-b08-build-a-course-catalog-api/) |

**M16 · Databases** · folder [`m16-databases/`](m16-databases/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | SQL and PostgreSQL in Docker | Lesson | [m16-l01-sql-and-postgresql-in-docker](m16-databases/m16-l01-sql-and-postgresql-in-docker/) |
| L02 | SQLAlchemy Core Ideas | Lesson | [m16-l02-sqlalchemy-core-ideas](m16-databases/m16-l02-sqlalchemy-core-ideas/) |
| L03 | Relationships and the N+1 Problem | Lesson | [m16-l03-relationships-and-the-n-1-problem](m16-databases/m16-l03-relationships-and-the-n-1-problem/) |
| L04 | Migrations with Alembic and Transactions | Lesson | [m16-l04-migrations-with-alembic-and-transactions](m16-databases/m16-l04-migrations-with-alembic-and-transactions/) |
| L05 | Async SQLAlchemy and Connection Pools | Lesson | [m16-l05-async-sqlalchemy-and-connection-pools](m16-databases/m16-l05-async-sqlalchemy-and-connection-pools/) |
| B09 | allcsvideos Backend v1 | Build | [m16-b09-build-allcsvideos-backend-v1](m16-databases/m16-b09-build-allcsvideos-backend-v1/) |

**M17 · Security and Authentication** · folder [`m17-security-and-authentication/`](m17-security-and-authentication/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Passwords Done Right | Lesson | [m17-l01-passwords-done-right](m17-security-and-authentication/m17-l01-passwords-done-right/) |
| L02 | Sessions, JWT and OAuth2 | Lesson | [m17-l02-sessions-jwt-and-oauth2](m17-security-and-authentication/m17-l02-sessions-jwt-and-oauth2/) |
| L03 | Authorisation and the OWASP API Top 10 | Lesson | [m17-l03-authorisation-and-the-owasp-api-top-10](m17-security-and-authentication/m17-l03-authorisation-and-the-owasp-api-top-10/) |
| L04 | Input Attacks and Secrets | Lesson | [m17-l04-input-attacks-and-secrets](m17-security-and-authentication/m17-l04-input-attacks-and-secrets/) |
| B10 | Secure allcsvideos | Build | [m17-b10-build-secure-allcsvideos](m17-security-and-authentication/m17-b10-build-secure-allcsvideos/) |

**M18 · Caching, Background Jobs and Messaging** · folder [`m18-caching-background-jobs-and-messaging/`](m18-caching-background-jobs-and-messaging/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Redis and Caching | Lesson | [m18-l01-redis-and-caching](m18-caching-background-jobs-and-messaging/m18-l01-redis-and-caching/) |
| L02 | Background Jobs with Celery | Lesson | [m18-l02-background-jobs-with-celery](m18-caching-background-jobs-and-messaging/m18-l02-background-jobs-with-celery/) |
| L03 | Events and Messages | Lesson | [m18-l03-events-and-messages](m18-caching-background-jobs-and-messaging/m18-l03-events-and-messages/) |
| L04 | Rate Limiting and Resilience | Lesson | [m18-l04-rate-limiting-and-resilience](m18-caching-background-jobs-and-messaging/m18-l04-rate-limiting-and-resilience/) |
| B11 | A URL Shortener | Build | [m18-b11-build-a-url-shortener](m18-caching-background-jobs-and-messaging/m18-b11-build-a-url-shortener/) |
| B12 | An Enrollment Email Worker | Build | [m18-b12-build-an-enrollment-email-worker](m18-caching-background-jobs-and-messaging/m18-b12-build-an-enrollment-email-worker/) |

**M19 · Docker, CI/CD and Deployment** · folder [`m19-docker-ci-cd-and-deployment/`](m19-docker-ci-cd-and-deployment/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Docker for Python Apps | Lesson | [m19-l01-docker-for-python-apps](m19-docker-ci-cd-and-deployment/m19-l01-docker-for-python-apps/) |
| L02 | Configuration the 12-Factor Way | Lesson | [m19-l02-configuration-the-12-factor-way](m19-docker-ci-cd-and-deployment/m19-l02-configuration-the-12-factor-way/) |
| L03 | CI-CD with GitHub Actions | Lesson | [m19-l03-ci-cd-with-github-actions](m19-docker-ci-cd-and-deployment/m19-l03-ci-cd-with-github-actions/) |
| L04 | Running in Production | Lesson | [m19-l04-running-in-production](m19-docker-ci-cd-and-deployment/m19-l04-running-in-production/) |
| B13 | A Deployment Pipeline | Build | [m19-b13-build-a-deployment-pipeline](m19-docker-ci-cd-and-deployment/m19-b13-build-a-deployment-pipeline/) |

**M20 · Observability and Performance** · folder [`m20-observability-and-performance/`](m20-observability-and-performance/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Health Checks, Metrics and Dashboards | Lesson | [m20-l01-health-checks-metrics-and-dashboards](m20-observability-and-performance/m20-l01-health-checks-metrics-and-dashboards/) |
| L02 | Tracing with OpenTelemetry | Lesson | [m20-l02-tracing-with-opentelemetry](m20-observability-and-performance/m20-l02-tracing-with-opentelemetry/) |
| L03 | Finding Slow Code | Lesson | [m20-l03-finding-slow-code](m20-observability-and-performance/m20-l03-finding-slow-code/) |
| L04 | Making It Faster | Lesson | [m20-l04-making-it-faster](m20-observability-and-performance/m20-l04-making-it-faster/) |

**M21 · Packaging, CLIs and Libraries** · folder [`m21-packaging-clis-and-libraries/`](m21-packaging-clis-and-libraries/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Command-Line Tools | Lesson | [m21-l01-command-line-tools](m21-packaging-clis-and-libraries/m21-l01-command-line-tools/) |
| L02 | Building and Publishing a Package | Lesson | [m21-l02-building-and-publishing-a-package](m21-packaging-clis-and-libraries/m21-l02-building-and-publishing-a-package/) |
| L03 | Working with Other People's Code | Lesson | [m21-l03-working-with-other-peoples-code](m21-packaging-clis-and-libraries/m21-l03-working-with-other-peoples-code/) |
| B14 | Publish allcsv-cli | Build | [m21-b14-build-and-publish-allcsv-cli](m21-packaging-clis-and-libraries/m21-b14-build-and-publish-allcsv-cli/) |

**M22 · Data and Automation with Python** · folder [`m22-data-and-automation-with-python/`](m22-data-and-automation-with-python/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | Automating the Boring Stuff | Lesson | [m22-l01-automating-the-boring-stuff](m22-data-and-automation-with-python/m22-l01-automating-the-boring-stuff/) |
| L02 | Web Scraping and APIs | Lesson | [m22-l02-web-scraping-and-apis](m22-data-and-automation-with-python/m22-l02-web-scraping-and-apis/) |
| L03 | Data Analysis Taster | Lesson | [m22-l03-data-analysis-taster](m22-data-and-automation-with-python/m22-l03-data-analysis-taster/) |
| B15 | A Weekly Report Bot | Build | [m22-b15-build-a-weekly-report-bot](m22-data-and-automation-with-python/m22-b15-build-a-weekly-report-bot/) |

**M23 · Interviews and Capstone** · folder [`m23-interviews-and-capstone/`](m23-interviews-and-capstone/)

| # | Lesson | Type | Folder |
|---|---|---|---|
| L01 | The Python Gotchas | Lesson | [m23-l01-the-python-gotchas](m23-interviews-and-capstone/m23-l01-the-python-gotchas/) |
| L02 | The Coding Round Toolkit | Lesson | [m23-l02-the-coding-round-toolkit](m23-interviews-and-capstone/m23-l02-the-coding-round-toolkit/) |
| L03 | The Backend Interview Round | Lesson | [m23-l03-the-backend-interview-round](m23-interviews-and-capstone/m23-l03-the-backend-interview-round/) |
| L04 | Mock Interview and Roadmap | Lesson | [m23-l04-mock-interview-and-roadmap](m23-interviews-and-capstone/m23-l04-mock-interview-and-roadmap/) |
| B16 | Capstone: Course Copilot-lite | Build | [m23-b16-capstone-course-copilot-lite](m23-interviews-and-capstone/m23-b16-capstone-course-copilot-lite/) |
