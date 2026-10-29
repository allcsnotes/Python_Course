import random
import time

import httpx


def temporary(err):
    if isinstance(err, httpx.HTTPStatusError):
        return err.response.status_code >= 500
    return True


def retry(call, tries=5, base=0.5):
    for attempt in range(1, tries + 1):
        try:
            return call()
        except httpx.HTTPError as err:
            if attempt == tries or not temporary(err):
                raise
            delay = base * 2 ** (attempt - 1)
            wait = random.uniform(0, delay)
            print(f"attempt {attempt} failed, waiting {wait:.2f} s")
            time.sleep(wait)
