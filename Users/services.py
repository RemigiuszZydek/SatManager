from datetime import timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status
from .models import Users
from ..auth.dependencies import create_access_token, create_refresh_token, authenticate_user as base_authenticate_user

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def create_user(db: Session, username: str, password: str, user_role: int) -> Users:
    existing_user = db.query(Users).filter(Users.username == username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")
    
    user = Users(
        username=username,
        hashed_password=bcrypt_context.hash(password),
        role_id=user_role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, username: str, password: str, token_expires: timedelta):
    user = base_authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    
    access_token = create_access_token(
        username=user.username,
        user_id=user.id,
        user_role=user.role.name if user.role else "",
        expires_delta=token_expires
    )

    refresh_token = create_refresh_token(data={"sub": user.username})

    return access_token, refresh_token