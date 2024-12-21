from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from app.core.database import Base
from shapely.geometry import Point

class Mitra(Base):
    __tablename__ = "mitra"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, default="Mitra Coffee", nullable=False)
    lokasi = Column(Geometry("POINT", srid=4326), nullable=False)

    @property
    def lokasi_coordinates(self):
        """
        Mengembalikan koordinat lokasi dalam bentuk tuple (longitude, latitude).
        """
        if self.lokasi:
            point = Point.from_wkb(self.lokasi)
            return (point.x, point.y)
        return None