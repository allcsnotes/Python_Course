import httpx


class CourseServiceError(Exception):
    pass


def fetch_courses(url):
    try:
        response = httpx.get(url, timeout=2)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as error:
        code = error.response.status_code
        raise CourseServiceError(f"server said {code}") from error
    except httpx.TimeoutException as error:
        raise CourseServiceError("server too slow") from error
    except httpx.ConnectError as error:
        raise CourseServiceError("cannot reach server") from error
