from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False


class TaskIn(TaskBase):
    pass


class TaskCreate(TaskBase):
    owner: UUID


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None


class Task(TaskBase):
    id: UUID
    owner: UUID

    model_config = ConfigDict(from_attributes=True)


class TaskOut(TaskBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)

