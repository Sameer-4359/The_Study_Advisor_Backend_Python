# app/api/universities.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import schemas, models
from ..database import get_db

router = APIRouter(prefix="/universities", tags=["universities"])

@router.post("/", response_model=schemas.UniversityResponse)
def create_university(
    university: schemas.UniversityCreate,
    db: Session = Depends(get_db)
):
    db_university = models.University(**university.dict())
    db.add(db_university)
    db.commit()
    db.refresh(db_university)
    return db_university

@router.get("/", response_model=List[schemas.UniversityResponse])
def get_universities(
    skip: int = 0,
    limit: int = 100,
    country: Optional[str] = None,
    program_level: Optional[str] = None,
    field: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.University)
    
    if country:
        query = query.filter(models.University.country == country)
    if program_level:
        query = query.filter(models.University.program_level == program_level)
    if field:
        query = query.filter(models.University.fields_offered.contains([field]))
    
    return query.offset(skip).limit(limit).all()

@router.get("/{university_id}", response_model=schemas.UniversityResponse)
def get_university(university_id: int, db: Session = Depends(get_db)):
    university = db.query(models.University).filter(models.University.id == university_id).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    return university