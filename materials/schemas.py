from pydantic import BaseModel

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

class TaskMaterialCreate(BaseModel):
    material_id: int
    quantity: float


class TaskMaterialRead(BaseModel):
    id: int
    quantity: float
    material: MaterialRead

    class Config:
        orm_mode = True
