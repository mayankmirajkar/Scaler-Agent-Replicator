# backend/app/routers/home.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/home", tags=["home"])

@router.get("/", response_model=schemas.HomeResponse)
def get_home(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)

    tasks_q = db.query(models.Task)
    total_tasks = tasks_q.count()
    completed_tasks = tasks_q.filter(models.Task.status == "complete").count()
    overdue_tasks = tasks_q.filter(
        models.Task.due_date < now,
        models.Task.status != "complete",
        models.Task.due_date != None
    ).count()
    this_week_completed = tasks_q.filter(
        models.Task.status == "complete",
        models.Task.due_date >= week_ago
    ).count()

    recent_projects = db.query(models.Project).order_by(models.Project.id.desc()).limit(5).all()
    my_tasks = tasks_q.order_by(models.Task.due_date.asc()).limit(10).all()

    widgets = schemas.HomeWidgetMetrics(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks,
        this_week_completed=this_week_completed,
    )

    return schemas.HomeResponse(
        widgets=widgets,
        recent_projects=recent_projects,
        my_tasks=my_tasks,
    )
