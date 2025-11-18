# backend/app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[schemas.Task])
def list_tasks(
    db: Session = Depends(get_db),
    project_id: Optional[int] = None,
    label: Optional[str] = Query(None, max_length=255),
    status: Optional[str] = None
):
    q = db.query(models.Task)
    if project_id is not None:
        q = q.filter(models.Task.project_id == project_id)
    # Example “business nuance” for label:
    # - empty string => ignore label filter
    # - null (missing) => ignore
    # - very long string => trimmed at 255
    if label is not None and label.strip() != "":
        label_value = label[:255]
        q = q.filter(models.Task.label == label_value)
    if status:
        q = q.filter(models.Task.status == status)
    return q.all()

@router.post("/", response_model=schemas.Task, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if not project:
        raise HTTPException(400, "Invalid project_id")
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.patch("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")

    data = update.dict(exclude_unset=True)
    if "label" in data and data["label"] is not None:
        data["label"] = data["label"][:255]

    for k, v in data.items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task
