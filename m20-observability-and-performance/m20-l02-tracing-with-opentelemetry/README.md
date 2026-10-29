# M20-L02 · Tracing with OpenTelemetry

> Video: Module 20, Lesson 2. Watch it first, then follow along here.

## What you'll learn

- What a trace and a span are, and how a trace ID follows one request through the API, Postgres, Redis, the queue and the worker
- How to set up OpenTelemetry (tracer provider, batch exporter) and use ready-made instrumentation for FastAPI, the Postgres driver, Redis, HTTPX and Celery
- How to add a manual span and attributes for your own steps (and what never to put in an attribute)
- How context propagation (the `traceparent` header and the message in the queue) joins the worker's spans to the server's trace
- How to put the trace ID in every log line, in the `X-Request-ID` header and in the error body (the "error id" is the trace id)
- How sampling keeps the cost small, with two environment variables and no code change

## Before you start

- Docker with `docker compose` running, and Python 3.14 on the host for two small scripts that only use the standard library (`python --version`).
- This lesson continues the backend of M20-L01. The folder `allcs/` is that backend plus `app/tracing.py`, `app/web_tracing.py` and a Jaeger container.
- Images (pinned): `jaegertracing/jaeger:2.22.0`, `postgres:17.11`, `redis:8`, `axllent/mailpit:v1.32.0`, and `ghcr.io/astral-sh/uv:0.13` for the API image. The compose project is `m20l02`. Host ports: API 8202, Jaeger UI 20162, Postgres 20502, Redis 20402. All keys and passwords are demo values.
- Timings, span start offsets and trace ids differ on every run, so yours will differ.

```bash
cd allcs
docker compose up -d --build
sleep 8
docker compose ps --format "table {{.Service}}\t{{.Status}}"
docker compose exec -T api python - < ../seed.py
```

```
SERVICE   STATUS
api       Up 8 seconds (healthy)
db        Up 10 seconds (healthy)
jaeger    Up 10 seconds
mail      Up 10 seconds (healthy)
redis     Up 10 seconds (healthy)
worker    Up 8 seconds
seeded
```

(The first start builds the image. The seed makes Lukas, Priya and Meera, with the demo password `<name>-demo-pass`, and two courses.) Get two tokens for the curl calls below:

```bash
U=localhost:8202
tok(){ curl -s -d "username=$1@example.com&password=$1-demo-pass" $U/auth/login | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])"; }
L=$(tok lukas); PR=$(tok priya)
```

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/app/tracing.py` | `start(service)`: tracer provider with the service name and a batch OTLP exporter; `TraceIdFilter` and `setup_logging()` put the trace id in every log line |
| `allcs/app/web_tracing.py` | `install(app)`: starts tracing, a middleware that sets `X-Request-ID` to the trace id, and the instrumentation for FastAPI, Postgres (psycopg), Redis, HTTPX and Celery |
| `allcs/app/worker.py` | The worker starts its own tracing when each worker process starts (a Celery signal), with the service name `allcs-worker` |
| `allcs/app/routers/enrollments.py` | A manual span `course.title` with the attribute `cache.hit` |
| `allcs/app/errors.py` | `server_error()`: the error id in a 500 is the trace id |
| `allcs/app/demo.py` | The lesson-only `/boom` route (divides by zero) |
| `allcs/compose.yaml` | The stack with Jaeger; the app gets `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_SERVICE_NAME` and the two sampler settings |
| `seed.py` | Demo data |
| `spans.py` | Asks the Jaeger API for one trace and prints its spans (service, start in ms, duration in ms, name, SQL) |
| `count_traces.py` | Counts the traces of `GET /courses` that Jaeger has kept (for the sampling demo) |

## Follow along

### 1. The idea

A parcel has a tracking number; at every stop a scanner writes where and how long. One request is one parcel: the tracking number is the trace ID, and each stop is a span (a name, a start time, a duration). Spans sit inside each other like boxes, and along a time line they make a waterfall picture. Context propagation means passing the tracking number along when one program calls another; in HTTP it travels in a header called `traceparent`. Three pieces make it work: the OpenTelemetry library inside the app (makes spans), an exporter (sends finished spans out with the standard OTLP protocol), and Jaeger (stores and shows them).

### 2. The setup code

`app/tracing.py` creates a `TracerProvider` with the service name and adds a `BatchSpanProcessor` with an `OTLPSpanExporter` (which reads its address from `OTEL_EXPORTER_OTLP_ENDPOINT`, here `http://jaeger:4318`). `app/web_tracing.py` calls the ready-made instrumentation (code that wraps a library and makes spans for you, with no change in your routes): `FastAPIInstrumentor`, `PsycopgInstrumentor`, `RedisInstrumentor`, `HTTPXClientInstrumentor`, `CeleryInstrumentor`. An honest note from the video: the SQLAlchemy instrumentation produced no database spans (it only supports the SQLAlchemy versions it was written for, and the server log said so). Instrumenting the layer underneath, the Postgres driver, works: every query becomes a span with the SQL text. When a trace is missing something, read the log of the instrumentation. The worker is a separate program, so it calls `tracing.start("allcs-worker")` when each worker process starts.

