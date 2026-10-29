"""Task 10 - a URL shortener: FastAPI + Postgres + Redis (cache, counters, rate limit)."""
import os
import secrets
import string
from typing import Annotated

import redis
from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import AnyHttpUrl, BaseModel, Field
from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://practice:practice@localhost:23604/practice")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:23404/5")
PREFIX = "t10:"
CACHE_SECONDS = 60
RATE_LIMIT = 5              # link creations ...
RATE_WINDOW = 60            # ... per minute per caller
ALPHABET = string.ascii_letters + string.digits


class Base(DeclarativeBase):
    pass


class Link(Base):
    __tablename__ = "t10_link"
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    url: Mapped[str]
    idempotency_key: Mapped[str | None] = mapped_column(String(100), unique=True)


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)
app = FastAPI(title="Short links")


def get_session():
    with Session(engine) as session:
        yield session


Db = Annotated[Session, Depends(get_session)]


class LinkIn(BaseModel):
    url: AnyHttpUrl
    code: str | None = Field(default=None, pattern=r"^[A-Za-z0-9_-]{3,32}$")


class LinkOut(BaseModel):
    code: str
    url: str


def new_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(7))


def rate_limit(request: Request):
    who = request.headers.get("x-api-key") or (request.client.host if request.client else "?")
    key = f"{PREFIX}rate:{who}"
    count = cache.incr(key)
    if count == 1:
        cache.expire(key, RATE_WINDOW)          # the window starts at the first call
    if count > RATE_LIMIT:
        wait = max(cache.ttl(key), 1)
        raise HTTPException(429, "too many links created", headers={"Retry-After": str(wait)})


@app.post("/links", status_code=201, response_model=LinkOut,
          dependencies=[Depends(rate_limit)])
def create(body: LinkIn, db: Db, response: Response,
           idempotency_key: Annotated[str | None, Header(max_length=100)] = None):
    if idempotency_key:                          # the same request again gives the same answer
        earlier = db.scalar(select(Link).where(Link.idempotency_key == idempotency_key))
        if earlier:
            response.status_code = 200
            return LinkOut(code=earlier.code, url=earlier.url)
    url = str(body.url)
    for _ in range(5):                           # random codes can (rarely) collide
        code = body.code or new_code()
        db.add(Link(code=code, url=url, idempotency_key=idempotency_key))
        try:
            db.commit()
            return LinkOut(code=code, url=url)
        except IntegrityError:
            db.rollback()
            if body.code:
                raise HTTPException(409, "that code is taken")
            if idempotency_key:                  # lost a race with the same key: return the winner
                earlier = db.scalar(select(Link).where(Link.idempotency_key == idempotency_key))
                if earlier:
                    response.status_code = 200
                    return LinkOut(code=earlier.code, url=earlier.url)
    raise HTTPException(503, "could not find a free code")


@app.get("/links/{code}/stats")
def stats(code: str):
    return {"code": code, "clicks": int(cache.get(f"{PREFIX}clicks:{code}") or 0)}


@app.delete("/links/{code}", status_code=204)
def delete(code: str, db: Db):
    link = db.get(Link, code)
    if link is None:
        raise HTTPException(404, "no such link")
    db.delete(link)
    db.commit()
    cache.delete(f"{PREFIX}url:{code}")          # invalidate, or the old URL would live on


@app.get("/{code}")
def follow(code: str, db: Db):
    key = f"{PREFIX}url:{code}"
    url = cache.get(key)                         # 1. look in the cache
    if url is None:
        link = db.get(Link, code)                # 2. miss: ask the database
        if link is None:
            raise HTTPException(404, "no such link")
        url = link.url
        cache.set(key, url, ex=CACHE_SECONDS)    # 3. remember it
    cache.incr(f"{PREFIX}clicks:{code}")
    return RedirectResponse(url, status_code=307)
