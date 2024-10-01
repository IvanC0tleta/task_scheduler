from pydantic import BaseModel
from typing import Optional
from models import TaskStatus


class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


class Task(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: TaskStatus

    class Config:
        from_attributes = True
