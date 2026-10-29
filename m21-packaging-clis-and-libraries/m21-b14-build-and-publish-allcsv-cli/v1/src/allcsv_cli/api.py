"""Ask the allcsvideos API for courses."""

import httpx

from allcsv_cli.data import Course


def fetch_courses(
    url: str, client: httpx.Client | None = None
) -> list[Course]:
    client = client or httpx.Client(timeout=5)
    response = client.get(f"{url}/courses")
    response.raise_for_status()
    return [Course(**item) for item in response.json()]