### 3. One enroll, one trace

Empty the Redis cache first so the first request is a cache miss, then enroll Lukas in course 1 and Priya in course 1:

```bash
docker compose exec -T redis redis-cli flushall
curl -s $U/courses > /dev/null
curl -s -i -X POST -H "Authorization: Bearer $L" $U/courses/1/enrollments
```

```
HTTP/1.1 201 Created
x-request-id: eef3bd4200c47cf6aee535c30f513b25
...
{"student_id":1,"course_id":1,"enrolled_on":"2026-10-29"}
```

(The ids and the date differ for you.) There is a new header, `X-Request-ID`: it is the trace ID. Print the trace from Jaeger (wait a few seconds for the batch exporter), or open `http://localhost:20162` and paste the ID:

```bash
python ../spans.py eef3bd4200c47cf6aee535c30f513b25
```

```
allcs-api         0.0     25.1  POST /courses/{course_id}/enrollments
allcs-api         1.2      0.3  SELECT  SELECT students.id, students.name, ...
allcs-api         1.8      1.1  course.title
allcs-api         1.8      0.2  GET  GET ?
allcs-api         2.4      0.1  SELECT  SELECT courses.id, courses.title, ...
allcs-api         2.7      0.2  SET  SET ? ? ? ?
allcs-api         3.5      0.4  INSERT  INSERT INTO enrollments (student_id, course_id) VALUES (...
allcs-api         6.0      0.2  SELECT  SELECT students.id, students.name, ...
allcs-api        20.4      3.0  apply_async/app.worker.send_welcome_email
allcs-api        20.8      1.0  PING  PING
allcs-api        22.1      0.8  LLEN ...
allcs-api        23.0      0.1  SADD  SADD ? ?
allcs-api        23.2      0.1  LPUSH  LPUSH ? ?
allcs-api        24.4      0.3  SELECT  SELECT enrollments.student_id, ...
allcs-worker     28.7     40.8  run/app.worker.send_welcome_email
allcs-worker     29.6      7.8  SET  SET ? ? ? ? ?
allcs-worker     54.6     12.5  smtp.send
```

(Columns: service, start in ms, duration in ms, name. About 17 spans in two services; some lines are shortened here.) Read it from the top: the long first span is the whole request in the server (25 ms). Below it: a `SELECT` to find the student, our own span `course.title` (with a `GET` to Redis inside it, and, because the cache was empty, a `SELECT` of the course and a `SET`), the `INSERT` of the enrollment, then empty space (from 6 ms to 20 ms, more than half of the request, with no span that explains it: a trace does not hide this), then the Redis spans (`PING`, `LLEN`, `SADD`, `LPUSH` push the welcome-email job into the queue), and then the trace crosses a border: `allcs-worker` spans `run/app.worker.send_welcome_email`, a `SET` (the idempotency key) and `smtp.send`. Same trace, two services.

Now the second request, a cache hit:

```bash
curl -s -i -X POST -H "Authorization: Bearer $PR" $U/courses/1/enrollments
```

Its trace has no `SELECT courses` and no `SET`: the `course.title` span shows only a `GET`, and the request is shorter.

### 4. A manual span, with an attribute

`app/routers/enrollments.py`:

```python
tracer = trace.get_tracer("allcs.enroll")
...
with tracer.start_as_current_span("course.title") as span:
    key = f"course:{course_id}:title"
    title = r.get(key)
    span.set_attribute("cache.hit", title is not None)
    if title is None:
        ...
```

Everything inside the `with` block becomes children of that span, and the attribute `cache.hit` (`false` for the first request, `true` for the second) shows when you click the span in Jaeger. Warning: never put a password, a token or private data in an attribute; whoever can open Jaeger can read it.

### 5. How the worker joined the trace

Stop the worker and enroll Lukas in course 2. The job waits in a Redis list; read it:

```bash
docker compose stop worker
curl -s -i -X POST -H "Authorization: Bearer $L" $U/courses/2/enrollments | grep -i x-request-id
docker compose exec -T redis redis-cli lrange celery 0 -1
```

The message headers contain (shortened):

```
traceparent: 00-c758cb698e9994f6344cb94c10ca313a-03ed887b6d07d462-03
task: app.worker.send_welcome_email
```

