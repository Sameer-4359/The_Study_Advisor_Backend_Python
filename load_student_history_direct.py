# load_student_history_direct.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import SessionLocal, engine
from app import models
import random
from datetime import datetime, timedelta

def create_student_admission_history():
    """Create realistic student admission history data"""
    db = SessionLocal()
    
    try:
        # Clear existing student history
        print("🧹 Clearing existing student history...")
        db.query(models.StudentAdmissionHistory).delete()
        
        # Get all universities from database
        universities = db.query(models.University).all()
        if not universities:
            print("❌ No universities found in database!")
            return
        
        print(f"🎓 Found {len(universities)} universities")
        
        # Define realistic student profiles
        student_profiles = []
        
        # High-achieving students (top 20%)
        for i in range(40):  # 40 students
            gpa = round(random.uniform(3.7, 4.0), 2)
            ielts = round(random.uniform(7.5, 9.0), 1)
            experience = random.randint(1, 5)
            
            student_profiles.append({
                "gpa": gpa,
                "ielts_score": ielts,
                "experience_years": experience,
                "research_experience": random.random() > 0.6,
                "publications_count": random.randint(0, 3),
                "work_experience_relevant": True,
                "leadership_experience": random.random() > 0.7,
                "acceptance_chance": 0.85  # High chance of acceptance
            })
        
        # Average students (middle 60%)
        for i in range(120):  # 120 students
            gpa = round(random.uniform(3.0, 3.7), 2)
            ielts = round(random.uniform(6.5, 7.5), 1)
            experience = random.randint(0, 3)
            
            student_profiles.append({
                "gpa": gpa,
                "ielts_score": ielts,
                "experience_years": experience,
                "research_experience": random.random() > 0.3,
                "publications_count": random.randint(0, 1),
                "work_experience_relevant": random.random() > 0.5,
                "leadership_experience": random.random() > 0.4,
                "acceptance_chance": 0.55  # Moderate chance
            })
        
        # Lower-performing students (bottom 20%)
        for i in range(40):  # 40 students
            gpa = round(random.uniform(2.5, 3.0), 2)
            ielts = round(random.uniform(6.0, 6.5), 1)
            experience = random.randint(0, 1)
            
            student_profiles.append({
                "gpa": gpa,
                "ielts_score": ielts,
                "experience_years": experience,
                "research_experience": random.random() > 0.1,
                "publications_count": 0,
                "work_experience_relevant": random.random() > 0.2,
                "leadership_experience": random.random() > 0.2,
                "acceptance_chance": 0.25  # Low chance
            })
        
        # Fields of study
        fields = [
            "Computer Science", "Business Administration", "Engineering", 
            "Data Science", "Medicine", "Law", "Psychology", "Biology", 
            "Physics", "Mathematics", "Economics", "Finance"
        ]
        
        # Generate admission records
        history_records = []
        student_id_counter = 1001
        
        for student_idx, profile in enumerate(student_profiles):
            # Each student applies to 1-3 universities
            num_applications = random.randint(1, 3)
            applied_universities = random.sample(universities, min(num_applications, len(universities)))
            
            for university in applied_universities:
                # Adjust acceptance chance based on university requirements
                base_chance = profile["acceptance_chance"]
                
                # Check if meets minimum requirements
                if profile["gpa"] < university.min_gpa:
                    base_chance *= 0.3  # Reduce chance significantly
                
                if profile["ielts_score"] and university.min_ielts:
                    if profile["ielts_score"] < university.min_ielts:
                        base_chance *= 0.4
                
                if profile["experience_years"] < university.min_experience_years:
                    base_chance *= 0.8
                
                # Higher ranking universities are more selective
                if university.world_ranking and university.world_ranking <= 100:
                    base_chance *= 0.7  # Top 100 unis are more selective
                
                # Determine acceptance
                accepted = random.random() < base_chance
                
                # Create dates
                app_date = datetime.now() - timedelta(days=random.randint(30, 365))
                if accepted:
                    decision_date = app_date + timedelta(days=random.randint(30, 90))
                else:
                    decision_date = app_date + timedelta(days=random.randint(20, 60))
                
                # Determine scholarship (only for accepted students)
                scholarship_received = False
                scholarship_amount = None
                
                if accepted and university.scholarship_available:
                    if random.random() > 0.5:  # 50% chance of scholarship
                        scholarship_received = True
                        if university.avg_scholarship_percentage:
                            scholarship_percent = random.uniform(
                                0.5, 1.5
                            ) * university.avg_scholarship_percentage
                            scholarship_amount = (university.tuition_fee_usd * scholarship_percent / 100)
                
                # Create history record
                history_record = models.StudentAdmissionHistory(
                    student_id=student_id_counter,
                    gpa=profile["gpa"],
                    ielts_score=profile["ielts_score"],
                    toefl_score=random.randint(95, 115) if random.random() > 0.7 else None,
                    gre_score=random.randint(310, 340) if random.random() > 0.6 else None,
                    gmat_score=random.randint(650, 750) if random.random() > 0.6 else None,
                    experience_years=profile["experience_years"],
                    previous_degree=random.choice(["BACHELORS", "MASTERS", "HIGH_SCHOOL"]),
                    previous_university=f"University {random.choice(['A', 'B', 'C', 'D'])}",
                    field_of_study=random.choice(fields),
                    research_experience=profile["research_experience"],
                    publications_count=profile["publications_count"],
                    work_experience_relevant=profile["work_experience_relevant"],
                    leadership_experience=profile["leadership_experience"],
                    university_applied_id=university.id,
                    program_applied=university.program_level,
                    application_status="ACCEPTED" if accepted else "REJECTED",
                    scholarship_received=scholarship_received,
                    scholarship_amount_usd=round(scholarship_amount, 2) if scholarship_amount else None,
                    application_date=app_date,
                    decision_date=decision_date if accepted else None,
                )
                
                history_records.append(history_record)
            
            student_id_counter += 1
            
            # Show progress
            if (student_idx + 1) % 20 == 0:
                print(f"📝 Generated history for {student_idx + 1} students...")
        
        # Insert in batches
        print(f"\n💾 Inserting {len(history_records)} history records...")
        batch_size = 100
        
        for i in range(0, len(history_records), batch_size):
            batch = history_records[i:i + batch_size]
            db.add_all(batch)
            db.commit()
            print(f"✅ Committed batch {i//batch_size + 1}/{(len(history_records)-1)//batch_size + 1}")
        
        print(f"\n🎉 Successfully created {len(history_records)} student admission records!")
        
        # Calculate statistics
        total_accepted = sum(1 for r in history_records if r.application_status == "ACCEPTED")
        total_rejected = len(history_records) - total_accepted
        acceptance_rate = (total_accepted / len(history_records)) * 100
        
        print(f"\n📊 Statistics:")
        print(f"  Total applications: {len(history_records)}")
        print(f"  Accepted: {total_accepted}")
        print(f"  Rejected: {total_rejected}")
        print(f"  Acceptance rate: {acceptance_rate:.1f}%")
        
        # Scholarship statistics
        scholarship_given = sum(1 for r in history_records if r.scholarship_received)
        if scholarship_given > 0:
            print(f"  Scholarships awarded: {scholarship_given}")
            avg_scholarship = sum(r.scholarship_amount_usd or 0 for r in history_records if r.scholarship_received) / scholarship_given
            print(f"  Average scholarship amount: ${avg_scholarship:,.2f}")
        
        return len(history_records)
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        db.close()

