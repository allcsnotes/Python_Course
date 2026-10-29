import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Path
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from sqlalchemy import select

from app import cache, errors, links, settings
from app.db import get_session
from app.limits import rate_limit
from app.models import Link
from app.schemas import LinkIn, LinkOut, Stats

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger(__name__)


async def flusher():
    while True:
        await asyncio.sleep(settings.FLUSH_SECONDS)
        try:
            await asyncio.to_thread(cache.flush_clicks)
        except Exception:
            log.exception("could not flush the clicks")


@asynccontextmanager
async def lifespan(app):
    task = asyncio.create_task(flusher())
    yield
    task.cancel()
    await asyncio.to_thread(cache.flush_clicks)


app = FastAPI(title="allcsvideos links", lifespan=lifespan)
app.add_exception_handler(
    RequestValidationError, errors.bad_input
)
app.add_exception_handler(HTTPException, errors.http_error)


def to_out(link):
    return LinkOut(
        code=link.code,
        short_url=f"{settings.BASE_URL}/{link.code}",
        url=link.url,
        expires_at=link.expires_at,
    )


@app.post(
    "/links",
    status_code=201,
    response_model=LinkOut,
    dependencies=[Depends(rate_limit)],
)
def create(body: LinkIn, session=Depends(get_session)):
    link = links.create_link(
        session, str(body.url), body.expires_in_days
    )
    return to_out(link)


@app.get("/links/{code}/stats", response_model=Stats)
def stats(code: str, session=Depends(get_session)):
    query = select(Link).where(Link.code == code)
    link = session.scalar(query)
    if link is None:
        errors.fail(404, "Unknown link")
    return Stats(
        code=code,
        url=link.url,
        clicks=link.clicks,
        pending=cache.pending_clicks(code),
    )


@app.get("/cache/stats")
def cache_stats():
    hits = int(cache.r.get("cache:hits") or 0)
    misses = int(cache.r.get("cache:misses") or 0)
    return {"hits": hits, "misses": misses}


@app.get("/{code}")
def go(
    code: str = Path(pattern="^[0-9a-zA-Z]{1,12}$"),
    session=Depends(get_session),
):
    found = links.find_link(session, code)
    if found is None:
        errors.fail(404, "Unknown link")
    if links.is_expired(found):
        errors.fail(410, "This link has expired")
    cache.count_click(code)
    return RedirectResponse(found["url"])
