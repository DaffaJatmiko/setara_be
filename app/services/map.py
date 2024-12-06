from sqlalchemy.orm import Session
from shapely.geometry import Point, Polygon
from geoalchemy2.shape import from_shape
from app.models.map import Gudang, Lahan
from geoalchemy2 import functions as geo_func


# CRUD Gudang
def create_gudang(db: Session, nama: str, lon: float, lat: float):
    # Create a Point object with lon, lat
    lokasi = from_shape(Point(lon, lat), srid=4326)
    gudang = Gudang(nama=nama, lokasi=lokasi)
    db.add(gudang)
    db.commit()
    db.refresh(gudang)
    return gudang

def get_all_gudang(db: Session):
    return db.query(Gudang).all()

def delete_gudang(db: Session, gudang_id: int):
    # Use filter instead of deprecated .get()
    gudang = db.query(Gudang).filter(Gudang.id == gudang_id).first()
    if gudang:
        db.delete(gudang)
        db.commit()
    return gudang

# CRUD Lahan
def create_lahan(db: Session, nama: str, koordinat: list):
    # Ensure the polygon is closed by repeating the first coordinate
    if koordinat[0] != koordinat[-1]:
        koordinat.append(koordinat[0])  # Close the polygon

    # Create a Polygon object
    area = from_shape(Polygon(koordinat), srid=4326)
    lahan = Lahan(nama=nama, area=area)
    db.add(lahan)
    db.commit()
    db.refresh(lahan)
    return lahan

def get_all_lahan(db: Session):
    return db.query(
        Lahan.id,
        Lahan.nama,
        geo_func.ST_AsText(Lahan.area).label("area_wkt")  # Menggunakan ST_AsText untuk mengonversi area ke WKT
    ).all()

def delete_lahan(db: Session, lahan_id: int):
    # Use filter instead of deprecated .get()
    lahan = db.query(Lahan).filter(Lahan.id == lahan_id).first()
    if lahan:
        db.delete(lahan)
        db.commit()
    return lahan
