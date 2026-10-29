from fastapi import FastAPI

from app.routers import auth

app = FastAPI(title="Course Copilot-lite")
app.include_router(auth.router)
