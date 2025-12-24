from sqlalchemy.orm import Session
from datetime import datetime
from .models import Tasks
from .schemas import TaskCreate, TaskStatusEnum

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


