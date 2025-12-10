# # app/models.py
# from sqlalchemy import Column, Integer, String, Float, Boolean, Text, Enum, ForeignKey, DateTime, ARRAY
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func
# from .database import Base
# import enum

# # Define enums
# class EducationLevel(str, enum.Enum):
#     HIGH_SCHOOL = "HIGH_SCHOOL"
#     BACHELORS = "BACHELORS"
#     MASTERS = "MASTERS"
#     PHD = "PHD"
#     POST_DOCTORAL = "POST_DOCTORAL"

# class ProgramType(str, enum.Enum):
#     BACHELORS = "BACHELORS"
#     MASTERS = "MASTERS"
#     PHD = "PHD"
#     POST_DOCTORAL = "POST_DOCTORAL"
#     DIPLOMA = "DIPLOMA"
#     FOUNDATION = "FOUNDATION"
#     PG_DIPLOMA = "PG_DIPLOMA"
#     MBA = "MBA"
#     RESEARCH_MASTERS = "RESEARCH_MASTERS"
#     EXECUTIVE_EDUCATION = "EXECUTIVE_EDUCATION"
#     RESEARCH_FELLOWSHIP = "RESEARCH_FELLOWSHIP"
#     EXCHANGE = "EXCHANGE"

# class Country(str, enum.Enum):
#     UNITED_STATES = "United States"
#     UNITED_KINGDOM = "United Kingdom"
#     CANADA = "Canada"
#     AUSTRALIA = "Australia"
#     GERMANY = "Germany"
#     FRANCE = "France"
#     NETHERLANDS = "Netherlands"
#     SWEDEN = "Sweden"
#     NORWAY = "Norway"
#     DENMARK = "Denmark"
#     SWITZERLAND = "Switzerland"
#     IRELAND = "Ireland"
#     NEW_ZEALAND = "New Zealand"
#     SINGAPORE = "Singapore"
#     MALAYSIA = "Malaysia"
#     JAPAN = "Japan"
#     SOUTH_KOREA = "South Korea"
#     CHINA = "China"
#     ITALY = "Italy"
#     SPAIN = "Spain"

# class University(Base):
#     __tablename__ = "universities"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), nullable=False, unique=True)
#     country = Column(String(100), nullable=False)
#     world_ranking = Column(Integer)
#     acceptance_rate = Column(Float)
#     website = Column(String(255))
#     description = Column(Text)
    
#     # Eligibility criteria
#     min_gpa = Column(Float, nullable=False)
#     min_ielts = Column(Float, nullable=False)
#     min_toefl = Column(Integer)
#     min_gre = Column(Integer)
#     min_gmat = Column(Integer)
#     min_experience_years = Column(Integer, default=0)
    
#     # Program information
#     program_name = Column(String(255), nullable=False)
#     program_level = Column(String(50), nullable=False)  # BACHELORS, MASTERS, PHD
#     program_type = Column(String(50))  # FULL_TIME, PART_TIME, ONLINE
#     program_duration_months = Column(Integer)
    
#     # Financial information
#     tuition_fee_usd = Column(Float, nullable=False)
#     scholarship_available = Column(Boolean, default=False)
#     avg_scholarship_percentage = Column(Float)
    
#     # Fields/Departments offered
#     fields_offered = Column(ARRAY(String))  # Array of fields like ["CS", "Business", "Engineering"]
    
#     # Requirements
#     requires_portfolio = Column(Boolean, default=False)
#     requires_research_proposal = Column(Boolean, default=False)
#     requires_interview = Column(Boolean, default=False)
    
#     # Dates
#     application_deadline = Column(String(100))
#     intake_seasons = Column(ARRAY(String))  # ["FALL", "SPRING", "SUMMER"]
    
#     # Additional metrics
#     graduation_rate = Column(Float)
#     employment_rate_6_months = Column(Float)
#     avg_starting_salary_usd = Column(Float)
    
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# class StudentAdmissionHistory(Base):
#     __tablename__ = "student_admission_history"
    
#     id = Column(Integer, primary_key=True, index=True)
#     student_id = Column(Integer, nullable=False)
    
#     # Student profile at time of application
#     gpa = Column(Float, nullable=False)
#     ielts_score = Column(Float)
#     toefl_score = Column(Integer)
#     gre_score = Column(Integer)
#     gmat_score = Column(Integer)
#     experience_years = Column(Integer, default=0)
    
#     # Academic background
#     previous_degree = Column(String(100))
#     previous_university = Column(String(255))
#     field_of_study = Column(String(100))
    
#     # Extracurriculars
#     research_experience = Column(Boolean, default=False)
#     publications_count = Column(Integer, default=0)
#     work_experience_relevant = Column(Boolean, default=False)
#     leadership_experience = Column(Boolean, default=False)
    
#     # Application details
#     university_applied_id = Column(Integer, ForeignKey("universities.id"))
#     university_applied = relationship("University")
#     program_applied = Column(String(255), nullable=False)
#     application_status = Column(String(50))  # ACCEPTED, REJECTED, WAITLISTED
#     scholarship_received = Column(Boolean, default=False)
#     scholarship_amount_usd = Column(Float)
    
#     # Timeline
#     application_date = Column(DateTime(timezone=True))
#     decision_date = Column(DateTime(timezone=True))
    
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

# class RecommendationResult(Base):
#     __tablename__ = "recommendation_results"
    
