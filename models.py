from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum


class TaskStatus(str, enum.Enum):
    added = "добавлена"
    in_progress = "в работе"
    completed = "выполнена"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    status = Column(Enum(TaskStatus), default=TaskStatus.added)
