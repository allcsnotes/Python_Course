import json
import time

from celery import Celery, Task
from celery.signals import setup_logging, worker_process_init
from celery.utils.log import get_task_logger
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from redis import Redis

from app import mailer, tracing
from app.settings import get_settings

BROKER = str(get_settings().redis_url)
DEAD = "dead_letters:email"
WEEK = 7 * 24 * 3600
celery_app = Celery("allcs", broker=BROKER)
redis = Redis.from_url(BROKER, decode_responses=True)
logger = get_task_logger(__name__)


@setup_logging.connect
def configure_logging(**kwargs):
    tracing.setup_logging()


@worker_process_init.connect
def start_tracing(**kwargs):
    tracing.start("allcs-worker")
    RedisInstrumentor().instrument()
    CeleryInstrumentor().instrument()


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


@celery_app.task
def slow_job(seconds):
    logger.info("slow job started (%s s)", seconds)
    time.sleep(seconds)
    logger.info("slow job finished")
    return "done"
