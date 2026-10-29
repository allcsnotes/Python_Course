# M20-L01 · Health Checks, Metrics and Dashboards

> Video: Module 20, Lesson 1. Watch it first, then follow along here.

## What you'll learn

- The three kinds of signal (logs, metrics, traces) and why a health check (yes or no, right now) cannot answer "why does the site feel slow since lunch?"
- The three metric types in `prometheus_client`: a counter, a gauge and a histogram (and why histogram buckets are cumulative)
- How to measure every request in one place with middleware, with labels that have few known values (the route pattern, not the real address)
- How Prometheus scrapes `/metrics`, and the PromQL you need: `rate`, `histogram_quantile` (P95), and an error ratio
- Why a label with many values (a user id) explodes the number of time series
- A Grafana dashboard as files (the RED method: rate, errors, duration), a business metric, and an alert rule on what users feel

## Before you start

- Docker with `docker compose` running, and Python 3.14 on the host for `promq.py` (it only uses the standard library: `python --version`).
- This lesson continues the backend of M19-L04. The folder `allcs/` is that backend with `app/metrics.py`, the monitoring files and a load generator.
- Images (pinned): `postgres:17.11`, `redis:8`, `axllent/mailpit:v1.32.0`, `prom/prometheus:v3.5.0`, `grafana/grafana:12.1.1`, `locustio/locust:2.37.14`, and `ghcr.io/astral-sh/uv:0.13` for the API image.
- The compose project is `m20l01`. Host ports: API 8201, Postgres 20501, Redis 20401, Prometheus 20091, Grafana 20031. All passwords and keys are demo values.
- Numbers (requests per second, latencies, how many requests) change on every machine and every run, so yours will differ. The shape is what counts.

Everything below runs in `allcs/` unless it says otherwise:

```bash
cd allcs
docker compose up -d --wait
docker compose ps --format "table {{.Service}}\t{{.Status}}"
```

```
SERVICE      STATUS
api          Up 5 seconds (healthy)
db           Up 9 seconds (healthy)
grafana      Up 5 seconds
mail         Up 9 seconds (healthy)
prometheus   Up 5 seconds
redis        Up 9 seconds (healthy)
worker       Up 5 seconds
```

(The first start builds the API image. Add the demo data: 200 students, 40 courses, and a file of long-lived access tokens for the load generator. The tokens are fake and made on your machine; the file is in `.gitignore`.)

```bash
docker compose exec -T -e PYTHONPATH=/app api python /tools/seed_load.py 2>/dev/null > loadgen/tokens.json
wc -c < loadgen/tokens.json
```

## Files in this folder

| File | What it is |
|------|------------|
| `allcs/app/metrics.py` | The metrics (`http_requests_total`, `http_request_seconds`, `http_requests_in_flight`, `enrollments_total`), the middleware `measure`, and the `/metrics` endpoint (multi-process safe) |
| `allcs/app/main.py` | Adds the middleware and the `/metrics` route (two lines) |
| `allcs/app/routers/enrollments.py` | One line after the enrollment is saved: `ENROLLMENTS.inc()` |
| `allcs/app/worker.py` | The worker starts its own metrics page on port 9100 (`emails_sent_total`, `email_task_seconds`) |
| `allcs/monitoring/prometheus.yml` | Scrape every 5 seconds: jobs `api` (`api:8000`) and `worker` (`worker:9100`); loads `rules.yml` |
| `allcs/monitoring/rules.yml` | The alert `HighErrorRate`: more than 5 percent of requests fail for 30 seconds |
| `allcs/monitoring/grafana/` | Provisioning (the data source and the dashboard folder) and the dashboard `allcs.json` with five panels |
| `allcs/compose.yaml` | The stack: db, redis, mail, migrate, api, worker, prometheus, grafana |
| `allcs/tools/types_demo.py` | One counter, one gauge, one histogram, printed as Prometheus would publish them |
| `allcs/tools/cardinality.py` | The label experiment: 3 series against 6000 series |
| `allcs/tools/seed_load.py` | Demo data and tokens (runs inside the API container) |
| `allcs/loadgen/locustfile.py` | Locust plays 30 students: browse courses, enroll, sometimes open a slow report |
| `promq.py` | Asks the Prometheus API one PromQL question and prints the answer |

