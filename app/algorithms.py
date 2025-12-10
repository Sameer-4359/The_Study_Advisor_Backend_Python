# # app/algorithms.py
# # app/algorithms.py - UPDATED VERSION
# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.metrics.pairwise import cosine_similarity
# from typing import List, Dict, Any, Tuple
# from sqlalchemy.orm import Session
# from sqlalchemy import or_, and_
# from . import models, schemas
# import time

# class HybridRecommender:
#     def __init__(self, db: Session):
#         self.db = db
#         self.scaler = MinMaxScaler()
        
#     def get_eligible_universities(self, student_profile: schemas.StudentProfile) -> List[models.University]:
#         """Step 1: Rule-based filtering"""
#         query = self.db.query(models.University)
        
#         # Filter by program level
#         query = query.filter(models.University.program_level == student_profile.desired_program)
        
#         # Filter by field of study - FIXED for PostgreSQL arrays
#         # Instead of .contains([value]), use SQLAlchemy's array contains operator
#         query = query.filter(models.University.fields_offered.any(student_profile.field_of_study))
        
#         # Filter by GPA
#         query = query.filter(models.University.min_gpa <= student_profile.gpa)
        
#         # Filter by IELTS if provided
#         if student_profile.ielts_score:
#             query = query.filter(models.University.min_ielts <= student_profile.ielts_score)
        
#         # Filter by experience
#         query = query.filter(models.University.min_experience_years <= student_profile.experience_years)
        
#         # Filter by budget if provided
#         if student_profile.budget_usd:
#             query = query.filter(models.University.tuition_fee_usd <= student_profile.budget_usd)
        
#         # Filter by preferred countries if provided
#         if student_profile.preferred_countries:
#             query = query.filter(models.University.country.in_(student_profile.preferred_countries))
        
#         return query.all()
    
#     # Rest of the methods remain the same...
    
#     def calculate_eligibility_score(self, university: models.University, student_profile: schemas.StudentProfile) -> float:
#         """Calculate how well student meets university requirements"""
#         score = 0.0
#         total_weight = 0
        
#         # GPA score (40% weight)
#         if university.min_gpa <= student_profile.gpa:
#             gpa_score = min(1.0, student_profile.gpa / 4.0)
#             score += gpa_score * 0.4
#             total_weight += 0.4
        
#         # IELTS score (20% weight)
#         if student_profile.ielts_score and university.min_ielts:
#             if student_profile.ielts_score >= university.min_ielts:
#                 ielts_score = min(1.0, student_profile.ielts_score / 9.0)
#                 score += ielts_score * 0.2
#                 total_weight += 0.2
        
#         # Experience score (15% weight)
#         exp_ratio = min(1.0, student_profile.experience_years / max(university.min_experience_years, 1))
#         score += exp_ratio * 0.15
#         total_weight += 0.15
        
#         # Additional qualifications (25% weight)
#         additional_score = 0.0
        
#         # Research experience
#         if student_profile.research_experience and (university.program_level in ["MASTERS", "PHD", "RESEARCH_MASTERS"]):
#             additional_score += 0.1
        
#         # Publications
#         if student_profile.publications_count > 0 and university.program_level in ["PHD", "RESEARCH_FELLOWSHIP"]:
#             pub_score = min(0.1, student_profile.publications_count * 0.02)
#             additional_score += pub_score
        
#         # Relevant work experience
#         if student_profile.work_experience_relevant and university.program_level in ["MBA", "EXECUTIVE_EDUCATION"]:
#             additional_score += 0.05
        
#         # Leadership experience
#         if student_profile.leadership_experience:
#             additional_score += 0.05
        
#         score += additional_score * 0.25
#         total_weight += 0.25
        
#         # Normalize by total weight applied
#         if total_weight > 0:
#             score = score / total_weight
        
#         return min(1.0, score)
    
