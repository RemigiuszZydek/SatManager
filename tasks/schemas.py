from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..users.schemas import UserOut
import enum

class TaskStatusEnum(enum.Enum):
    UNASSIGNED = "UNASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    REJECTED = "REJECTED"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]  = None
    address: str
    execution_date: Optional[datetime]

class TaskStatusUpdate(BaseModel):
    status: TaskStatusEnum

class TaskNoteUpdate(BaseModel):
    note: str

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatusEnum
    assigned_user_id: Optional[int]
    assigned_user : Optional[UserOut]
    address: str
    execution_date: Optional[datetime]
    
    class Config:
        from_attributes = True