from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from geoalchemy2 import functions as geo_func
from app.core.database import SessionLocal
from app.schemas.map import LahanCreate, LahanRead
from app.models.map import Lahan
from app.services.map import create_lahan, get_all_lahan, delete_lahan
from shapely import wkt

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LahanRead)
def add_lahan(lahan: LahanCreate, db: Session = Depends(get_db)):
    return create_lahan(db, lahan.nama, lahan.koordinat)

@router.get("/", response_model=list[LahanRead])
def list_lahan(db: Session = Depends(get_db)):
    print("Fetching list of Lahan")
    # Query Lahan dan ekstrak koordinat Polygon menggunakan ST_AsText (atau ST_AsGeoJSON)
    lahans = db.query(
        Lahan.id,
        Lahan.nama,
        geo_func.ST_AsText(Lahan.area).label("area_wkt")
    ).all()

    # Print data yang diambil
    print(f"Fetched {len(lahans)} Lahan records from database")

    # Mengubah koordinat WKT menjadi bentuk list of tuples (lon, lat)
    result = [
        LahanRead(
            id=l[0],
            nama=l[1],
            koordinat=parse_wkt_to_coordinates(l[2])  # Mengonversi WKT ke list koordinat
        ) for l in lahans
    ]
    
    # Print hasil konversi koordinat
    for item in result:
        print(f"Lahan {item.id} ({item.nama}) coordinates: {item.koordinat}")
    
    return result

def parse_wkt_to_coordinates(wkt_str: str):
    """ Fungsi untuk mengonversi WKT (Well Known Text) ke list koordinat """
    print(f"Parsing WKT: {wkt_str}")  # Pastikan ini adalah string WKT yang valid
    polygon = wkt.loads(wkt_str)  # Parsing WKT menjadi objek Polygon
    coordinates = list(polygon.exterior.coords)  # Mengembalikan koordinat sebagai list
    print(f"Parsed coordinates: {coordinates}")
    return coordinates

@router.delete("/{lahan_id}")
def remove_lahan(lahan_id: int, db: Session = Depends(get_db)):
    return delete_lahan(db, lahan_id)
