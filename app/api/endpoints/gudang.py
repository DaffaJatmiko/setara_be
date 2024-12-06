from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2 import functions as geo_func
from app.core.database import SessionLocal
from app.schemas.map import GudangCreate, GudangRead
from app.models.map import Gudang
from app.services.map import create_gudang, get_all_gudang, delete_gudang

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=GudangRead)
def add_gudang(gudang: GudangCreate, db: Session = Depends(get_db)):
    return create_gudang(db, gudang.nama, gudang.lokasi[0], gudang.lokasi[1])

@router.get("/", response_model=list[GudangRead])
def list_gudang(db: Session = Depends(get_db)):
    # Query Gudang and extract ST_X and ST_Y directly from the database
    gudangs = db.query(
        Gudang.id,
        Gudang.nama,
        geo_func.ST_X(Gudang.lokasi).label("lon"),
        geo_func.ST_Y(Gudang.lokasi).label("lat")
    ).all()

    return [
        GudangRead(
            id=g[0],
            nama=g[1],
            lokasi=(float(g[2]), float(g[3]))  # Extract and cast lon, lat as float
        ) for g in gudangs
    ]
@router.delete("/{gudang_id}")
def remove_gudang(gudang_id: int, db: Session = Depends(get_db)):
    return delete_gudang(db, gudang_id)