from sqlalchemy.orm import Session
from shapely.geometry import Point
from geoalchemy2.elements import WKTElement
from geoalchemy2 import functions as geo_func

from app.models.mitra import Mitra
from app.schemas.mitra import MitraRead


# CRUD Mitra
def create_mitra(db: Session, nama: str, lon: float, lat: float) -> MitraRead:
    lokasi = WKTElement(f"POINT({lon} {lat})", srid=4326)
    mitra = Mitra(nama=nama, lokasi=lokasi)
    db.add(mitra)
    db.commit()
    db.refresh(mitra)

    # Ambil kembali data dengan lon dan lat terpisah
    lon, lat = db.query(
        geo_func.ST_X(Mitra.lokasi),
        geo_func.ST_Y(Mitra.lokasi)
    ).filter(Mitra.id == mitra.id).first()

    return MitraRead(
        id=mitra.id,
        nama=mitra.nama,
        lokasi=(lon, lat)
    )


def get_all_mitra(db: Session):
    """
    Mengembalikan semua data Mitra dalam bentuk daftar objek MitraRead.
    """
    mitra_list = db.query(Mitra).all()
    mitra_read_list = []
    for mitra in mitra_list:
        lon, lat = db.query(
            geo_func.ST_X(Mitra.lokasi),
            geo_func.ST_Y(Mitra.lokasi)
        ).filter(Mitra.id == mitra.id).first()
        mitra_read_list.append(MitraRead(
            id=mitra.id,
            nama=mitra.nama,
            lokasi=(lon, lat)
        ))
    return mitra_read_list


def get_mitra_by_id(db: Session, mitra_id: int) -> MitraRead:
    """
    Mengambil data Mitra berdasarkan ID.
    """
    mitra = db.query(Mitra).filter(Mitra.id == mitra_id).first()
    if not mitra:
        return None

    lon, lat = db.query(
        geo_func.ST_X(Mitra.lokasi),
        geo_func.ST_Y(Mitra.lokasi)
    ).filter(Mitra.id == mitra.id).first()

    return MitraRead(
        id=mitra.id,
        nama=mitra.nama,
        lokasi=(lon, lat)
    )


def update_mitra(db: Session, mitra_id: int, nama: str, lon: float, lat: float) -> MitraRead:
    """
    Memperbarui data Mitra berdasarkan ID.
    """
    mitra = db.query(Mitra).filter(Mitra.id == mitra_id).first()
    if not mitra:
        return None

    lokasi = WKTElement(f"POINT({lon} {lat})", srid=4326)
    mitra.nama = nama
    mitra.lokasi = lokasi

    db.commit()
    db.refresh(mitra)

    lon, lat = db.query(
        geo_func.ST_X(Mitra.lokasi),
        geo_func.ST_Y(Mitra.lokasi)
    ).filter(Mitra.id == mitra.id).first()

    return MitraRead(
        id=mitra.id,
        nama=mitra.nama,
        lokasi=(lon, lat)
    )


def delete_mitra(db: Session, mitra_id: int) -> bool:
    """
    Menghapus data Mitra berdasarkan ID.
    """
    mitra = db.query(Mitra).filter(Mitra.id == mitra_id).first()
    if not mitra:
        return False

    db.delete(mitra)
    db.commit()
    return True