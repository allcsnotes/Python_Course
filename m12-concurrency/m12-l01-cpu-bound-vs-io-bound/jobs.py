import time


def build_report():
    total = 0
    for n in range(140_000_000):
        total += n


def check_pages():
    for page in range(4):
        time.sleep(0.5)