#     def calculate_similarity_score(self, university: models.University, student_profile: schemas.StudentProfile) -> float:
#         """Calculate similarity based on historical admissions"""
#         # Get historical admissions data for this university and program
#         history_query = self.db.query(models.StudentAdmissionHistory).filter(
#             models.StudentAdmissionHistory.university_applied_id == university.id,
#             models.StudentAdmissionHistory.program_applied == university.program_level,
#             models.StudentAdmissionHistory.application_status == "ACCEPTED"
#         ).limit(100)  # Limit to recent 100 for performance
        
#         history = history_query.all()
        
#         if not history:
#             return 0.5  # Default neutral score if no history
        
#         # Prepare feature vectors
#         features = []
#         student_vector = []
        
#         # Define feature weights
#         feature_weights = {
#             'gpa': 0.3,
#             'ielts_score': 0.2,
#             'experience_years': 0.15,
#             'research_experience': 0.15,
#             'publications_count': 0.1,
#             'work_experience_relevant': 0.1
#         }
        
#         for record in history:
#             record_features = [
#                 record.gpa / 4.0,  # Normalized GPA
#                 (record.ielts_score or 0) / 9.0,  # Normalized IELTS
#                 min(1.0, record.experience_years / 10.0),  # Normalized experience
#                 1.0 if record.research_experience else 0.0,
#                 min(1.0, record.publications_count / 5.0),  # Normalized publications
#                 1.0 if record.work_experience_relevant else 0.0
#             ]
#             features.append(record_features)
        
#         # Prepare student vector
#         student_vector = [
#             student_profile.gpa / 4.0,
#             (student_profile.ielts_score or 0) / 9.0,
#             min(1.0, student_profile.experience_years / 10.0),
#             1.0 if student_profile.research_experience else 0.0,
#             min(1.0, student_profile.publications_count / 5.0),
#             1.0 if student_profile.work_experience_relevant else 0.0
#         ]
        
#         # Calculate weighted cosine similarity
#         if len(features) > 1:
#             features_array = np.array(features)
#             student_array = np.array(student_vector).reshape(1, -1)
            
#             # Apply feature weights
#             weights = np.array(list(feature_weights.values()))
#             features_weighted = features_array * weights
#             student_weighted = student_array * weights
            
#             # Calculate similarity
#             similarities = cosine_similarity(student_weighted, features_weighted)[0]
#             avg_similarity = np.mean(similarities)
#             return float(avg_similarity)
        
#         return 0.5
    
#     def calculate_final_score(self, eligibility_score: float, similarity_score: float) -> float:
#         """Combine scores with weights"""
#         # Weighted combination
#         final_score = (eligibility_score * 0.6) + (similarity_score * 0.4)
#         return min(1.0, final_score)
    
#     def generate_reasons(self, university: models.University, 
#                         eligibility_score: float, 
#                         similarity_score: float,
#                         student_profile: schemas.StudentProfile) -> List[str]:
#         """Generate human-readable reasons for recommendation"""
#         reasons = []
        
#         # GPA reason
#         if student_profile.gpa >= university.min_gpa + 0.5:
#             reasons.append(f"Excellent GPA ({student_profile.gpa}) exceeds requirement ({university.min_gpa})")
#         elif student_profile.gpa >= university.min_gpa:
#             reasons.append(f"Meets GPA requirement ({student_profile.gpa} ≥ {university.min_gpa})")
        
#         # IELTS reason
#         if student_profile.ielts_score and university.min_ielts:
#             if student_profile.ielts_score >= university.min_ielts + 1.0:
#                 reasons.append(f"Strong IELTS score ({student_profile.ielts_score})")
#             elif student_profile.ielts_score >= university.min_ielts:
#                 reasons.append(f"Meets IELTS requirement ({student_profile.ielts_score} ≥ {university.min_ielts})")
        
#         # Experience reason
#         if student_profile.experience_years >= university.min_experience_years + 2:
#             reasons.append(f"Significant experience ({student_profile.experience_years} years)")
        
#         # Research/publications reason
#         if student_profile.research_experience and university.program_level in ["MASTERS", "PHD"]:
#             reasons.append("Research experience relevant for program")
        
