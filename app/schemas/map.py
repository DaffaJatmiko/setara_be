from pydantic import BaseModel
from typing import List, Tuple

class GudangCreate(BaseModel):
    nama: str
    lokasi: Tuple[float, float]  

class GudangRead(GudangCreate):
    id: int
    nama: str
    lokasi: Tuple[float, float]

    class Config:
        from_attributes = True

class LahanCreate(BaseModel):
    nama: str
    koordinat: list[list[float]]

class LahanRead(LahanCreate):
    id: int
    nama: str
    koordinat: List[Tuple[float, float]]
    class Config:
        from_attributes = True
