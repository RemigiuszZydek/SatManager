from pydantic import BaseModel
from typing import Optional

class MaterialRead(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True

class MaterialCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class TaskMaterialCreate(BaseModel):
    material_id: int
    quantity: float


class TaskMaterialRead(BaseModel):
    id: int
    quantity: float
    material: MaterialRead

    class Config:
        orm_mode = True
