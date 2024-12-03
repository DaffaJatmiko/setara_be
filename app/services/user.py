# app/services/user_service.py
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate):
        # Cek apakah username atau email sudah ada
        existing_user = db.query(User).filter(
            or_(User.username == user.username, User.email == user.email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username atau email sudah terdaftar"
            )
        
        # Hash password sebelum disimpan
        hashed_password = get_password_hash(user.password)
        
        db_user = User(
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        
        if not user:
            return False
        
        if not verify_password(password, user.hashed_password):
            return False
        
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()