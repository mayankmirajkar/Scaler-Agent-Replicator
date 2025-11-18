# backend/app/schemas.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
# from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    status: Optional[str] = Field("not_started")
    due_date: Optional[datetime] = None
    assignee: Optional[str] = None
    priority: Optional[str] = None
    label: Optional[str] = None

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee: Optional[str] = None
    priority: Optional[str] = None
    label: Optional[str] = None

class Task(TaskBase):
    id: int
    project_id: int
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    archived: bool = False

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    archived: Optional[bool] = None

class Project(ProjectBase):
    id: int
    tasks: List[Task] = []

    class Config:
        orm_mode = True

class HomeWidgetMetrics(BaseModel):
    total_tasks: int
    completed_tasks: int
    overdue_tasks: int
    this_week_completed: int

class HomeResponse(BaseModel):
    widgets: HomeWidgetMetrics
    recent_projects: List[Project]
    my_tasks: List[Task]
