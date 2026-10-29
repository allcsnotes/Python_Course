from toolkit import RetryableError, retry

charged = []


@retry(times=2)
def pay(amount):
    charged.append(amount)
    raise RetryableError("no reply")


try:
    pay(499)
except RetryableError:
    print("payment failed")
print("charged:", charged)