def verify_data():
    """Verify the loaded data"""
    db = SessionLocal()
    
    try:
        # Count records
        uni_count = db.query(models.University).count()
        hist_count = db.query(models.StudentAdmissionHistory).count()
        
        print(f"\n🔍 Verification Results:")
        print(f"  Universities in database: {uni_count}")
        print(f"  Student history records: {hist_count}")
        
        if hist_count > 0:
            # Show some samples
            print(f"\n📋 Sample Accepted Applications:")
            accepted_samples = db.query(models.StudentAdmissionHistory)\
                .filter(models.StudentAdmissionHistory.application_status == "ACCEPTED")\
                .limit(3).all()
            
            for sample in accepted_samples:
                uni = db.query(models.University).filter(models.University.id == sample.university_applied_id).first()
                print(f"  Student {sample.student_id}: GPA {sample.gpa}, IELTS {sample.ielts_score}")
                print(f"    → {uni.name if uni else 'Unknown'} ({sample.program_applied})")
                if sample.scholarship_received:
                    print(f"    💰 Scholarship: ${sample.scholarship_amount_usd:,.2f}")
                print()
            
            # Show some rejected
            print(f"📋 Sample Rejected Applications:")
            rejected_samples = db.query(models.StudentAdmissionHistory)\
                .filter(models.StudentAdmissionHistory.application_status == "REJECTED")\
                .limit(2).all()
            
            for sample in rejected_samples:
                uni = db.query(models.University).filter(models.University.id == sample.university_applied_id).first()
                print(f"  Student {sample.student_id}: GPA {sample.gpa}, IELTS {sample.ielts_score}")
                print(f"    → {uni.name if uni else 'Unknown'} ({sample.program_applied})")
                print()
            
            # Calculate acceptance rates by GPA range
            print(f"📈 Acceptance by GPA Range:")
            gpa_ranges = [(2.5, 3.0), (3.0, 3.5), (3.5, 4.0)]
            
            for gpa_min, gpa_max in gpa_ranges:
                total = db.query(models.StudentAdmissionHistory)\
                    .filter(models.StudentAdmissionHistory.gpa.between(gpa_min, gpa_max))\
                    .count()
                
                if total > 0:
                    accepted = db.query(models.StudentAdmissionHistory)\
                        .filter(
                            models.StudentAdmissionHistory.gpa.between(gpa_min, gpa_max),
                            models.StudentAdmissionHistory.application_status == "ACCEPTED"
                        )\
                        .count()
                    
                    rate = (accepted / total) * 100
                    print(f"  GPA {gpa_min}-{gpa_max}: {rate:.1f}% ({accepted}/{total})")
        
    finally:
        db.close()

def main():
    print("=" * 60)
    print("🎓 STUDENT ADMISSION HISTORY DATA GENERATOR")
    print("=" * 60)
    
    # Create tables if needed
    print("\n📦 Checking database tables...")
    models.Base.metadata.create_all(bind=engine)
    
    # Create student history
    print("\n👨‍🎓 Generating realistic student admission history...")
    print("-" * 60)
    
    records_created = create_student_admission_history()
    
    if records_created:
        print("\n" + "=" * 60)
        print("✅ DATA GENERATION COMPLETE")
        print("=" * 60)
        
        # Verify the data
        verify_data()
        
        print("\n🎯 Ready for recommendations!")
        print("👉 Start your server: python run.py")
        print("👉 Test with POST /recommendations")
    else:
        print("\n❌ Data generation failed!")

if __name__ == "__main__":
    main()