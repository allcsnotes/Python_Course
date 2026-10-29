import redis

from tasks import celery_app, logger

store = redis.Redis(port=18402, decode_responses=True)


@celery_app.task(
    bind=True,
    autoretry_for=(RuntimeError,),
    retry_backoff=1,
    retry_jitter=False,
    max_retries=3,
)
def welcome_naive(self, email):
    store.rpush("outbox", email)  # the email leaves here
    if self.request.retries == 0:
        raise RuntimeError("connection lost after sending")
    logger.info("sent %s", email)


@celery_app.task(
    bind=True,
    autoretry_for=(RuntimeError,),
    retry_backoff=1,
    retry_jitter=False,
    max_retries=3,
)
def welcome_safe(self, email):
    first_time = store.set(f"sent:{email}", 1, nx=True)
    if first_time:
        store.rpush("outbox", email)  # the email leaves here
    if self.request.retries == 0:
        raise RuntimeError("connection lost after sending")
    logger.info("sent %s", email)
