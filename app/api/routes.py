# app/api/routes.py
from fastapi import APIRouter

# Import router spesifik dari setiap endpoint
from app.api.endpoints import (
    users,       # Endpoint manajemen user
    # news,        # Endpoint berita
    programs,    # Endpoint program
    # maps         # Endpoint peta
)

# Buat router utama
api_router = APIRouter()

# Include router spesifik dengan prefix
api_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["users"]
)

api_router.include_router(
    programs.router, 
    prefix="/programs", 
    tags=["programs"]
)

# api_router.include_router(
#     news.router, 
#     prefix="/news", 
#     tags=["news"]
# )

# api_router.include_router(
#     programs.router, 
#     prefix="/programs", 
#     tags=["programs"]
# )

# api_router.include_router(
#     maps.router, 
#     prefix="/maps", 
#     tags=["maps"]
# )