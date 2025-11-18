# backend/app/main.py
from fastapi import FastAPI
from .db import Base, engine
from .routers import home, projects, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Asana Replica API",
    version="0.1.0"
)

app.include_router(home.router)
app.include_router(projects.router)
app.include_router(tasks.router)