#         if student_profile.publications_count > 0 and university.program_level in ["PHD"]:
#             reasons.append(f"Publications ({student_profile.publications_count}) strengthen application")
        
#         # Budget reason
#         if student_profile.budget_usd and student_profile.budget_usd >= university.tuition_fee_usd:
#             reasons.append("Within budget range")
        
#         # Similarity reason
#         if similarity_score > 0.8:
#             reasons.append("Strong match with previous successful applicants")
#         elif similarity_score > 0.6:
#             reasons.append("Good match with admission history")
        
#         # University ranking reason
#         if university.world_ranking and university.world_ranking <= 100:
#             reasons.append(f"Top {university.world_ranking} university worldwide")
#         elif university.world_ranking and university.world_ranking <= 500:
#             reasons.append(f"Ranked in top 500 universities")
        
#         # Add default reason if none
#         if not reasons:
#             reasons.append("Good overall match based on your profile")
        
#         return reasons[:3]  # Return top 3 reasons
    
#     def get_recommendations(self, student_profile: schemas.StudentProfile, top_k: int = 5) -> List[Dict[str, Any]]:
#         """Main recommendation function"""
#         start_time = time.time()
        
#         # Step 1: Get eligible universities
#         eligible_universities = self.get_eligible_universities(student_profile)
        
#         if not eligible_universities:
#             return {
#                 "recommendations": [],
#                 "total_considered": 0,
#                 "message": "No universities match your criteria"
#             }
        
#         recommendations = []
        
#         # Step 2: Calculate scores for each university
#         for university in eligible_universities:
#             # Calculate scores
#             eligibility_score = self.calculate_eligibility_score(university, student_profile)
#             similarity_score = self.calculate_similarity_score(university, student_profile)
#             final_score = self.calculate_final_score(eligibility_score, similarity_score)
            
#             # Generate reasons
#             reasons = self.generate_reasons(university, eligibility_score, similarity_score, student_profile)
            
#             recommendations.append({
#                 "university": university,
#                 "match_score": eligibility_score,
#                 "eligibility_score": eligibility_score,
#                 "similarity_score": similarity_score,
#                 "final_score": final_score,
#                 "reasons": reasons
#             })
        
#         # Step 3: Sort by final score
#         recommendations.sort(key=lambda x: x["final_score"], reverse=True)
        
#         # Step 4: Take top K
#         top_recommendations = recommendations[:top_k]
        
#         processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
#         return {
#             "recommendations": top_recommendations,
#             "total_considered": len(eligible_universities),
#             "algorithm_version": "v2.0_hybrid",
#             "processing_time_ms": processing_time
#         }




# app/algorithms.py - UPDATED VERSION
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from . import models, schemas
import time

