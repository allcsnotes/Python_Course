import logging
import time

import httpx

log = logging.getLogger("weekly_report")


class ApiDown(Exception):
    pass


def login(client, settings):
    reply = client.post(
        "/auth/login",
        data={
            "username": settings.api_user,
            "password": settings.api_password.get_secret_value(),
        },
    )
    reply.raise_for_status()
    return reply.json()["access_token"]


def fetch_report(client, settings, start, end):
    token = login(client, settings)
    reply = client.get(
        "/admin/report",
        params={
            "start": start.isoformat(),
            "end": end.isoformat(),
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    reply.raise_for_status()
    return reply.json()


def worth_trying_again(err):
    if isinstance(err, httpx.HTTPStatusError):
        code = err.response.status_code
        return code >= 500 or code == 429
    return True


def fetch_with_tries(client, settings, start, end):
    n = settings.tries
    for attempt in range(1, n + 1):
        try:
            return fetch_report(client, settings, start, end)
        except httpx.HTTPError as err:
            log.warning("try %d/%d failed: %s", attempt, n, err)
            if attempt == n or not worth_trying_again(err):
                raise ApiDown(str(err)) from err
            time.sleep(settings.wait * attempt)
