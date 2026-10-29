from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_session
from app.deps import require_admin
from app.logs import request_id
from app.routers.learn import lesson_or_404
from app.schemas import LessonEdit
from app.worker import reindex_lesson, weekly_progress_all

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)


@router.put("/lessons/{lesson_id}", status_code=202)
def edit_lesson(
    lesson_id: int,
    body: LessonEdit,
    session: Session = Depends(get_session),
):
    lesson = lesson_or_404(session, lesson_id)
    lesson.notes = body.notes
    session.commit()
    reindex_lesson.delay(lesson_id, request_id.get())
    return {"status": "saved, search index updating"}


@router.post("/weekly-emails", status_code=202)
def weekly_emails():
    weekly_progress_all.delay(request_id.get())
    return {"status": "queued"}
