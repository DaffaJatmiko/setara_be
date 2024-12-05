# app/core/middleware.py
from fastapi import Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User

class RBACMiddleware:
    @staticmethod
    def require_role(allowed_roles=None):
        if allowed_roles is None:
            allowed_roles = ['user']  # Default roles

        def role_checker(request: Request):
            # Dapatkan token dari header Authorization
            authorization = request.headers.get('Authorization')
            if not authorization:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token tidak ditemukan"
                )

            # Validasi token
            token = authorization.split(' ')[-1]
            payload = decode_token(token)
            
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token tidak valid"
                )

            # Dapatkan database session
            db = next(get_db())
            
            # Cari user berdasarkan username di token
            user = db.query(User).filter(User.username == payload.get('sub')).first()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User tidak ditemukan"
                )

            # Cek role (contoh sederhana, bisa dikembangkan)
            if 'superuser' in allowed_roles and user.is_superuser:
                return user
            elif 'user' in allowed_roles and user.is_active:
                return user
            
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Akses ditolak"
            )

        return role_checker