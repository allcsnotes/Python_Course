from tasks import celery_app, logger

celery_app.conf.beat_schedule = {
    "count-every-four-seconds": {
        "task": "beat_tasks.count_enrollments",
        "schedule": 4.0,
    },
}


@celery_app.task
def count_enrollments():
    logger.info("counting enrollments")
    return "counted"
