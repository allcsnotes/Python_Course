import asyncio
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile

app = FastAPI()
UPLOADS = Path("uploads")
UPLOADS.mkdir(exist_ok=True)


@app.post("/courses/{course_id}/thumbnail")
async def upload_thumbnail(course_id: int, file: UploadFile):
    if file.content_type != "image/png":
        raise HTTPException(
            status_code=415, detail="Only PNG images"
        )
    data = await file.read()
    target = UPLOADS / f"course-{course_id}.png"
    await asyncio.to_thread(target.write_bytes, data)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(data),
    }
