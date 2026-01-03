from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from .models import Tasks
from .schemas import TaskCreate, TaskStatusEnum
from fastapi import HTTPException, status
from ..users.models import Users

def create_task(db: Session, task_data: TaskCreate, current_user):
    """
    Tworzy nowe zlecenie (task). Kontrola roli odbywa się w routerze.
    """

    task = Tasks(
        title=task_data.title,
        description=task_data.description,
        address=task_data.address,
        execution_date=task_data.execution_date,
        status=TaskStatusEnum.UNASSIGNED,
        created_at=datetime.utcnow(),
        created_by_id=current_user["id"],
        assigned_user_id=None
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_task_by_id(db:Session, task_id):
    """
    Pobiera pojedynczy task po ID.
    Zwraca None, jeśli nie istnieje.
    """

    return db.query(Tasks).filter(Tasks.id == task_id).first()

def get_task_by_user(db:Session, user):
    """
    Pobiera wszystkie taski przypisane do danego użytkownika.
    """
    
    return db.query(Tasks).filter(Tasks.assigned_user_id == user["id"]).all()

def get_unassigned_tasks(db:Session):
    """
    Pobiera wszystkie nieprzypisane taski
    """

    return db.query(Tasks).filter(Tasks.assigned_user_id == None).all()

def update_task(db: Session, task_id: int, task_update, current_user):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_update.title
    task.description = task_update.description
    task.address = task_update.address
    task.execution_date = task_update.execution_date

    db.commit()
    db.refresh(task)
    return task

def assign_task(db: Session, task_id: int, user_to_assign_id: int, current_user):
    task = (
        db.query(Tasks)
        .options(joinedload(Tasks.assigned_user).joinedload(Users.role))
        .filter(Tasks.id == task_id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.assigned_user_id is not None:
        raise HTTPException(status_code=400, detail="Task already assigned")
    
    task.assigned_user_id = user_to_assign_id
    
    db.commit()
    db.refresh(task)
    return task

def change_task_status(db: Session, task_id: int, new_status: TaskStatusEnum, current_user):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = new_status

    db.commit()
    db.refresh(task)
    return task

def add_task_note(db: Session, task_id: int, note: str, current_user):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.description:
        task.description += f"\nNote by {current_user['username']}: {note}"
    else:
        task.description = f"Note by {current_user['username']}: {note}"

    db.commit()
    db.refresh(task)
    return task

def delete_task(db:Session, task_id: int, current_user):
    task = db.query(Tasks).filter(Tasks.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}