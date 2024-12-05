# app/api/endpoints/programs.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.middleware import RBACMiddleware
from app.schemas.program import ProgramCreate, ProgramUpdate, ProgramInDB
from app.services.program import ProgramService

router = APIRouter()

@router.post(
    "/", 
    response_model=ProgramInDB, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RBACMiddleware.require_role(['user', 'superuser']))]
)
def create_program(
    program: ProgramCreate, 
    db: Session = Depends(get_db)
):
    return ProgramService.create_program(db, program)

@router.get(
    "/", 
    response_model=List[ProgramInDB],
    dependencies=[Depends(RBACMiddleware.require_role(['user', 'superuser']))]
)
def read_programs(
    skip: int = 0, 
    limit: int = 100, 
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return ProgramService.get_all_programs(db, skip, limit, is_active)

@router.get(
    "/{program_id}", 
    response_model=ProgramInDB,
    dependencies=[Depends(RBACMiddleware.require_role(['user', 'superuser']))]
)
def read_program(
    program_id: int, 
    db: Session = Depends(get_db)
):
    return ProgramService.get_program_by_id(db, program_id)

@router.put(
    "/{program_id}", 
    response_model=ProgramInDB,
    dependencies=[Depends(RBACMiddleware.require_role(['user', 'superuser']))]
)
def update_program(
    program_id: int, 
    program: ProgramUpdate, 
    db: Session = Depends(get_db)
):
    return ProgramService.update_program(db, program_id, program)

@router.delete(
    "/{program_id}",
    dependencies=[Depends(RBACMiddleware.require_role(['superuser']))]
)
def delete_program(
    program_id: int, 
    db: Session = Depends(get_db)
):
    return ProgramService.delete_program(db, program_id)