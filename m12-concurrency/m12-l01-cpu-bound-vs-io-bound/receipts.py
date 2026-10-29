import time
from clocks import measure


def fetch_payments():
    time.sleep(1.5)


def draw_receipts():
    sum(range(400_000_000))


def make_receipts():
    fetch_payments()
    draw_receipts()


measure("make_receipts", make_receipts)
measure("fetch_payments", fetch_payments)
measure("draw_receipts", draw_receipts)
