# M18-L03 · Events and Messages

> Video: Module 18, Lesson 3. Watch it first, then follow along here.

## What you'll learn

- The difference between a command (do this, one receiver) and an event (this happened, anyone may listen)
- Publish and subscribe with Redis, and why pub sub forgets messages when nobody is listening
- A log with offsets and consumer groups, using Kafka (a producer, a consumer, bookmarks, replay)
- At-least-once delivery: duplicates happen, so consumers must be idempotent (use the event id)
- The outbox pattern: keep the database and the events in agreement

## Before you start

- Python 3.14 or newer (`python --version`) and Docker running.
- No earlier lesson folder is needed. Everything here is small scripts. (The database parts use SQLite, which comes with Python.)
- Two containers: Redis 8 on port 18403 and one single-node Kafka on port 18603. Nothing leaves your laptop.

```bash
docker run -d --name pyrepo-m18-l03-redis -p 18403:6379 redis:8
docker run -d --name pyrepo-m18-l03-kafka -p 18603:18603 \
  -e KAFKA_NODE_ID=1 -e KAFKA_PROCESS_ROLES=broker,controller \
  -e KAFKA_LISTENERS=PLAINTEXT://:18603,CONTROLLER://:9093 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:18603 \
  -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
  -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
  -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 \
  -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 \
  apache/kafka:4.3.1
```

(The video starts Kafka with a plain `docker run` of the Apache Kafka image. The settings above make one small server reachable on port 18603; the video used the image `apache/kafka:latest`, which was version 4.3.1 when it was recorded. A real company runs several servers; Module 19 explains Docker properly.) Wait about ten seconds for Kafka to start.

Set up Python and tell the scripts where the servers are:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install redis==8.1.0 confluent-kafka==2.16.1
export REDIS_URL=redis://localhost:18403/0
export KAFKA_SERVERS=localhost:18603
cd files
```

Create the topic `enrollments` (one partition). You will use this command again to reset between demos:

```bash
docker exec pyrepo-m18-l03-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:18603 --create --topic enrollments --partitions 1 --replication-factor 1
```

```
Created topic enrollments.
```

## Files in this folder

| File | What it is |
|------|------------|
| `files/hook.py` | The problem: three helper calls in `enroll`, and a broken dashboard breaks enrollment |
| `files/events.py` | `enrolled(student, course)` builds an event: an id, a type in the past tense, and the details |
| `files/bus.py` | The Redis connection, the Kafka address, and `topic_size()` |
| `files/publisher.py`, `files/subscriber.py` | Redis pub sub: publish events, and a named subscriber |
| `files/producer.py`, `files/consumer.py` | Kafka: produce events, and a consumer with a group id and a manual bookmark |
| `files/welcome.py` | A consumer that sends a "welcome email" and can crash on purpose (`CRASH_ON`) |
| `files/welcome_fixed.py` | The same consumer made idempotent with a Redis set of event ids |
| `files/lost.py` | Save to the database, crash before publishing: the event is lost |
| `files/outbox.py` | The outbox pattern with a relay |

## Follow along

All commands run in `files/` with the virtual environment active.

### 1. One broken helper breaks the whole enrollment

```bash
python hook.py
```

```
saved Lukas in python-basics
email sent to Lukas
stats updated for python-basics
Traceback (most recent call last):
  ...
