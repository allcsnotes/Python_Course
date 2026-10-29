import time

from celery import Celery
from celery.utils.log import get_task_logger
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import engine
from app.models import Enrollment

celery_app = Celery(
    "allcs",
    broker="redis://localhost:18402/0",
    backend="redis://localhost:18402/1",
)
celery_app.conf.task_track_started = True
logger = get_task_logger(__name__)


def talk_to_mail_service(email, course):
    time.sleep(2)  # pretend to talk to the mail service
    logger.info("mail sent to %s", email)


@celery_app.task(
    autoretry_for=(ConnectionError,),
    retry_backoff=2,
    max_retries=5,
)
def send_welcome_email(email, course):
    talk_to_mail_service(email, course)
    return f"sent: {course}"


@celery_app.task
def build_report():
    time.sleep(3)  # pretend this is a heavy report
    with Session(engine) as session:
        total = session.scalar(
            select(func.count()).select_from(Enrollment)
        )
    return {"enrollments": total}