## Follow along

### 1. The health check says fine, and that is all it says

```bash
curl -s -i localhost:8201/health/ready
```

```
HTTP/1.1 200 OK
content-length: 47
content-type: application/json

{"status":"ready","postgres":"ok","redis":"ok"}
```

It is right, but it answers one question: alive, yes or no. If Meera says "the site feels slow since lunch", it cannot tell you how many requests arrive, how fast they are answered, or since when it got slow. A car has a warning light (health check) and a dashboard (metrics, changing all the time). Logs are one line per thing that happened; metrics are numbers over time (tiny, cheap, easy to graph, they tell you THAT something is wrong); traces are the story of one request (next lesson).

### 2. The three metric types

```bash
docker run --rm --entrypoint python -v $PWD/tools:/tools:ro m20l01-api /tools/types_demo.py
```

```
# HELP enrollments_total Students enrolled
# TYPE enrollments_total counter
enrollments_total 3.0
# HELP students_online Students online
# TYPE students_online gauge
students_online 39.0
# HELP page_seconds Page time
# TYPE page_seconds histogram
page_seconds_bucket{le="0.1"} 1.0
page_seconds_bucket{le="0.5"} 2.0
page_seconds_bucket{le="1.0"} 2.0
page_seconds_bucket{le="5.0"} 3.0
page_seconds_bucket{le="+Inf"} 3.0
page_seconds_count 3.0
page_seconds_sum 2.34
```

(The real output also has `_created` lines with a time stamp, left out here.) A counter only goes up (requests, enrollments; it restarts from zero when the program restarts). A gauge goes up and down (`inc`, `dec`, `set`: students online, 42 minus 3 is 39). A histogram keeps buckets of how many things were faster than a limit: the pages took 0.04, 0.3 and 2.0 seconds, so the bucket "0.5 seconds" has two. Buckets are cumulative.

### 3. Measure every request in one place

Read `app/metrics.py`. The counter has the labels `method`, `route` and `status`; the histogram has `route` and eight buckets from 10 ms to 5 s. The middleware `measure` skips `/metrics` and the health checks, adds one to `in flight`, starts a timer, calls the next step, and in a `finally` block takes one off again and records the count and the time. The trick: the label is the ROUTE PATTERN (`/courses/{course_id}`), not the real address (`/courses/17`), otherwise every course would be a new series. Unknown paths become `unmatched`. The server runs two gunicorn worker processes, each with its own memory, so the library's multi-process mode keeps the counters in small files in a folder (`PROMETHEUS_MULTIPROC_DIR`) and `/metrics` adds them up. Ask for a few pages and read the metrics page:

```bash
for i in 1 2 3; do curl -s -o /dev/null localhost:8201/courses; done
curl -s -o /dev/null localhost:8201/courses/1
curl -s -o /dev/null localhost:8201/nothing-here
sleep 6
curl -s localhost:8201/metrics | grep -E "^(http_requests_total|http_requests_in_flight)"
curl -s localhost:8201/metrics | grep -E "^http_request_seconds_count"
```

```
http_requests_total{method="GET",route="/courses",status="200"} 3.0
http_requests_total{method="GET",route="/courses/{course_id}",status="200"} 1.0
http_requests_total{method="GET",route="unmatched",status="404"} 1.0
http_requests_in_flight 0.0
http_request_seconds_count{route="/courses"} 3.0
http_request_seconds_count{route="/courses/{course_id}"} 1.0
http_request_seconds_count{route="unmatched"} 1.0
```

Every metric starts with two comment lines (`# HELP`, `# TYPE`); then one line per time series: the name, the labels in braces, and the value. A time series is a name plus one set of labels. A histogram writes eleven lines for each route: eight buckets, `+Inf`, the sum and the count. The worker has no web server, so when it is ready it starts a tiny one on port 9100:

