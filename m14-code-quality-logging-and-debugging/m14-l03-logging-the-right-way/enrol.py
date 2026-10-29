import logging

logger = logging.getLogger(__name__)


def enrol(course, student):
    if student in course:
        logger.warning("%s is already enrolled", student)
        return False
    course.append(student)
    logger.info("enrolled %s", student)
    return True
