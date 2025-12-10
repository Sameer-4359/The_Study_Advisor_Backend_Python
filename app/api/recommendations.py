# app/api/recommendations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from .. import schemas, algorithms
from ..database import get_db

router = APIRouter(prefix="/recommendations", tags=["recommendations"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.RecommendationResponse)
async def get_recommendations(
    request: schemas.RecommendationRequest,
    db: Session = Depends(get_db)
):
    """
    Get university recommendations based on student profile
    
    - **student_profile**: Detailed student profile
    - **top_k**: Number of recommendations to return (default: 5)
    """
    try:
        recommender = algorithms.HybridRecommender(db)
        
        # Get recommendations
        result = recommender.get_recommendations(
            student_profile=request.student_profile,
            top_k=request.top_k
        )
        
        if not result.get("recommendations"):
            raise HTTPException(
                status_code=404,
                detail=result.get("message", "No recommendations found")
            )
        
        # Convert to response format
        recommendations = []
        for rec in result["recommendations"]:
            recommendations.append(schemas.UniversityRecommendation(
                university=rec["university"],
                match_score=rec["final_score"],
                eligibility_score=rec["eligibility_score"],
                similarity_score=rec["similarity_score"],
                final_score=rec["final_score"],
                reasons=rec["reasons"]
            ))
        
        return schemas.RecommendationResponse(
            recommendations=recommendations,
            total_considered=result["total_considered"],
            algorithm_version=result["algorithm_version"],
            processing_time_ms=result["processing_time_ms"]
        )
        
    except Exception as e:
        logger.error(f"Error in recommendation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
async def test_recommendation(db: Session = Depends(get_db)):
    """
    Test endpoint with sample data
    """
    # Sample student profile for testing
    test_profile = schemas.StudentProfile(
        gpa=3.7,
        ielts_score=7.5,
        experience_years=2,
        research_experience=True,
        publications_count=1,
        work_experience_relevant=True,
        leadership_experience=True,
        current_education_level="BACHELORS",
        field_of_study="Computer Science",
        institution_name="NUST",
        desired_program="MASTERS",
        preferred_countries=["United States", "Canada", "United Kingdom"],
        budget_usd=50000,
        preferred_intake="FALL_2024",
        study_mode="FULL_TIME"
    )
    
    recommender = algorithms.HybridRecommender(db)
    result = recommender.get_recommendations(test_profile, top_k=3)
    
    return {
        "message": "Recommendation system is working",
        "test_profile": test_profile.dict(),
        "result": result
    }