class HybridRecommender:
    def __init__(self, db: Session):
        self.db = db
        self.scaler = MinMaxScaler()
    
    def get_eligible_universities(self, student_profile: schemas.StudentProfile, flexible: bool = True) -> List[models.University]:
        """
        Get eligible universities with flexible filtering
        If flexible=True, it will relax some filters to get more results
        """
        query = self.db.query(models.University)
        
        # ALWAYS filter by program level (most important)
        query = query.filter(models.University.program_level == student_profile.desired_program)
        
        # Filter by field of study - make flexible
        if flexible and student_profile.field_of_study:
            # Try to match related fields too
            field = student_profile.field_of_study.lower()
            related_fields = self._get_related_fields(field)
            
            # Build OR condition for related fields
            conditions = []
            for related_field in related_fields:
                conditions.append(models.University.fields_offered.any(related_field))
            
            if conditions:
                query = query.filter(or_(*conditions))
            else:
                query = query.filter(models.University.fields_offered.any(student_profile.field_of_study))
        elif student_profile.field_of_study:
            # Strict filtering
            query = query.filter(models.University.fields_offered.any(student_profile.field_of_study))
        
        # Filter by GPA (can be flexible)
        if flexible and student_profile.gpa < 3.0:
            # If GPA is low, relax the requirement a bit
            query = query.filter(models.University.min_gpa <= student_profile.gpa + 0.3)
        else:
            query = query.filter(models.University.min_gpa <= student_profile.gpa)
        
        # Filter by IELTS if provided
        if student_profile.ielts_score:
            if flexible and student_profile.ielts_score < 6.5:
                # If IELTS is low, relax requirement
                query = query.filter(models.University.min_ielts <= student_profile.ielts_score + 0.5)
            else:
                query = query.filter(models.University.min_ielts <= student_profile.ielts_score)
        
        # Filter by experience (usually not strict)
        query = query.filter(models.University.min_experience_years <= student_profile.experience_years)
        
        # Filter by budget if provided
        if student_profile.budget_usd:
            if flexible:
                # Allow universities up to 20% over budget
                query = query.filter(models.University.tuition_fee_usd <= student_profile.budget_usd * 1.2)
            else:
                query = query.filter(models.University.tuition_fee_usd <= student_profile.budget_usd)
        
        # Filter by preferred countries if provided
        if student_profile.preferred_countries:
            if flexible and len(student_profile.preferred_countries) < 3:
                # If few countries selected, also include top-ranked universities from other countries
                query = query.filter(
                    or_(
                        models.University.country.in_(student_profile.preferred_countries),
                        models.University.world_ranking <= 100  # Top 100 worldwide
                    )
                )
            else:
                query = query.filter(models.University.country.in_(student_profile.preferred_countries))
        
        return query.all()
    
    def _get_related_fields(self, field: str) -> List[str]:
        """Get related fields for flexible matching"""
        field_lower = field.lower()
        
        # Define field mappings
        field_groups = {
            'computer science': ['Computer Science', 'Software Engineering', 'Information Technology', 
                               'Data Science', 'Artificial Intelligence', 'Machine Learning'],
            'business administration': ['Business Administration', 'Management', 'Finance', 
                                      'Marketing', 'Entrepreneurship', 'MBA'],
            'engineering': ['Engineering', 'Mechanical Engineering', 'Electrical Engineering',
                          'Civil Engineering', 'Chemical Engineering', 'Aerospace Engineering'],
            'data science': ['Data Science', 'Computer Science', 'Statistics', 
                           'Machine Learning', 'Artificial Intelligence'],
            'medicine': ['Medicine', 'Biomedical Sciences', 'Public Health', 
                        'Pharmacy', 'Nursing', 'Dentistry'],
            'psychology': ['Psychology', 'Neuroscience', 'Cognitive Science', 
                          'Counseling', 'Clinical Psychology'],
        }
        
        # Find matching group
        for key, related in field_groups.items():
            if key in field_lower or field_lower in key:
                return related
        
        # If no group found, return the original field
        return [field.title()]
    
    def get_potential_universities(self, student_profile: schemas.StudentProfile) -> List[models.University]:
        """
        Get universities that match at least some criteria (for backup)
        """
        query = self.db.query(models.University)
        
        # Always match program level
        query = query.filter(models.University.program_level == student_profile.desired_program)
        
        # Get universities (limit to reasonable number)
        universities = query.order_by(
            models.University.world_ranking.asc().nulls_last(),
            models.University.min_gpa.asc()
        ).limit(20).all()
        
        return universities
    
    def calculate_eligibility_score(self, university: models.University, student_profile: schemas.StudentProfile) -> float:
        """Calculate how well student meets university requirements"""
        score = 0.0
        total_weight = 0
        
        # 1. GPA score (30% weight)
        if university.min_gpa <= student_profile.gpa:
            gpa_score = min(1.0, student_profile.gpa / 4.0)
            score += gpa_score * 0.3
            total_weight += 0.3
        else:
            # Partial score even if below requirement
            gpa_ratio = student_profile.gpa / university.min_gpa
            if gpa_ratio >= 0.8:  # Close to requirement
                score += gpa_ratio * 0.15
                total_weight += 0.15
        
        # 2. IELTS score (15% weight)
        if student_profile.ielts_score and university.min_ielts:
            if student_profile.ielts_score >= university.min_ielts:
                ielts_score = min(1.0, student_profile.ielts_score / 9.0)
                score += ielts_score * 0.15
                total_weight += 0.15
            else:
                # Partial score
                ielts_ratio = student_profile.ielts_score / university.min_ielts
                if ielts_ratio >= 0.9:
                    score += ielts_ratio * 0.1
                    total_weight += 0.1
        
        # 3. Experience score (10% weight)
        exp_ratio = min(1.0, student_profile.experience_years / max(university.min_experience_years, 1))
        score += exp_ratio * 0.1
        total_weight += 0.1
        
        # 4. Field match score (20% weight)
        field_match = 0.0
        if student_profile.field_of_study in university.fields_offered:
            field_match = 1.0
        else:
            # Check for related fields
            for field in university.fields_offered:
                if any(related.lower() in field.lower() for related in 
                      self._get_related_fields(student_profile.field_of_study)):
                    field_match = 0.7
                    break
        
        score += field_match * 0.2
        total_weight += 0.2
        
        # 5. Country preference (10% weight)
        country_score = 0.0
        if student_profile.preferred_countries:
            if university.country in student_profile.preferred_countries:
                country_score = 1.0
            elif university.world_ranking and university.world_ranking <= 100:
                country_score = 0.5  # Top universities get partial score
        
        score += country_score * 0.1
        total_weight += 0.1
        
        # 6. Budget match (5% weight)
        budget_score = 0.0
        if student_profile.budget_usd:
            if university.tuition_fee_usd <= student_profile.budget_usd:
                budget_score = 1.0
            elif university.tuition_fee_usd <= student_profile.budget_usd * 1.2:
                budget_score = 0.5
        
        score += budget_score * 0.05
        total_weight += 0.05
        
        # 7. Additional qualifications (10% weight)
        additional_score = 0.0
        
        # Research experience
        if student_profile.research_experience and university.program_level in ["MASTERS", "PHD", "RESEARCH_MASTERS"]:
            additional_score += 0.05
        
        # Publications
        if student_profile.publications_count > 0:
            pub_bonus = min(0.03, student_profile.publications_count * 0.01)
            additional_score += pub_bonus
        
        # Relevant work experience
        if student_profile.work_experience_relevant and university.program_level in ["MBA", "EXECUTIVE_EDUCATION", "MASTERS"]:
            additional_score += 0.02
        
        # Leadership experience
        if student_profile.leadership_experience:
            additional_score += 0.02
        
        score += additional_score * 0.1
        total_weight += 0.1
        
        # Normalize score
        if total_weight > 0:
            score = score / total_weight
        
        return min(1.0, score)
    
    def calculate_similarity_score(self, university: models.University, student_profile: schemas.StudentProfile) -> float:
        """Calculate similarity based on historical admissions"""
        # Get historical admissions data for this university
        history_query = self.db.query(models.StudentAdmissionHistory).filter(
            models.StudentAdmissionHistory.university_applied_id == university.id,
            models.StudentAdmissionHistory.application_status == "ACCEPTED"
        ).limit(50)
        
        history = history_query.all()
        
        if not history:
            # If no history for this specific university, use general history
            history_query = self.db.query(models.StudentAdmissionHistory).filter(
                models.StudentAdmissionHistory.program_applied == university.program_level,
                models.StudentAdmissionHistory.application_status == "ACCEPTED"
            ).limit(50)
            history = history_query.all()
        
        if not history:
            return 0.5  # Default neutral score
        
        # Prepare feature vectors
        features = []
        
        for record in history:
            record_features = [
                record.gpa / 4.0,  # Normalized GPA
                (record.ielts_score or 6.5) / 9.0,  # Normalized IELTS (default 6.5 if missing)
                min(1.0, record.experience_years / 5.0),  # Normalized experience
                1.0 if record.research_experience else 0.0,
                min(1.0, record.publications_count / 3.0),  # Normalized publications
                1.0 if record.work_experience_relevant else 0.0,
                1.0 if record.leadership_experience else 0.0
            ]
            features.append(record_features)
        
        # Prepare student vector
        student_vector = [
            student_profile.gpa / 4.0,
            (student_profile.ielts_score or 6.5) / 9.0,
            min(1.0, student_profile.experience_years / 5.0),
            1.0 if student_profile.research_experience else 0.0,
            min(1.0, student_profile.publications_count / 3.0),
            1.0 if student_profile.work_experience_relevant else 0.0,
            1.0 if student_profile.leadership_experience else 0.0
        ]
        
        # Calculate cosine similarity
        features_array = np.array(features)
        student_array = np.array(student_vector).reshape(1, -1)
        
        try:
            similarities = cosine_similarity(student_array, features_array)[0]
            avg_similarity = np.mean(similarities)
            return float(max(0.3, min(0.95, avg_similarity)))  # Bound between 0.3 and 0.95
        except:
            return 0.5
    
    def calculate_final_score(self, eligibility_score: float, similarity_score: float, 
                            university: Optional[models.University] = None) -> float:
        """Combine scores with weights"""
        # Base weights
        eligibility_weight = 0.7
        similarity_weight = 0.3
        
        # Adjust weights based on university ranking
        if university and university.world_ranking:
            if university.world_ranking <= 50:
                # Top universities rely more on similarity (they're selective)
                eligibility_weight = 0.6
                similarity_weight = 0.4
            elif university.world_ranking >= 500:
                # Lower-ranked universities rely more on eligibility
                eligibility_weight = 0.8
                similarity_weight = 0.2
        
        final_score = (eligibility_score * eligibility_weight) + (similarity_score * similarity_weight)
        return min(1.0, final_score)
    
    def generate_reasons(self, university: models.University, 
                        eligibility_score: float, 
                        similarity_score: float,
                        student_profile: schemas.StudentProfile) -> List[str]:
        """Generate human-readable reasons for recommendation"""
        reasons = []
        
        # GPA reason
        if student_profile.gpa >= university.min_gpa + 0.3:
            reasons.append(f"Strong GPA ({student_profile.gpa})")
        elif student_profile.gpa >= university.min_gpa:
            reasons.append(f"Meets GPA requirement")
        
        # IELTS reason
        if student_profile.ielts_score and university.min_ielts:
            if student_profile.ielts_score >= university.min_ielts + 0.5:
                reasons.append(f"Good English proficiency")
            elif student_profile.ielts_score >= university.min_ielts:
                reasons.append(f"Meets language requirements")
        
        # Field match reason
        if student_profile.field_of_study in university.fields_offered:
            reasons.append(f"Exact match for {student_profile.field_of_study}")
        else:
            # Check for related fields
            for field in university.fields_offered:
                if any(related.lower() in field.lower() for related in 
                      self._get_related_fields(student_profile.field_of_study)):
                    reasons.append(f"Related program available")
                    break
        
        # Country reason
        if student_profile.preferred_countries and university.country in student_profile.preferred_countries:
            reasons.append(f"Located in preferred country")
        
        # Ranking reason
        if university.world_ranking:
            if university.world_ranking <= 50:
                reasons.append(f"Top {university.world_ranking} university globally")
            elif university.world_ranking <= 200:
                reasons.append(f"Ranked in top 200 worldwide")
        
        # Budget reason
        if student_profile.budget_usd:
            if university.tuition_fee_usd <= student_profile.budget_usd:
                reasons.append("Within your budget")
            elif university.tuition_fee_usd <= student_profile.budget_usd * 1.2:
                reasons.append("Slightly above budget but competitive")
        
        # Similarity reason
        if similarity_score > 0.75:
            reasons.append("Matches profile of previously accepted students")
        elif similarity_score > 0.6:
            reasons.append("Similar to successful applicants")
        
        # Add default reason if needed
        if len(reasons) < 2:
            if eligibility_score > 0.7:
                reasons.append("Strong overall match")
            else:
                reasons.append("Good potential match")
        
        return reasons[:3]
    
    def get_recommendations(self, student_profile: schemas.StudentProfile, top_k: int = 5) -> Dict[str, Any]:
        """Main recommendation function with fallback logic"""
        start_time = time.time()
        
        # Try flexible filtering first
        eligible_universities = self.get_eligible_universities(student_profile, flexible=True)
        
        # If still not enough, get potential universities
        if len(eligible_universities) < top_k:
            potential = self.get_potential_universities(student_profile)
            # Add unique universities
            existing_ids = {uni.id for uni in eligible_universities}
            for uni in potential:
                if uni.id not in existing_ids and len(eligible_universities) < top_k * 2:
                    eligible_universities.append(uni)
        
        if not eligible_universities:
            return {
                "recommendations": [],
                "total_considered": 0,
                "message": "No universities match your criteria",
                "algorithm_version": "v3.0_flexible"
            }
        
        recommendations = []
        
        # Calculate scores for each university
        for university in eligible_universities:
            eligibility_score = self.calculate_eligibility_score(university, student_profile)
            similarity_score = self.calculate_similarity_score(university, student_profile)
            final_score = self.calculate_final_score(eligibility_score, similarity_score, university)
            
            # Only include universities with decent scores
            if final_score >= 0.3:  # Minimum threshold
                reasons = self.generate_reasons(university, eligibility_score, similarity_score, student_profile)
                
                recommendations.append({
                    "university": university,
                    "match_score": final_score,
                    "eligibility_score": eligibility_score,
                    "similarity_score": similarity_score,
                    "final_score": final_score,
                    "reasons": reasons,
                    "ranking_tier": self._get_ranking_tier(university.world_ranking)
                })
        
        # Sort by final score
        recommendations.sort(key=lambda x: x["final_score"], reverse=True)
        
        # Always return top K, even if scores aren't perfect
        top_recommendations = recommendations[:top_k]
        
        # If we have fewer than requested, pad with lower-scored ones
        if len(top_recommendations) < top_k and len(recommendations) > len(top_recommendations):
            remaining = recommendations[len(top_recommendations):min(len(recommendations), top_k * 2)]
            top_recommendations.extend(remaining[:top_k - len(top_recommendations)])
        
        processing_time = (time.time() - start_time) * 1000
        
        return {
            "recommendations": top_recommendations,
            "total_considered": len(eligible_universities),
            "algorithm_version": "v3.0_flexible",
            "processing_time_ms": processing_time,
            "matched_criteria": self._get_matched_criteria_count(student_profile, top_recommendations)
        }
    
    def _get_ranking_tier(self, ranking: Optional[int]) -> str:
        """Categorize university by ranking tier"""
        if not ranking:
            return "Not Ranked"
        elif ranking <= 50:
            return "Elite"
        elif ranking <= 200:
            return "Top Tier"
        elif ranking <= 500:
            return "Competitive"
        else:
            return "Good"
    
    def _get_matched_criteria_count(self, student_profile: schemas.StudentProfile, recommendations: List[Dict]) -> Dict:
        """Count how many recommendations match various criteria"""
        matched = {
            "field_of_study": 0,
            "preferred_countries": 0,
            "budget": 0,
            "gpa_requirement": 0,
            "ielts_requirement": 0
        }
        
        for rec in recommendations:
            uni = rec["university"]
            
            # Check field match
            if student_profile.field_of_study in uni.fields_offered:
                matched["field_of_study"] += 1
            
            # Check country preference
            if student_profile.preferred_countries and uni.country in student_profile.preferred_countries:
                matched["preferred_countries"] += 1
            
            # Check budget
            if student_profile.budget_usd and uni.tuition_fee_usd <= student_profile.budget_usd:
                matched["budget"] += 1
            
            # Check GPA
            if student_profile.gpa >= uni.min_gpa:
                matched["gpa_requirement"] += 1
            
            # Check IELTS
            if student_profile.ielts_score and uni.min_ielts and student_profile.ielts_score >= uni.min_ielts:
                matched["ielts_requirement"] += 1
        
        return matched