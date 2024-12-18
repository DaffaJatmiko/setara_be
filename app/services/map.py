from sqlalchemy.orm import Session
from shapely.geometry import Point, Polygon
from geoalchemy2.shape import from_shape
from app.models.map import Gudang, Lahan
from geoalchemy2 import functions as geo_func
from shapely.geometry import mapping
from shapely import wkt
from shapely.wkt import dumps
from geoalchemy2.elements import WKTElement

from ..schemas.map import GudangRead

# CRUD Gudang
def create_gudang(db: Session, nama: str, lon: float, lat: float) -> Gudang:
    lokasi = WKTElement(f"POINT({lon} {lat})", srid=4326)
    gudang = Gudang(nama=nama, lokasi=lokasi)
    db.add(gudang)
    db.commit()
    db.refresh(gudang)
    
    # Ambil kembali data dengan lon dan lat terpisah
    lon, lat = db.query(
        geo_func.ST_X(Gudang.lokasi),
        geo_func.ST_Y(Gudang.lokasi)
    ).filter(Gudang.id == gudang.id).first()
    
    return GudangRead(
        id=gudang.id,
        nama=gudang.nama,
        lokasi=(lon, lat) 
    )

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
    # Konversi koordinat menjadi geometri WKT
    polygon_geom = Polygon(koordinat)
    polygon_wkt = dumps(polygon_geom)
    
    # Create the Lahan object with the WKT geometry
    lahan = Lahan(nama=nama, area=polygon_wkt)
    db.add(lahan)
    db.commit()
    db.refresh(lahan)

    return {
        "id": lahan.id,
        "nama": lahan.nama,
        "koordinat": koordinat
    }

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
