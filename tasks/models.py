from ..database.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Enum, Text
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from .schemas import TaskStatusEnum



class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text,nullable=True)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.UNASSIGNED, nullable=False)

    assigned_user_id = Column(Integer, ForeignKey("users.id"),nullable=True)
    assigned_user = relationship("Users", foreign_keys=[assigned_user_id])

    address = Column(String, nullable=False)
    execution_date = Column(DateTime,nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    
    created_by_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    created_by = relationship("Users", foreign_keys=[created_by_id])