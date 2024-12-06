from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_AsText
from app.core.database import Base
from shapely.geometry import Point

class Gudang(Base):
    __tablename__ = "gudang"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    lokasi = Column(Geometry("POINT", srid=4326), nullable=False)

    @property
    def lokasi_coordinates(self):
        # Get WKB as text (WKT format), then convert it to a Shapely Point object
        point = self.lokasi and Point.from_wkb(self.lokasi)
        if point:
            return (point.x, point.y)  # Return tuple of coordinates
        return None

class Lahan(Base):
    __tablename__ = "lahan"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    area = Column(Geometry("POLYGON", srid=4326), nullable=False)
