from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app import cache
from app.codes import new_code
from app.errors import fail
from app.models import Link

TAKEN = "links_code_key"


def expiry(days):
    if days is None:
        return None
    now = datetime.now(timezone.utc)
    return now + timedelta(days=days)


def create_link(session, url, days):
    expires_at = expiry(days)
    for _ in range(5):
        code = new_code()
        link = Link(code=code, url=url, expires_at=expires_at)
        session.add(link)
        try:
            session.commit()
        except IntegrityError as err:
            session.rollback()
            if err.orig.diag.constraint_name != TAKEN:
                raise
        else:
            return link
    fail(503, "Could not find a free code, try again")


def find_link(session, code):
    found = cache.get_cached(code)
    if found is not None:
        return found
    query = select(Link).where(Link.code == code)
    link = session.scalar(query)
    if link is None:
        return None
    cache.put_cached(code, link.url, link.expires_at)
    return cache.pack(link.url, link.expires_at)


def is_expired(found):
    if found["expires_at"] is None:
        return False
    when = datetime.fromisoformat(found["expires_at"])
    return when <= datetime.now(timezone.utc)
