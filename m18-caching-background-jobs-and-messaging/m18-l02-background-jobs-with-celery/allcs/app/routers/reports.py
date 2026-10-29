from celery.result import AsyncResult
from fastapi import APIRouter, Depends

from app.permissions import require_role
from app.worker import build_report, celery_app

router = APIRouter(
    prefix="/reports",
    tags=["reports"],
    dependencies=[Depends(require_role("admin"))],
)


@router.post("/enrollments", status_code=202)
def start_report():
    job = build_report.delay()
    return {"job_id": job.id, "status_url": f"/reports/{job.id}"}


@router.get("/{job_id}")
def report_status(job_id: str):
    job = AsyncResult(job_id, app=celery_app)
    body = {"job_id": job_id, "status": job.state}
    if job.successful():
        body["result"] = job.result
    return body
