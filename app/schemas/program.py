# app/schemas/program.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProgramBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: Optional[bool] = True

class ProgramCreate(ProgramBase):
    pass

class ProgramUpdate(ProgramBase):
    pass

class ProgramInDB(ProgramBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True