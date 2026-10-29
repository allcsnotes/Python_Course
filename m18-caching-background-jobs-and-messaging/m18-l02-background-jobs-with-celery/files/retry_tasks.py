import redis

from tasks import celery_app, logger

store = redis.Redis(port=18402, decode_responses=True)


@celery_app.task(
    autoretry_for=(ConnectionError,),
    retry_backoff=1,
    retry_jitter=False,
    max_retries=4,
)
def send_flaky(email):
    tries = store.incr(f"tries:{email}")
    logger.info("attempt %s for %s", tries, email)
    if tries < 3:
        raise ConnectionError("mail service is down")
    return f"sent to {email}"
