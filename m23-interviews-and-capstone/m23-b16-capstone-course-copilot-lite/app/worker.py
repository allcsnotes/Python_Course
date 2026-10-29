import logging
from datetime import date

from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging
from sqlalchemy import func, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app import cache, mailer, search
from app.db import engine
from app.logs import configure_logging, request_id
from app.models import Lesson, Progress, User
from app.settings import get_settings

settings = get_settings()
log = logging.getLogger("copilot.worker")
celery_app = Celery(
    "copilot", broker=str(settings.redis_url)
)
celery_app.conf.update(
    timezone="Asia/Kolkata",
    beat_schedule={
        "weekly-progress": {
            "task": "app.worker.weekly_progress_all",
            "schedule": crontab(day_of_week=1, hour=8),
        }
    },
)


@setup_logging.connect
def use_json_logs(**kwargs):
    configure_logging(settings.log_level)


@celery_app.task(
    autoretry_for=(OperationalError,),
    retry_backoff=1,
    max_retries=3,
)
def reindex_lesson(lesson_id, rid="-"):
    request_id.set(rid)
    with Session(engine) as session:
        search.index_lesson(session, lesson_id)
        session.commit()
    generation = cache.invalidate()
    log.info(
        "lesson reindexed",
        extra={
            "lesson_id": lesson_id,
            "generation": generation,
        },
    )


@celery_app.task
def weekly_progress_all(rid="-"):
    request_id.set(rid)
    with Session(engine) as session:
        ids = session.scalars(
            select(User.id).where(User.role == "student")
        ).all()
    for user_id in ids:
        send_progress_email.delay(user_id, rid)
    log.info(
        "weekly emails queued", extra={"students": len(ids)}
    )


@celery_app.task(
    autoretry_for=(OSError,), retry_backoff=1, max_retries=3
)
def send_progress_email(user_id, rid="-"):
    request_id.set(rid)
    year, week, _ = date.today().isocalendar()
    key = f"weekly:{user_id}:{year}-W{week}"
    if not cache.redis.set(
        key, 1, nx=True, ex=8 * 24 * 3600
    ):
        log.info("already sent", extra={"user_id": user_id})
        return
    with Session(engine) as session:
        user = session.get(User, user_id)
        done = session.scalar(
            select(func.count()).where(
                Progress.user_id == user_id
            )
        )
        total = session.scalar(
            select(func.count(Lesson.id))
        )
    if user is None:
        return
    message = mailer.progress_message(
        user.name, user.email, done, total
    )
    try:
        mailer.send(message)
    except Exception:
        cache.redis.delete(key)
        raise
    log.info(
        "progress email sent", extra={"to": user.email}
    )
