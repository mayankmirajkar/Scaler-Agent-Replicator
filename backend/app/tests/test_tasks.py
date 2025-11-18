# backend/app/tests/test_tasks.py
import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app
from app.db import Base, engine, SessionLocal
from app import models

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    project = models.Project(name="Test Project")
    db.add(project)
    db.commit()
    db.refresh(project)
    task = models.Task(
        project_id=project.id,
        name="Task 1",
        label="bug"
    )
    db.add(task)
    db.commit()
    db.close()
    yield

@pytest.mark.asyncio
async def test_label_exact_match():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/tasks", params={"label": "bug"})
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert len(data) == 1

@pytest.mark.asyncio
async def test_label_empty_string_ignored():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/tasks", params={"label": ""})
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    # empty label should behave same as no label filter
    assert len(data) == 1

@pytest.mark.asyncio
async def test_label_very_long_trimmed():
    long_label = "x" * 300
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.patch(
            "/tasks/1",
            json={"label": long_label}
        )
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert len(data["label"]) == 255
