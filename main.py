from fastapi import FastAPI, status, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session 
from .users import models
from .database.database import engine, SessionLocal, get_db
from .auth.auth import router as auth_route, get_current_user

app = FastAPI()
app.include_router(auth_route)

models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"User":user}