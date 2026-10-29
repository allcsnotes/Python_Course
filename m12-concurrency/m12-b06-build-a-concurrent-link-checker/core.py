import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import httpx

BASE = "http://localhost:8626"
OPTIONS = {"timeout": 2, "follow_redirects": True}
BAD = ("broken", "timeout", "down")
LINKS = Path("links.txt").read_text().split()


@dataclass
class Result:
    url: str
    status: int | None
    kind: str
    ms: int


def elapsed(start):
    return round((time.perf_counter() - start) * 1000)


def from_response(url, response, start):
    status = response.status_code
    if status >= 400:
        kind = "broken"
    elif response.history:
        kind = "moved"
    else:
        kind = "ok"
    return Result(url, status, kind, elapsed(start))


def from_error(url, error, start):
    if isinstance(error, httpx.TimeoutException):
        kind = "timeout"
    else:
        kind = "down"
    return Result(url, None, kind, elapsed(start))


def report(results, seconds):
    for r in results:
        if r.kind == "ok":
            continue
        code = r.status or "-"
        path = r.url.removeprefix(BASE)
        print(f"{r.kind:<8}{code:>4}{r.ms:>6} ms  {path}")
    counts = Counter(r.kind for r in results)
    parts = ", ".join(f"{n} {k}" for k, n in counts.items())
    print(f"{len(results)} links checked in {seconds:.1f} s")
    print(parts)