```bash
docker compose exec -T worker python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:9100/metrics').read().decode())" | grep -E "^# TYPE"
```

```
# TYPE email_task_seconds histogram
# TYPE enrollments_total counter
# TYPE emails_sent_total counter
```

(There are more lines; the order may differ.)

### 4. Prometheus scrapes the pages

`monitoring/prometheus.yml` says: scrape every 5 seconds, evaluate rules every 5 seconds, two jobs (`api:8000`, `worker:9100`). Prometheus and Grafana are two more services in the same compose file. Check the targets:

```bash
curl -s localhost:20091/api/v1/targets | python3 -c "import json,sys; [print(t['labels']['job'], t['scrapeUrl'], t['health']) for t in json.load(sys.stdin)['data']['activeTargets']]"
```

```
api http://api:8000/metrics up
worker http://worker:9100/metrics up
```

(Or open `http://localhost:20091/targets`.) If a target stops answering, the metric `up` becomes 0: a health check across the whole system.

### 5. Play 30 students and ask questions in PromQL

Locust plays 30 students (lesson 3 explains it). Start it for 2 minutes in a second terminal:

```bash
docker run --rm --name pyrepo-m20-l01-locust --network m20l01_default -v "$PWD/loadgen":/mnt/locust locustio/locust:2.37.14 -f /mnt/locust/locustfile.py --headless -u 30 -r 5 -t 135s --host http://api:8000 --only-summary
```

After about a minute, Prometheus has history. `promq.py` asks the Prometheus API the same question the Prometheus web page asks (`http://localhost:20091/query`):

```bash
python ../promq.py 'up'
python ../promq.py 'sum by (route) (http_requests_total)'
python ../promq.py 'sum by (route) (rate(http_requests_total[1m]))'
python ../promq.py 'histogram_quantile(0.95, sum by (le) (rate(http_request_seconds_bucket[1m])))'
python ../promq.py 'histogram_quantile(0.95, sum by (le, route) (rate(http_request_seconds_bucket[1m])))'
python ../promq.py 'sum(increase(enrollments_total[1m]))'
python ../promq.py 'sum(increase(emails_sent_total[1m]))'
python ../promq.py 'sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))'
```

```
{__name__="up",instance="worker:9100",job="worker"} 1.0
{__name__="up",instance="api:8000",job="api"} 1.0
{route="/courses"} 1023.0
{route="/courses/{course_id}"} 558.0
{route="unmatched"} 1.0
{route="/courses/{course_id}/enrollments"} 322.0
{route="/slow"} 114.0
{route="/courses"} 17.51
{route="/courses/{course_id}"} 9.551
{route="unmatched"} 0.0
{route="/courses/{course_id}/enrollments"} 5.468
{route="/slow"} 1.961
{} 0.28
{route="/courses"} 0.01
{route="/courses/{course_id}"} 0.01
{route="unmatched"} nan
{route="/courses/{course_id}/enrollments"} 0.041
{route="/slow"} 0.487
{} 326.353
{} 325.556
(an empty answer: no 5xx so far)
```

(Your numbers differ: this is one real run on one laptop.) What they say: a counter alone is a running total since the start; `rate(...[1m])` turns it into requests per second. An average hides the slow ones; P95 is the time that 95 of every 100 requests beat. Per route it is clearer: 0.01 is the smallest bucket (10 ms or less), the slow report is about 0.49 seconds (it sleeps 0.4 seconds). The error ratio is EMPTY, not zero: Prometheus has never seen a 5xx, so that series does not exist yet. Enrollments per minute and emails sent per minute follow each other (about 326 each): if they ever drift apart, emails are stuck.

### 6. Labels: a warning

Every different set of label values is a new time series, and Prometheus keeps every series in memory:

```bash
docker run --rm --entrypoint python -v $PWD/tools:/tools:ro m20l01-api /tools/cardinality.py
```

```
label route:        3
label route + user: 6000
```

One innocent label for 2000 users makes 2000 times more series, and for a histogram multiply by eleven (66,000 series). A label must have few, known values: the method, the route pattern, the status. Never a user id, an email, a request id or a raw address.

