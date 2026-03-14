from fastapi import FastAPI

from app.database import Base, engine
from app.routers import notes, users

app = FastAPI(title="Notes API", version="1.0.0")

app.include_router(users.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {"message": "Notes API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
