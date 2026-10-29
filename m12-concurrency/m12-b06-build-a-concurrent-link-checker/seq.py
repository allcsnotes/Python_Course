import time

import httpx

from core import LINKS, OPTIONS, from_error, from_response, report


def check(client, url):
    start = time.perf_counter()
    try:
        response = client.get(url)
    except httpx.HTTPError as error:
        return from_error(url, error, start)
    return from_response(url, response, start)


def run(links):
    with httpx.Client(**OPTIONS) as client:
        return [check(client, url) for url in links]


if __name__ == "__main__":
    began = time.perf_counter()
    results = run(LINKS)
    report(results, time.perf_counter() - began)
