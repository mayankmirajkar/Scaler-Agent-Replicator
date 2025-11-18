# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)  # hex like #3be8b0
    archived = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="not_started")  # not_started, in_progress, complete
    due_date = Column(DateTime, nullable=True)
    assignee = Column(String(255), nullable=True)
    priority = Column(String(50), nullable=True)  # low, medium, high
    label = Column(String(255), nullable=True)

    project = relationship("Project", back_populates="tasks")
