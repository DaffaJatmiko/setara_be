# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.database import Base, engine
from app.core.config import settings
from app.core.global_middleware import GlobalMiddleware

import logging

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Buat semua tabel di database
Base.metadata.create_all(bind=engine)

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Backend untuk web profile"
    )
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Global Middleware
    app.add_middleware(GlobalMiddleware)
    
    # Include router
    app.include_router(api_router, prefix="/api")
    
    return app

app = create_application()

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )