from fastapi import FastAPI, status, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session 
from .users import models
from .database.database import engine, SessionLocal, get_db
from .auth.routes import router as auth_route
from .auth.test_roles import router as test_role_route
from .auth.dependencies import get_current_user
from .users.seed_roles import seed_roles
from .tasks.routes import router as tasks_route


app = FastAPI()
app.include_router(auth_route)
app.include_router(test_role_route)
app.include_router(tasks_route)

def init_db():
    models.Base.metadata.create_all(bind=engine)
    seed_roles()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"User":user}

if __name__ == "__main__":
    init_db()