`traceparent` holds the version (`00`), the trace ID, the ID of the parent span and some flags. The Celery instrumentation wrote it into the message when the server sent the job. Start the worker again (`docker compose start worker`), wait, and print the trace with that request's `X-Request-ID`:

```
allcs-api         37.0      1.9  apply_async/app.worker.send_welcome_email
allcs-worker    5730.8     26.5  run/app.worker.send_welcome_email
allcs-worker    5750.0      6.7  smtp.send
```

The worker's span starts as a child of the server's span, and the trace is seconds long: the job waited in the queue (here about 5.7 seconds), and a trace shows the waiting time too. It also works from outside: a caller can send its own `traceparent` with a trace ID it chose, and the server joins that trace and answers with the same ID:

```bash
curl -s -i -X POST -H "Authorization: Bearer $PR" -H "traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01" $U/courses/2/enrollments | grep -iE "^HTTP|x-request-id"
```

```
HTTP/1.1 201 Created
x-request-id: 0af7651916cd43dd8448eb211c80319c
```

### 6. The trace ID in every log line

`TraceIdFilter` in `app/tracing.py` is a logging filter (module 14): it asks OpenTelemetry for the current span, reads its trace ID and puts it on every log record, and the format is `%(levelname)s %(name)s [%(trace_id)s] %(message)s`. One search over the logs of the server and the worker:

```bash
docker compose logs --no-log-prefix api worker | grep eef3bd4200c47cf6aee535c30f513b25
```

```
INFO allcs.enroll [eef3bd4200c47cf6aee535c30f513b25] student 1 enrolled in course 1
INFO app.worker [eef3bd4200c47cf6aee535c30f513b25] welcome email sent to lukas@example.com
INFO celery.app.trace [eef3bd4200c47cf6aee535c30f513b25] Task app.worker.send_welcome_email[4bd8716b-...] succeeded in 0.0422s: None
```

The log says what happened, the trace says when and for how long; with the same ID on both you can jump from one to the other. This grows the error id of module 15: now the error id and the trace ID are the same number. A real crash (the lesson-only route `/boom` divides by zero):

```bash
curl -s -i $U/boom
docker compose logs --no-log-prefix api | grep "^ERROR"
```

```
HTTP/1.1 500 Internal Server Error
x-request-id: 12e8f2ff12fc6a8a8199c5b4cc6eee00
{"error":{"code":"server_error","message":"Something went wrong","error_id":"12e8f2ff12fc6a8a8199c5b4cc6eee00"}}
ERROR allcs.errors [12e8f2ff12fc6a8a8199c5b4cc6eee00] error 12e8f2ff12fc6a8a8199c5b4cc6eee00
```

(followed by the traceback, ending in `ZeroDivisionError: division by zero`.) Support asks the customer for the error ID, searches the logs, finds the traceback, and opens the same ID in Jaeger.

### 7. Sampling

Every span costs a little time and memory, and a busy server can make millions of traces a day, so you keep only some (sampling). Two environment variables, no code change: `OTEL_TRACES_SAMPLER=parentbased_traceidratio` and `OTEL_TRACES_SAMPLER_ARG=0.1` (parent based means: if the caller already decided, follow it). `compose.yaml` passes both through (default: keep everything). Send 100 requests with everything kept, then restart Jaeger (it keeps traces in memory), restart the API with a ratio of 0.1, and send 100 again:

```bash
docker compose restart jaeger; sleep 7
for i in $(seq 100); do curl -s -o /dev/null $U/courses; done; sleep 8
python ../count_traces.py
docker compose restart jaeger; sleep 7
OTEL_TRACES_SAMPLER=parentbased_traceidratio OTEL_TRACES_SAMPLER_ARG=0.1 docker compose up -d api; sleep 10
for i in $(seq 100); do curl -s -o /dev/null $U/courses; done; sleep 8
python ../count_traces.py
```

```
100
9
```

All 100 traces are kept at first; with the ratio at 0.1 you get about 10, not exactly 10, because the choice is made by the trace ID (the video got 16 in its run).

## Common mistakes

- Putting private data in a span attribute.
- Expecting database spans from an instrumentation that does not support your library version: read the instrumentation's log, and instrument the layer underneath (the driver).
- Forgetting that the worker is a separate program: it needs its own `start("allcs-worker")`.
- A new trace in every service because the context (`traceparent`) was not passed along.
- Keeping every trace in production without a sampler.
- Logging without the trace ID, so you cannot jump from a log line to its trace.

## Clean up

```bash
docker compose down -v --remove-orphans
docker rmi m20l02-api
```

## Next

[M20-L03 · Finding Slow Code](../m20-l03-finding-slow-code/README.md)
