from pydantic import BaseModel
from typing import Tuple

class MitraCreate(BaseModel):
    nama: str
    lokasi: Tuple[float, float]  # Lokasi dalam format (longitude, latitude)

class MitraRead(MitraCreate):
    id: int  # ID Mitra
    nama: str
    lokasi: Tuple[float, float]  # Lokasi dalam format (longitude, latitude)

    class Config:
        from_attributes = True