#     id = Column(Integer, primary_key=True, index=True)
#     student_id = Column(Integer, nullable=False)
    
#     # Input parameters
#     input_gpa = Column(Float, nullable=False)
#     input_ielts = Column(Float)
#     input_experience_years = Column(Integer)
#     input_field = Column(String(100))
#     input_program_level = Column(String(50))
#     input_budget_usd = Column(Float)
    
#     # Results
#     recommended_university_ids = Column(ARRAY(Integer))
#     recommendation_scores = Column(ARRAY(Float))  # Scores for each recommendation
#     algorithm_version = Column(String(50), default="v1.0")
    
#     created_at = Column(DateTime(timezone=True), server_default=func.now())


# app/models.py - UPDATED VERSION
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY  # Change this import
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

# Define enums (keep as is)
class EducationLevel(str, enum.Enum):
    HIGH_SCHOOL = "HIGH_SCHOOL"
    BACHELORS = "BACHELORS"
    MASTERS = "MASTERS"
    PHD = "PHD"
    POST_DOCTORAL = "POST_DOCTORAL"

class ProgramType(str, enum.Enum):
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

class Country(str, enum.Enum):
    UNITED_STATES = "United States"
    UNITED_KINGDOM = "United Kingdom"
    CANADA = "Canada"
    AUSTRALIA = "Australia"
    GERMANY = "Germany"
    FRANCE = "France"
    NETHERLANDS = "Netherlands"
    SWEDEN = "Sweden"
    NORWAY = "Norway"
    DENMARK = "Denmark"
    SWITZERLAND = "Switzerland"
    IRELAND = "Ireland"
    NEW_ZEALAND = "New Zealand"
    SINGAPORE = "Singapore"
    MALAYSIA = "Malaysia"
    JAPAN = "Japan"
    SOUTH_KOREA = "South Korea"
    CHINA = "China"
    ITALY = "Italy"
    SPAIN = "Spain"
    PAKISTAN = "Pakistan"

class University(Base):
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    country = Column(String(100), nullable=False)
    world_ranking = Column(Integer)
    acceptance_rate = Column(Float)
    website = Column(String(255))
    description = Column(Text)
    
    # Eligibility criteria
    min_gpa = Column(Float, nullable=False)
    min_ielts = Column(Float, nullable=False)
    min_toefl = Column(Integer)
    min_gre = Column(Integer)
    min_gmat = Column(Integer)
    min_experience_years = Column(Integer, default=0)
    
    # Program information
    program_name = Column(String(255), nullable=False)
    program_level = Column(String(50), nullable=False)  # BACHELORS, MASTERS, PHD
    program_type = Column(String(50))  # FULL_TIME, PART_TIME, ONLINE
    program_duration_months = Column(Integer)
    
    # Financial information
    tuition_fee_usd = Column(Float, nullable=False)
    scholarship_available = Column(Boolean, default=False)
    avg_scholarship_percentage = Column(Float)
    
    # Fields/Departments offered - FIXED
    fields_offered = Column(ARRAY(String))  # Use PostgreSQL ARRAY
    
    # Requirements
    requires_portfolio = Column(Boolean, default=False)
    requires_research_proposal = Column(Boolean, default=False)
    requires_interview = Column(Boolean, default=False)
    
    # Dates
    application_deadline = Column(String(100))
    intake_seasons = Column(ARRAY(String))  # Use PostgreSQL ARRAY
    
    # Additional metrics
    graduation_rate = Column(Float)
    employment_rate_6_months = Column(Float)
    avg_starting_salary_usd = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class StudentAdmissionHistory(Base):
    __tablename__ = "student_admission_history"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    
    # Student profile at time of application
    gpa = Column(Float, nullable=False)
    ielts_score = Column(Float)
    toefl_score = Column(Integer)
    gre_score = Column(Integer)
    gmat_score = Column(Integer)
    experience_years = Column(Integer, default=0)
    
    # Academic background
    previous_degree = Column(String(100))
    previous_university = Column(String(255))
    field_of_study = Column(String(100))
    
    # Extracurriculars
    research_experience = Column(Boolean, default=False)
    publications_count = Column(Integer, default=0)
    work_experience_relevant = Column(Boolean, default=False)
    leadership_experience = Column(Boolean, default=False)
    
    # Application details
    university_applied_id = Column(Integer, ForeignKey("universities.id"))
    university_applied = relationship("University")
    program_applied = Column(String(255), nullable=False)
    application_status = Column(String(50))  # ACCEPTED, REJECTED, WAITLISTED
    scholarship_received = Column(Boolean, default=False)
    scholarship_amount_usd = Column(Float)
    
    # Timeline
    application_date = Column(DateTime(timezone=True))
    decision_date = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RecommendationResult(Base):
    __tablename__ = "recommendation_results"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, nullable=False)
    
    # Input parameters
    input_gpa = Column(Float, nullable=False)
    input_ielts = Column(Float)
    input_experience_years = Column(Integer)
    input_field = Column(String(100))
    input_program_level = Column(String(50))
    input_budget_usd = Column(Float)
    
    # Results
    recommended_university_ids = Column(ARRAY(Integer))  # Use PostgreSQL ARRAY
    recommendation_scores = Column(ARRAY(Float))  # Use PostgreSQL ARRAY
    algorithm_version = Column(String(50), default="v1.0")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())