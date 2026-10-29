"""Task 7 - check many URLs concurrently, politely, with timeouts and retries."""
import asyncio
from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    url: str
    ok: bool
    status: int | None = None
    attempts: int = 0
    error: str | None = None


async def check_one(url, fetch, *, timeout, retries, semaphore) -> Result:
    attempts = 0
    error = None
    for _ in range(retries + 1):
        attempts += 1
        try:
            async with semaphore:                      # at most N requests in flight
                status = await asyncio.wait_for(fetch(url), timeout)
        except asyncio.TimeoutError:
            error = "timeout"
        except OSError as exc:                          # connection problems
            error = type(exc).__name__
        else:
            if status < 500:                            # 4xx is the site's answer: do not retry
                return Result(url, status < 400, status, attempts)
            error = f"server error {status}"
    return Result(url, False, None, attempts, error)


async def check_all(urls, fetch, *, concurrency=5, timeout=1.0, retries=1) -> list[Result]:
    """Results come back in the same order as `urls`."""
    if concurrency < 1:
        raise ValueError("concurrency must be at least 1")
    semaphore = asyncio.Semaphore(concurrency)
    return await asyncio.gather(*(
        check_one(url, fetch, timeout=timeout, retries=retries, semaphore=semaphore)
        for url in urls))