### 7. Grafana: the dashboard as files

Open `http://localhost:20031` (login is off, anonymous viewer) and the dashboard "allcsvideos API" in the folder `allcsvideos`. Grafana reads two small files at start (`provisioning/datasources/prometheus.yml`: the Prometheus data source; `provisioning/dashboards/allcs.yml`: the folder to look in) and the dashboard JSON `allcs.json`, which sits in version control like code. Its five panels, each one a PromQL question from step 5:

| Panel | Query |
|-------|-------|
| Rate: requests per second | `sum by (route) (rate(http_requests_total[1m]))` |
| Errors: share of requests that fail | `sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))` |
| Duration: P95 latency | `histogram_quantile(0.95, sum by (le) (rate(http_request_seconds_bucket[1m])))` |
| Enrollments per minute | `sum(rate(enrollments_total[1m])) * 60` |
| Emails sent per minute | `sum(rate(emails_sent_total[1m])) * 60` |

Rate, errors and duration are the RED method: they answer most questions about any service. The last two are a business metric (`enrollments_total`, one line in the enroll route) and the worker's emails.

### 8. An incident, and an alert

While Locust is running, stop Redis, look at the health check, and start Redis again about 40 seconds later:

```bash
docker stop m20l01-redis-1
curl -s -i localhost:8201/health/ready | sed -n '1p;$p'
```

```
HTTP/1.1 503 Service Unavailable
{"status":"not ready","postgres":"ok","redis":"down"}
```

The health check noticed at once (a load balancer would stop sending traffic). The dashboard tells the whole story: after a minute of Redis being down

```bash
python ../promq.py 'sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))'
python ../promq.py 'sum by (route) (rate(http_requests_total{status=~"5.."}[1m]))'
```

```
{} 0.071
{route="/courses/{course_id}/enrollments"} 2.974
```

(In the video, with Redis down for about 85 seconds, the error share was about 0.109 and 4.3 requests a second.) Only the enrollments route fails (it needs Redis), the P95 jumps up because failing enrollments are slow, and the emails sent by the worker fall to zero and come back after the restart. The alert rule in `monitoring/rules.yml` asks itself every 5 seconds: is the share of failed requests above 5 percent, for at least 30 seconds? While Redis was down it turned pending and then firing:

```bash
curl -s localhost:20091/api/v1/alerts | python3 -c "import json,sys; [print(a['labels']['alertname'], a['state'], a['annotations']['summary']) for a in json.load(sys.stdin)['data']['alerts']]"
```

```
HighErrorRate pending More than 5% of requests are failing
HighErrorRate firing More than 5% of requests are failing
```

(The first line right after the failures start, the second about 30 seconds later; `http://localhost:20091/alerts` shows the same.) Prometheus hands a firing alert to a program called Alertmanager, which sends the e-mail or the chat message (this lesson does not run one). One habit: alert on what users feel (errors, slowness), not on causes like "CPU at 80 percent".

A business metric earns its place here: if the enroll button breaks on the web page, every request that arrives is fine, the error rate is zero and the health check says ready, but enrollments per minute drops to nothing.

## Common mistakes

- Using the real address as a label (`/courses/17`) or putting a user id or e-mail in a label: thousands of series, and the server that stores your metrics runs out of memory.
- Looking only at the average latency. Use P95 or P99.
- Using a counter's raw value instead of `rate(...)`.
- Reading an empty answer as zero: "no series yet" is not the same as "0".
- Forgetting that each gunicorn worker has its own memory: use the multi-process mode.
- Counting the health checks and `/metrics` itself as users.
- Alerting on causes (CPU) instead of symptoms (errors, slowness).

## Clean up

```bash
docker rm -f pyrepo-m20-l01-locust 2>/dev/null
docker compose down -v --remove-orphans
docker rmi m20l01-api
rm -f loadgen/tokens.json
```

## Next

[M20-L02 · Tracing with OpenTelemetry](../m20-l02-tracing-with-opentelemetry/README.md)
