from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import search
from app.db import get_session
from app.schemas import Hit, SearchOut

router = APIRouter(tags=["search"])


@router.get("/search")
def find_lessons(
    q: str = Query(min_length=2, max_length=100),
    session: Session = Depends(get_session),
) -> SearchOut:
    results = search.find(session, q)
    hits = [Hit(**row) for row in results]
    return SearchOut(query=q, cache="miss", results=hits)
