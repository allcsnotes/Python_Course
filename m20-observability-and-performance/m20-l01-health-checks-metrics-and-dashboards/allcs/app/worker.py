import json
import time

from celery import Celery, Task
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from prometheus_client import Counter, Histogram, start_http_server
from redis import Redis

from app import mailer, metrics
from app.settings import get_settings

BROKER = str(get_settings().redis_url)
DEAD = "dead_letters:email"
WEEK = 7 * 24 * 3600
celery_app = Celery("allcs", broker=BROKER)
redis = Redis.from_url(BROKER, decode_responses=True)
logger = get_task_logger(__name__)
EMAILS = Counter("emails_sent_total", "Welcome emails sent")
EMAIL_SECONDS = Histogram(
    "email_task_seconds", "Time to send one welcome email"
)


@worker_ready.connect
def serve_metrics(**kwargs):
    start_http_server(9100, registry=metrics.registry())


class EmailTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        item = {
            "task_id": task_id,
            "kwargs": kwargs,
            "error": repr(exc),
        }
        redis.lpush(DEAD, json.dumps(item))
        logger.error("gave up on %s", kwargs["email"])


@celery_app.task(
    base=EmailTask,
    autoretry_for=(OSError,),
    retry_backoff=1,
    retry_jitter=False,
    max_retries=3,
)
def send_welcome_email(
    *, student_id, course_id, name, email, title
):
    key = f"welcome:{student_id}:{course_id}"
    if not redis.set(key, 1, nx=True, ex=WEEK):
        logger.info("skipped %s, already sent", key)
        return
    message = mailer.welcome_message(name, email, title)
    try:
        with EMAIL_SECONDS.time():
            mailer.send(message)
        EMAILS.inc()
    except Exception:
        redis.delete(key)
        raise
    logger.info("welcome email sent to %s", email)


@celery_app.task
def slow_job(seconds):
    logger.info("slow job started (%s s)", seconds)
    time.sleep(seconds)
    logger.info("slow job finished")
    return "done"
