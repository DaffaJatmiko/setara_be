# app/api/endpoints/mitra.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.middleware import RBACMiddleware
from app.schemas.mitra import MitraCreate, MitraRead
from app.services.mitra import create_mitra, get_all_mitra, get_mitra_by_id, update_mitra, delete_mitra

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Mitra
@router.post(
    "/", 
    response_model=MitraRead, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RBACMiddleware.require_role(['user', 'superuser']))]
)
def add_mitra(mitra: MitraCreate, db: Session = Depends(get_db)):
    return create_mitra(db, mitra.nama, mitra.lokasi[0], mitra.lokasi[1])

# Get All Mitra
@router.get(
    "/", 
    response_model=list[MitraRead]
)
def list_mitra(db: Session = Depends(get_db)):
    return get_all_mitra(db)

# Get Mitra by ID
@router.get(
    "/{mitra_id}", 
    response_model=MitraRead
)
def get_mitra(mitra_id: int, db: Session = Depends(get_db)):
    mitra = get_mitra_by_id(db, mitra_id)
    if not mitra:
        return {"error": "Mitra not found"}
    return mitra

# Update Mitra
@router.put(
    "/{mitra_id}", 
    response_model=MitraRead,
    dependencies=[Depends(RBACMiddleware.require_role(['user', 'superuser']))]
)
def edit_mitra(mitra_id: int, mitra: MitraCreate, db: Session = Depends(get_db)):
    updated_mitra = update_mitra(db, mitra_id, mitra.nama, mitra.lokasi[0], mitra.lokasi[1])
    if not updated_mitra:
        return {"error": "Mitra not found or update failed"}
    return updated_mitra

# Delete Mitra
@router.delete(
    "/{mitra_id}",
    dependencies=[Depends(RBACMiddleware.require_role(['superuser']))]
)
def remove_mitra(mitra_id: int, db: Session = Depends(get_db)):
    success = delete_mitra(db, mitra_id)
    if not success:
        return {"error": "Mitra not found or delete failed"}
    return {"message": "Mitra deleted successfully"}