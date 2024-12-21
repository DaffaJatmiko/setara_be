# app/api/endpoints/lahan.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from geoalchemy2 import functions as geo_func
from app.core.database import SessionLocal
from app.core.middleware import RBACMiddleware
from app.schemas.map import LahanCreate, LahanRead
from app.models.map import Lahan
from app.services.map import create_lahan, get_all_lahan, delete_lahan
from shapely import wkt

from ...utils.helpers import parse_wkt_to_coordinates

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/", 
    response_model=LahanRead, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RBACMiddleware.require_role(['user', 'superuser']))]
)
def add_lahan(lahan: LahanCreate, db: Session = Depends(get_db)):
    return create_lahan(db, lahan.nama, lahan.koordinat)

@router.get(
    "/", 
    response_model=list[LahanRead]
)
def list_lahan(db: Session = Depends(get_db)):
    lahans = db.query(
        Lahan.id,
        Lahan.nama,
        geo_func.ST_AsText(Lahan.area).label("area_wkt")
    ).all()

    result = [
        LahanRead(
            id=l[0],
            nama=l[1],
            koordinat=parse_wkt_to_coordinates(l[2])
        ) for l in lahans
    ]
    return result

@router.delete(
    "/{lahan_id}",
    dependencies=[Depends(RBACMiddleware.require_role(['superuser']))]
)
def remove_lahan(lahan_id: int, db: Session = Depends(get_db)):
    return delete_lahan(db, lahan_id)
