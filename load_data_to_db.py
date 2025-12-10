# load_data_to_db.py
import csv
import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import SessionLocal, engine
from app import models
from typing import List, Dict, Any
import json

def safe_int(value):
    """Safely convert to int, handling float strings"""
    if not value or str(value).strip() == '':
        return None
    try:
        # First try to convert to float, then to int
        return int(float(value))
    except (ValueError, TypeError):
        return None

def safe_float(value):
    """Safely convert to float"""
    if not value or str(value).strip() == '':
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None

def safe_bool(value):
    """Safely convert to boolean"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ['true', 'yes', '1', 'y', 't']
    return bool(value)

def load_universities_from_csv(filepath: str):
    """Load universities from CSV to database"""
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(models.University).delete()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            universities = []
            row_count = 0
            
            for row in reader:
                row_count += 1
                print(f"Processing university {row_count}: {row.get('name', 'Unknown')}")
                
                # Convert fields_offered from comma-separated string to list
                fields_str = row.get('fields_offered', '')
                fields_list = [f.strip() for f in str(fields_str).split(',') if f.strip()]
                
                # Convert intake_seasons from comma-separated string to list
                intake_str = row.get('intake_seasons', '')
                intake_list = [s.strip() for s in str(intake_str).split(',') if s.strip()]
                
                # Prepare university data with safe conversions
                uni_data = {
                    'name': str(row.get('name', 'Unknown University')),
                    'country': str(row.get('country', 'Unknown')),
                    'world_ranking': safe_int(row.get('world_ranking')),
                    'acceptance_rate': safe_float(row.get('acceptance_rate')),
                    'website': str(row.get('website', '')) if row.get('website') else None,
                    'description': str(row.get('description', '')) if row.get('description') else None,
                    
                    'min_gpa': safe_float(row.get('min_gpa', 2.5)),
                    'min_ielts': safe_float(row.get('min_ielts')),
                    'min_toefl': safe_int(row.get('min_toefl')),
                    'min_gre': safe_int(row.get('min_gre')),
                    'min_gmat': safe_int(row.get('min_gmat')),
                    'min_experience_years': safe_int(row.get('min_experience_years', 0)),
                    
                    'program_name': str(row.get('program_name', 'General Program')),
                    'program_level': str(row.get('program_level', 'BACHELORS')),
                    'program_type': str(row.get('program_type', 'FULL_TIME')) if row.get('program_type') else None,
                    'program_duration_months': safe_int(row.get('program_duration_months')),
                    
                    'tuition_fee_usd': safe_float(row.get('tuition_fee_usd', 10000)),
                    'scholarship_available': safe_bool(row.get('scholarship_available', False)),
                    'avg_scholarship_percentage': safe_float(row.get('avg_scholarship_percentage')),
                    
                    'fields_offered': fields_list,
                    'requires_portfolio': safe_bool(row.get('requires_portfolio', False)),
                    'requires_research_proposal': safe_bool(row.get('requires_research_proposal', False)),
                    'requires_interview': safe_bool(row.get('requires_interview', False)),
                    
                    'application_deadline': str(row.get('application_deadline', '')) if row.get('application_deadline') else None,
                    'intake_seasons': intake_list,
                    
                    'graduation_rate': safe_float(row.get('graduation_rate')),
                    'employment_rate_6_months': safe_float(row.get('employment_rate_6_months')),
                    'avg_starting_salary_usd': safe_float(row.get('avg_starting_salary_usd')),
                }
                
                # Validate required fields
                if not uni_data['min_gpa']:
                    print(f"Warning: Missing min_gpa for {uni_data['name']}, using default 2.5")
                    uni_data['min_gpa'] = 2.5
                
                if not uni_data['tuition_fee_usd']:
                    print(f"Warning: Missing tuition_fee_usd for {uni_data['name']}, using default 10000")
                    uni_data['tuition_fee_usd'] = 10000
                
                university = models.University(**uni_data)
                universities.append(university)
            
            # Bulk insert
            db.add_all(universities)
            db.commit()
            
            print(f"✅ Successfully loaded {len(universities)} universities from {filepath}")
            
            # Show some statistics
            countries = set(uni.country for uni in universities)
            print(f"🌍 Countries represented: {len(countries)}")
            print(f"📊 GPA range: {min(uni.min_gpa for uni in universities):.1f} - {max(uni.min_gpa for uni in universities):.1f}")
            
            return [uni.id for uni in universities]
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error loading universities: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

def load_student_history_from_csv(filepath: str):
    """Load student admission history from CSV"""
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(models.StudentAdmissionHistory).delete()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            history_records = []
            row_count = 0
            
            for row in reader:
                row_count += 1
                if row_count % 50 == 0:
                    print(f"Processing student record {row_count}...")
                
                # Prepare history data with safe conversions
                hist_data = {
                    'student_id': safe_int(row.get('student_id', row_count + 1000)),
                    'gpa': safe_float(row.get('gpa', 3.0)),
                    'ielts_score': safe_float(row.get('ielts_score')),
                    'toefl_score': safe_int(row.get('toefl_score')),
                    'gre_score': safe_int(row.get('gre_score')),
                    'gmat_score': safe_int(row.get('gmat_score')),
                    'experience_years': safe_int(row.get('experience_years', 0)),
                    'previous_degree': str(row.get('previous_degree', '')) if row.get('previous_degree') else None,
                    'previous_university': str(row.get('previous_university', '')) if row.get('previous_university') else None,
                    'field_of_study': str(row.get('field_of_study', '')) if row.get('field_of_study') else None,
                    'research_experience': safe_bool(row.get('research_experience', False)),
                    'publications_count': safe_int(row.get('publications_count', 0)),
                    'work_experience_relevant': safe_bool(row.get('work_experience_relevant', False)),
                    'leadership_experience': safe_bool(row.get('leadership_experience', False)),
                    'university_applied_id': safe_int(row.get('university_applied_id', 1)),
                    'program_applied': str(row.get('program_applied', 'BACHELORS')),
                    'application_status': str(row.get('application_status', 'PENDING')),
                    'scholarship_received': safe_bool(row.get('scholarship_received', False)),
                    'scholarship_amount_usd': safe_float(row.get('scholarship_amount_usd')),
                    'application_date': str(row.get('application_date', '')) if row.get('application_date') else None,
                    'decision_date': str(row.get('decision_date', '')) if row.get('decision_date') else None,
                }
                
                # Validate required fields
                if not hist_data['gpa']:
                    print(f"Warning: Missing GPA for student {hist_data['student_id']}, using default 3.0")
                    hist_data['gpa'] = 3.0
                
                history_record = models.StudentAdmissionHistory(**hist_data)
                history_records.append(history_record)
            
            # Bulk insert in batches to avoid memory issues
            batch_size = 100
            for i in range(0, len(history_records), batch_size):
                batch = history_records[i:i + batch_size]
                db.add_all(batch)
                db.commit()
                print(f"✅ Committed batch {i//batch_size + 1}/{(len(history_records)-1)//batch_size + 1}")
            
            print(f"✅ Loaded {len(history_records)} student history records from {filepath}")
            
            # Show statistics
            accepted = sum(1 for r in history_records if r.application_status == 'ACCEPTED')
            rejected = sum(1 for r in history_records if r.application_status == 'REJECTED')
            
            print(f"📊 Acceptance rate: {accepted/len(history_records)*100:.1f}%")
            print(f"📊 Accepted: {accepted}, Rejected: {rejected}")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error loading student history: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()

def verify_data():
    """Verify that data was loaded correctly"""
    db = SessionLocal()
    
    try:
        # Count universities
        uni_count = db.query(models.University).count()
        print(f"\n🎯 Universities in database: {uni_count}")
        
        # Count student history
        hist_count = db.query(models.StudentAdmissionHistory).count()
        print(f"🎯 Student history records: {hist_count}")
        
        # Show sample data
        if uni_count > 0:
            sample_uni = db.query(models.University).first()
            print(f"\n📝 Sample University:")
            print(f"  Name: {sample_uni.name}")
            print(f"  Country: {sample_uni.country}")
            print(f"  World Ranking: {sample_uni.world_ranking}")
            print(f"  Min GPA: {sample_uni.min_gpa}")
            print(f"  IELTS: {sample_uni.min_ielts}")
            print(f"  Tuition: ${sample_uni.tuition_fee_usd:,.2f}")
            print(f"  Fields: {sample_uni.fields_offered[:3]}")
        
        if hist_count > 0:
            sample_hist = db.query(models.StudentAdmissionHistory).first()
            print(f"\n📝 Sample Student History:")
            print(f"  Student ID: {sample_hist.student_id}")
            print(f"  GPA: {sample_hist.gpa}")
            print(f"  IELTS: {sample_hist.ielts_score}")
            print(f"  Experience: {sample_hist.experience_years} years")
            print(f"  Status: {sample_hist.application_status}")
            print(f"  University ID: {sample_hist.university_applied_id}")
        
        # Show some aggregated stats
        if uni_count > 0:
            avg_gpa = db.query(models.University).with_entities(func.avg(models.University.min_gpa)).scalar()
            avg_tuition = db.query(models.University).with_entities(func.avg(models.University.tuition_fee_usd)).scalar()
            print(f"\n📈 Average min GPA requirement: {avg_gpa:.2f}")
            print(f"📈 Average tuition fee: ${avg_tuition:,.2f}")
            
    finally:
        db.close()

def main():
    """Main function to load all data"""
    print("🚀 Starting data load process...")
    print("=" * 50)
    
    # Create tables if they don't exist
    print("📦 Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    
    # Load universities
    universities_file = "universities.csv"
    if os.path.exists(universities_file):
        print(f"\n📥 Loading universities from {universities_file}...")
        load_universities_from_csv(universities_file)
    else:
        print(f"⚠️  {universities_file} not found. Please generate it first.")
        return
    
    # Load student history
    history_file = "student_admission_history.csv"
    if os.path.exists(history_file):
        print(f"\n📥 Loading student history from {history_file}...")
        load_student_history_from_csv(history_file)
    else:
        print(f"⚠️  {history_file} not found. Please generate it first.")
        return
    
    # Verify data
    print("\n🔍 Verifying loaded data...")
    print("=" * 50)
    verify_data()
    
    print("\n" + "=" * 50)
    print("🎉 Data loading complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()