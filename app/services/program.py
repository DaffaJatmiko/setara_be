# app/services/program_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.program import Program
from app.schemas.program import ProgramCreate, ProgramUpdate
from typing import List, Optional

class ProgramService:
    @staticmethod
    def create_program(db: Session, program: ProgramCreate):
        # Create a new program
        db_program = Program(**program.model_dump())
        
        db.add(db_program)
        db.commit()
        db.refresh(db_program)
        
        return db_program
    
    @staticmethod
    def get_program_by_id(db: Session, program_id: int):
        program = db.query(Program).filter(Program.id == program_id).first()
        
        if not program:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Program not found"
            )
        
        return program
    
    @staticmethod
    def get_all_programs(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        is_active: Optional[bool] = None
    ) -> List[Program]:
        query = db.query(Program)
        
        if is_active is not None:
            query = query.filter(Program.is_active == is_active)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_program(
        db: Session, 
        program_id: int, 
        program: ProgramUpdate
    ):
        # Fetch existing program
        db_program = db.query(Program).filter(Program.id == program_id).first()
        
        if not db_program:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Program not found"
            )
        
        # Update program details
        for key, value in program.model_dump(exclude_unset=True).items():
            setattr(db_program, key, value)
        
        db.commit()
        db.refresh(db_program)
        
        return db_program
    
    @staticmethod
    def delete_program(
        db: Session, 
        program_id: int
    ):
        # Fetch existing program
        db_program = db.query(Program).filter(Program.id == program_id).first()
        
        if not db_program:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Program not found"
            )
        
        db.delete(db_program)
        db.commit()
        
        return {"detail": "Program deleted successfully"}