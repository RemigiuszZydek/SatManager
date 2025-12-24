from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import List
import os
from ..users.models import Users
from ..database.database import get_db

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/login')

def require_roles(allowed_roles: List[str]):
    async def role_checker(user: dict = Depends(get_current_user)):
        if user['user_role'] not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return user
    return role_checker

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, str(user.hashed_password)):
        return False
    return user

def create_access_token(username: str, user_id: int, user_role: str, expires_delta: timedelta): 
    if SECRET_KEY is None or ALGORITHM is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Wrong SECRETKEY OR ALGORITHM")
    encode = {"sub": username, "id": user_id, "user_role": user_role, "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data:dict, expires_delta: timedelta= timedelta(days=7)):
    if SECRET_KEY is None or ALGORITHM is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Wrong SECRETKEY OR ALGORITHM")
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp":expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        if SECRET_KEY is None or ALGORITHM is None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Wrong SECRETKEY OR ALGORITHM")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('user_role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    

async def refresh_access_token(db:Session, refresh_token: str):
    payload = decode_token(refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload"
        )
    
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    new_access_token = create_access_token(
        username=user.username,
        user_id=user.id,
        user_role=user.role.name if user.role else "",
        expires_delta=timedelta(minutes=1)
    )

    return new_access_token