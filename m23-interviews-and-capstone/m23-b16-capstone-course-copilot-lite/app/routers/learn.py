from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db import get_session
from app.deps import current_user
from app.models import Lesson, Note, Progress, User
from app.schemas import NoteIn, NoteOut, ProgressOut

router = APIRouter(tags=["learn"])


def lesson_or_404(session, lesson_id):
    lesson = session.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(404, "no such lesson")
    return lesson


@router.post("/notes", status_code=201)
def add_note(
    body: NoteIn,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
) -> NoteOut:
    lesson_or_404(session, body.lesson_id)
    note = Note(
        user_id=user.id,
        lesson_id=body.lesson_id,
        body=body.body,
    )
    session.add(note)
    session.commit()
    return NoteOut.model_validate(
        note, from_attributes=True
    )


@router.get("/notes")
def my_notes(
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
) -> list[NoteOut]:
    query = select(Note).where(Note.user_id == user.id)
    notes = session.scalars(query.order_by(Note.id)).all()
    return [
        NoteOut.model_validate(n, from_attributes=True)
        for n in notes
    ]


@router.post("/progress/{lesson_id}")
def mark_done(
    lesson_id: int,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
) -> ProgressOut:
    lesson_or_404(session, lesson_id)
    insert_done = (
        insert(Progress)
        .values(user_id=user.id, lesson_id=lesson_id)
        .on_conflict_do_nothing()
    )
    session.execute(insert_done)
    session.commit()
    return progress_of(session, user.id)


@router.get("/progress")
def my_progress(
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
) -> ProgressOut:
    return progress_of(session, user.id)


def progress_of(session, user_id):
    done = session.scalar(
        select(func.count()).where(
            Progress.user_id == user_id
        )
    )
    total = session.scalar(select(func.count(Lesson.id)))
    percent = round(100 * done / total) if total else 0
    return ProgressOut(
        done=done, total=total, percent=percent
    )
