import json
import os

from celery import Celery, Task
from celery.utils.log import get_task_logger
from redis import Redis

from app import mailer

BROKER = os.environ.get(
    "REDIS_URL", "redis://localhost:18412/0"
)
DEAD = "dead_letters:email"
WEEK = 7 * 24 * 3600
celery_app = Celery("allcs", broker=BROKER)
redis = Redis.from_url(BROKER, decode_responses=True)
logger = get_task_logger(__name__)


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
        mailer.send(message)
    except Exception:
        redis.delete(key)
        raise
    logger.info("welcome email sent to %s", email)
