import httpx

from backoff import retry

URL = "http://localhost:8284/rate"


def get_rate():
    r = httpx.get(URL, timeout=1.0)
    r.raise_for_status()
    return r.json()["inr_per_eur"]


print("rate:", retry(get_rate))
