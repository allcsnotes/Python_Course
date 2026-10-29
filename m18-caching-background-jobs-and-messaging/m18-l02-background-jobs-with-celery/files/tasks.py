import time

from celery import Celery
from celery.utils.log import get_task_logger

celery_app = Celery(
    "allcs",
    broker="redis://localhost:18402/0",
    backend="redis://localhost:18402/1",
)
celery_app.conf.task_track_started = True
logger = get_task_logger(__name__)


@celery_app.task
def send_welcome_email(email, course):
    logger.info("sending to %s", email)
    time.sleep(2)  # pretend to talk to the mail service
    return f"sent: {course}"
