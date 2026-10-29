from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app import cache, search
from app.db import get_session
from app.ratelimit import search_limit
from app.schemas import Hit, SearchOut

router = APIRouter(tags=["search"])


@router.get("/search", dependencies=[Depends(search_limit)])
def find_lessons(
    response: Response,
    q: str = Query(min_length=2, max_length=100),
    session: Session = Depends(get_session),
) -> SearchOut:
    results = cache.get(q)
    state = "hit" if results is not None else "miss"
    if results is None:
        results = search.find(session, q)
        cache.put(q, results)
    response.headers["X-Cache"] = state.upper()
    hits = [Hit(**row) for row in results]
    return SearchOut(query=q, cache=state, results=hits)
