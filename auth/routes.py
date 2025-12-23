from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated
from .dependencies import authenticate_user, create_access_token, get_current_user, refresh_access_token
from ..database.database import get_db
from ..users.models import CreateUserRequest, Token, Users
from ..users import services
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

db_dependency = Annotated[Session, Depends(get_db)]

# register
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(create_user_request: CreateUserRequest, db: db_dependency):
    user = services.create_user(db, create_user_request.username, create_user_request.password, create_user_request.user_role)
    return {"id": user.id, "username": user.username, "user_role":user.role_id, "user_role":user.role}

# login
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    access_token, refresh_token = services.login_user(db, form_data.username, form_data.password, timedelta(minutes=1))
    return {"access_token": access_token,"refresh_token":refresh_token , "token_type": "bearer",}

#refresh
@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(db: db_dependency,
                                 refresh_token: str = Body(..., embed=True)):
    new_access_token = await refresh_access_token(db, refresh_token)
    return {
    "access_token": new_access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
}