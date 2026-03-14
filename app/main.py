from fastapi import FastAPI
from app.routers import notes, users
from app.database import engine, Base

app = FastAPI(title="Notes API", version="1.0.0")

app.include_router(users.router)
app.include_router(notes.router)


@app.get("/")
def root():
    return {"message": "Notes API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
