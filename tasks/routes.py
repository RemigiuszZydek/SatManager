from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.database import get_db
from .schemas import TaskCreate, TaskOut
from . import services
from ..auth.dependencies import get_current_user, require_roles

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

db_dependency = Depends(get_db)

@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task_endpoint(task_data: TaskCreate, db: Session = db_dependency, current_user = Depends(require_roles(["ADMIN","KOORDYNATOR"]))):
    """
    Tworzy nowe zlecenie. Kontrola roli odbywa się w dependency.
    """
    task = services.create_task(db,task_data,current_user)
    
    return task

@router.get("/my-tasks", response_model=List[TaskOut])
async def get_my_tasks(db: Session = db_dependency, current_user = Depends(get_current_user)):
    """
    Pobiera zlecenia zalogowanego użytkownika
    """
    tasks = services.get_task_by_user(db, current_user)
    return tasks

@router.get("/unassigned", response_model=List[TaskOut])
async def get_unassigned_tasks(db: Session = db_dependency, current_user = Depends(get_current_user)):
    """
    Pobiera wszystkie nieprzypisane taski.
    Każdy zalogowany użytkownik może je zobaczyć.
    """
    tasks = services.get_unassigned_tasks(db)
    return tasks

@router.get("/{task_id}", response_model= TaskOut)
async def get_task_by_id_endpoint(task_id: int, db: Session = db_dependency):
    """
    Pobiera zlecenie po jego id
    """
    task = services.get_task_by_id(db,task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task