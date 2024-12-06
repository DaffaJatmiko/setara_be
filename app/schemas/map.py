from pydantic import BaseModel
from typing import List, Tuple

class GudangCreate(BaseModel):
    nama: str
    lokasi: Tuple[float, float]  # (longitude, latitude)

class GudangRead(GudangCreate):
    id: int
    nama: str
    lokasi: Tuple[float, float]

    class Config:
        orm_mode = True

class LahanCreate(BaseModel):
    nama: str
    koordinat: List[Tuple[float, float]]  # List of coordinates for polygon

class LahanRead(LahanCreate):
    id: int
    nama: str
    koordinat: List[Tuple[float, float]]
    class Config:
        from_attributes = True
