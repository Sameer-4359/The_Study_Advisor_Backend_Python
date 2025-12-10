# app/schemas.py
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums for API
class EducationLevel(str, Enum):
    HIGH_SCHOOL = "HIGH_SCHOOL"
    BACHELORS = "BACHELORS"
    MASTERS = "MASTERS"
    PHD = "PHD"
    POST_DOCTORAL = "POST_DOCTORAL"

class ProgramType(str, Enum):
    BACHELORS = "BACHELORS"
    MASTERS = "MASTERS"
    PHD = "PHD"
    POST_DOCTORAL = "POST_DOCTORAL"
    DIPLOMA = "DIPLOMA"
    FOUNDATION = "FOUNDATION"
    PG_DIPLOMA = "PG_DIPLOMA"
    MBA = "MBA"
    RESEARCH_MASTERS = "RESEARCH_MASTERS"
    EXECUTIVE_EDUCATION = "EXECUTIVE_EDUCATION"
    RESEARCH_FELLOWSHIP = "RESEARCH_FELLOWSHIP"
    EXCHANGE = "EXCHANGE"

class StudyMode(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    ONLINE = "ONLINE"
    HYBRID = "HYBRID"

# Request/Response schemas
class UniversityBase(BaseModel):
    name: str
    country: str
    world_ranking: Optional[int] = None
    acceptance_rate: Optional[float] = None
    website: Optional[str] = None
    description: Optional[str] = None
    
    min_gpa: float = Field(..., ge=0.0, le=4.0)
    min_ielts: float = Field(..., ge=0.0, le=9.0)
    min_toefl: Optional[int] = None
    min_gre: Optional[int] = None
    min_gmat: Optional[int] = None
    min_experience_years: int = 0
    
    program_name: str
    program_level: str
    program_type: Optional[str] = None
    program_duration_months: Optional[int] = None
    
    tuition_fee_usd: float
    scholarship_available: bool = False
    avg_scholarship_percentage: Optional[float] = None
    
    fields_offered: List[str] = []
    requires_portfolio: bool = False
    requires_research_proposal: bool = False
    requires_interview: bool = False
    
    application_deadline: Optional[str] = None
    intake_seasons: List[str] = []

class UniversityCreate(UniversityBase):
    pass

class UniversityResponse(UniversityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class StudentProfile(BaseModel):
    # Academic
    gpa: float = Field(..., ge=0.0, le=4.0, description="GPA on 4.0 scale")
    ielts_score: Optional[float] = Field(None, ge=0.0, le=9.0)
    toefl_score: Optional[int] = Field(None, ge=0, le=120)
    gre_score: Optional[int] = Field(None, ge=260, le=340)
    gmat_score: Optional[int] = Field(None, ge=200, le=800)
    
    # Experience
    experience_years: int = Field(0, ge=0)
    research_experience: bool = False
    publications_count: int = 0
    work_experience_relevant: bool = False
    leadership_experience: bool = False
    
    # Education background
    current_education_level: str
    field_of_study: str
    institution_name: Optional[str] = None
    
    # Preferences
    desired_program: str
    preferred_countries: List[str] = []
    budget_usd: Optional[float] = None
    preferred_intake: Optional[str] = None
    study_mode: Optional[str] = None
    
    @validator('current_education_level')
    def validate_education_level(cls, v):
        valid_levels = [e.value for e in EducationLevel]
        if v not in valid_levels:
            raise ValueError(f"Education level must be one of: {valid_levels}")
        return v
    
    @validator('desired_program')
    def validate_program(cls, v):
        valid_programs = [p.value for p in ProgramType]
        if v not in valid_programs:
            raise ValueError(f"Program must be one of: {valid_programs}")
        return v

class RecommendationRequest(BaseModel):
    student_profile: StudentProfile
    top_k: int = Field(5, ge=1, le=20, description="Number of recommendations to return")

class UniversityRecommendation(BaseModel):
    university: UniversityResponse
    match_score: float = Field(..., ge=0.0, le=1.0)
    eligibility_score: float = Field(..., ge=0.0, le=1.0)
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    final_score: float = Field(..., ge=0.0, le=1.0)
    reasons: List[str] = []

class RecommendationResponse(BaseModel):
    recommendations: List[UniversityRecommendation]
    total_considered: int
    algorithm_version: str
    processing_time_ms: float