ConnectionError: dashboard is down
```

`enrolled!` never printed. Fix: `enroll` should only announce one fact (an event), and each part listens on its own.

### 2. Redis pub sub

Open two terminals and start the subscribers (each prints that it is listening):

```bash
python subscriber.py email      # terminal 1
python subscriber.py stats      # terminal 2
```

```
email is listening
stats is listening
```

In terminal 3 publish two events:

```bash
python publisher.py python-basics Lukas Priya
```

```
published Lukas: received by 2
published Priya: received by 2
```

Both subscribers print `email got Lukas python-basics`, `email got Priya python-basics` (and the same lines with `stats`). One announcement, two readers, and the publisher knows nothing about them. Now stop the `stats` subscriber with Ctrl+C (it prints `stats stopped`) and publish another event:

```bash
python publisher.py fastapi Lukas
```

```
published Lukas: received by 1
```

Only `email` gets it. Start `stats` again: it prints only `stats is listening` and never sees the missed event. Pub sub is like live radio: if you are not tuned in, the message is gone and Redis keeps no copy. That is fine for "who is online right now", not for an enrollment that must never be lost. Stop both subscribers (Ctrl+C).

### 3. Kafka: a log with offsets and bookmarks

Start with an empty topic (create it as above, or delete and create it again). Send four events, and only then start a consumer:

```bash
python producer.py python-basics Lukas Priya
python producer.py fastapi Lukas Priya
python consumer.py email
python consumer.py email
```

```
events sent: 2
events sent: 2
email offset 0 Lukas python-basics
email offset 1 Priya python-basics
email offset 2 Lukas fastapi
email offset 3 Priya fastapi
email is up to date
email is up to date
```

The consumer reads all four (offsets 0 to 3) although it was not running when they were sent. The second run prints only `is up to date`, because the bookmark for the group `email` now stands at 4. Send two more events and read again, then run a brand new group:

```bash
python producer.py sql Priya Lukas
python consumer.py email
python consumer.py stats
```

```
events sent: 2
email offset 4 Priya sql
email offset 5 Lukas sql
email is up to date
stats offset 0 Lukas python-basics
stats offset 1 Priya python-basics
stats offset 2 Lukas fastapi
stats offset 3 Priya fastapi
stats offset 4 Priya sql
stats offset 5 Lukas sql
stats is up to date
```

`email` continues from its bookmark; the new group `stats` starts at zero and replays everything (`auto.offset.reset` is `earliest`, and auto commit is off, so the script moves the bookmark itself after the work). Different groups each get every message. Consumers in the same group share the work.

### 4. At-least-once delivery: duplicates

Reset the topic and the group state (delete and re-create the topic, and use a new Kafka container if the old groups still hold bookmarks):

```bash
docker exec pyrepo-m18-l03-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:18603 --delete --topic enrollments
docker exec pyrepo-m18-l03-kafka /opt/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:18603 --delete --group welcome
docker exec pyrepo-m18-l03-kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:18603 --create --topic enrollments --partitions 1 --replication-factor 1
docker exec pyrepo-m18-l03-redis redis-cli del processed
```

(The second command may say the group does not exist the first time; that is fine.) Put three events in the topic, then run the consumer that crashes on purpose after Priya's first email, and run it again:

```bash
python producer.py python-basics Lukas Priya
python producer.py fastapi Priya
CRASH_ON=Priya-python-basics python welcome.py
python welcome.py
```

```
events sent: 2
events sent: 1
welcome email to Lukas python-basics
welcome email to Priya python-basics
power cut before the commit!
welcome email to Priya python-basics
welcome email to Priya fastapi
```

Priya got the python-basics email twice: the first run sent it and crashed before moving the bookmark, so the same message arrived again. Kafka did nothing wrong.

The cure is on the consumer side: be idempotent, using the event id. `welcome_fixed.py` first does `r.sadd("processed", e["id"])` (a Redis set holds each value once; it returns 1 for a new id and 0 for a seen one) and skips duplicates. Reset again (the four commands above) and repeat with the fixed consumer:

```bash
python producer.py python-basics Lukas Priya
python producer.py fastapi Priya
CRASH_ON=Priya-python-basics python welcome_fixed.py
python welcome_fixed.py
```

```
events sent: 2
events sent: 1
welcome email to Lukas python-basics
welcome email to Priya python-basics
power cut before the commit!
skip duplicate Priya-python-basics
welcome email to Priya fastapi
```

Honest notes: a unique constraint in the database does the same job, and "mark" then "work" are still two steps, so a crash between them could lose work instead of doubling it.

### 5. The publisher side: lost events and the outbox

Reset the topic (delete, then create) and the SQLite files (`rm -f allcs.db allcs2.db`). `lost.py` saves an enrollment, then "loses power" before publishing:

```bash
python lost.py
```

```
power cut before publish!
enrollments saved: 1
events in the topic: 0
```

Lukas is enrolled, but nobody will ever hear about it. The outbox pattern writes the event into an `outbox` table in the same database transaction as the enrollment, and a small relay publishes it later. Reset the topic and delete `allcs2.db`, then:

```bash
python outbox.py
```

```
waiting in the outbox: 1
events in the topic: 0
waiting in the outbox: 0
events in the topic: 1
```

This is a sketch: the relay must run all the time, if it dies between `produce` and marking the row the event goes out twice (so consumers must be idempotent), and old rows need cleaning.

### 6. Which tool, when?

- A command for one worker that must do a job (send an email): a background job, as in lesson 2.
- A live announcement where missing it is fine: Redis pub sub.
- Events that must be kept, replayed or read by several teams: a log such as Kafka.

Traps: a poison message (an event that always fails blocks everything behind it; after a few tries put it in a dead letter topic), secrets in events (send ids, never passwords or card numbers), and using a broker when a plain function call is enough.

## Common mistakes

- Expecting Redis pub sub to remember messages for a subscriber that was away.
- Moving the Kafka bookmark before the work is done (you can lose messages), or after (you can get duplicates). Assume duplicates and make consumers idempotent.
- Writing to the database and publishing as two separate steps with nothing joining them. Use an outbox.
- Putting secrets in event data.
- Running `lost.py` or `outbox.py` twice without deleting the SQLite files (the tables already exist).
- Running `lost.py` or `outbox.py` before the topic exists (you get `Unknown partition`). Create the topic first.

## Clean up

```bash
rm -f allcs.db allcs2.db
docker rm -f -v pyrepo-m18-l03-redis pyrepo-m18-l03-kafka
cd .. && rm -rf .venv
```

## Next

[M18-L04 · Rate Limiting and Resilience](../m18-l04-rate-limiting-and-resilience/README.md)
