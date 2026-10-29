from fastapi import FastAPI

from app.routers import auth, learn, search

app = FastAPI(title="Course Copilot-lite")
app.include_router(auth.router)
app.include_router(search.router)
app.include_router(learn.router)
