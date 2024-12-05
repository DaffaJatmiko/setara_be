# app/api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserInDB, Token
from app.services.user import UserService
from app.core.security import create_access_token, get_current_user
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserInDB)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserService.create_user(db, user)

@router.post("/login", response_model=Token)
def login_user(
    user_login: UserLogin, 
    db: Session = Depends(get_db)
):
    user = UserService.authenticate_user(
        db, 
        user_login.username, 
        user_login.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserInDB)
def read_users_me(
    current_user = Depends(get_current_user)
):
    return current_user