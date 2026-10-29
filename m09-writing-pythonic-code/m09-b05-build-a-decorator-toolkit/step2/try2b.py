from toolkit import RetryableError, retry


@retry(times=2)
def always_down():
    raise RetryableError("server busy")


@retry(times=3)
def buggy(total):
    return total / 0


try:
    always_down()
except RetryableError as error:
    print("gave up:", error)

buggy(10)
