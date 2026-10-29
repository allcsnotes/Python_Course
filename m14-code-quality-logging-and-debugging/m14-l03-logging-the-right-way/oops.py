import logging

logging.basicConfig(format="%(levelname)s %(message)s")
logger = logging.getLogger("enrol")


def seats_left(seats, taken):
    return seats // (seats - taken)


try:
    seats_left(2, 2)
except ZeroDivisionError as err:
    logger.error("could not count seats: %s", err)
    logger.exception("could not count seats")
