from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from ..database.database import SessionLocal, get_db
from ..users.models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

SECRET_KEY = "jaciekrecealejaja123123cosiedzieje232323oho25"
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    acces_token: str
    token_type: str

db_dependency = Annotated[Session,Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    
    print(create_user_request.password)
    print(create_user_request.username)
    create_user_model = Users(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )
    print("Password type:", type(create_user_request.password))
    print("Password value:", create_user_request.password)

    db.add(create_user_model)
    db.commit()