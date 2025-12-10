# generate_data.py (UPDATED VERSION)
import csv
import random
from faker import Faker
import pandas as pd
import numpy as np

fake = Faker()

# Initialize for reproducibility
np.random.seed(42)
random.seed(42)
fake.seed_instance(42)

# Countries and programs
countries = ["United States", "United Kingdom", "Canada", "Australia", "Germany", 
             "France", "Netherlands", "Sweden", "Switzerland", "Singapore"]

program_levels = ["BACHELORS", "MASTERS", "PHD", "MBA", "RESEARCH_MASTERS"]
fields = ["Computer Science", "Business Administration", "Engineering", 
          "Data Science", "Medicine", "Law", "Psychology", "Biology", 
          "Physics", "Mathematics", "Economics", "Finance"]

# Generate universities data with proper types
def generate_universities(num=50):
    universities = []
    
    # Prestigious universities (INTEGER rankings)
    top_universities = [
        {"name": "Stanford University", "country": "United States", "min_gpa": 3.9, "ranking": 3},
        {"name": "Massachusetts Institute of Technology", "country": "United States", "min_gpa": 3.9, "ranking": 1},
        {"name": "Harvard University", "country": "United States", "min_gpa": 3.9, "ranking": 2},
        {"name": "University of Cambridge", "country": "United Kingdom", "min_gpa": 3.8, "ranking": 5},
        {"name": "University of Oxford", "country": "United Kingdom", "min_gpa": 3.8, "ranking": 4},
        {"name": "University of Toronto", "country": "Canada", "min_gpa": 3.6, "ranking": 18},
        {"name": "University of Melbourne", "country": "Australia", "min_gpa": 3.5, "ranking": 33},
        {"name": "ETH Zurich", "country": "Switzerland", "min_gpa": 3.7, "ranking": 11},
        {"name": "National University of Singapore", "country": "Singapore", "min_gpa": 3.6, "ranking": 19},
        {"name": "University of California, Berkeley", "country": "United States", "min_gpa": 3.8, "ranking": 8},
    ]
    
    for i, uni in enumerate(top_universities):
        program_fields = random.sample(fields, random.randint(2, 4))
        
        universities.append({
            "id": i + 1,
            "name": uni["name"],
            "country": uni["country"],
            "world_ranking": int(uni["ranking"]),  # INTEGER type
            "acceptance_rate": round(random.uniform(4, 15), 1),
            "website": f"https://www.{uni['name'].lower().replace(' ', '').replace(',', '').replace('.', '')}.edu",
            "description": f"A premier institution for {', '.join(program_fields)} education",
            
            "min_gpa": float(uni["min_gpa"]),
            "min_ielts": round(random.uniform(6.5, 7.5), 1),
            "min_toefl": random.choice([90, 95, 100, 105, None]),
            "min_gre": random.choice([310, 315, 320, None]),
            "min_gmat": random.choice([650, 680, 700, None]),
            "min_experience_years": int(random.choice([0, 0, 0, 1, 2])),
            
            "program_name": f"{random.choice(program_fields)} {random.choice(['Program', 'Studies', 'Course'])}",
            "program_level": random.choice(program_levels),
            "program_type": random.choice(["FULL_TIME", "PART_TIME", "HYBRID"]),
            "program_duration_months": int(random.choice([12, 18, 24, 36, 48])),
            
            "tuition_fee_usd": float(round(random.uniform(15000, 60000), 2)),
            "scholarship_available": random.choice([True, False]),
            "avg_scholarship_percentage": round(random.uniform(10, 50), 1) if random.random() > 0.3 else None,
            
            "fields_offered": ",".join(program_fields),
            "requires_portfolio": random.choice([True, False, False]),
            "requires_research_proposal": random.choice([True, False, False, False]),
            "requires_interview": random.choice([True, False]),
            
            "application_deadline": random.choice(["2024-12-15", "2024-11-30", "2025-01-15", "2025-02-28"]),
            "intake_seasons": ",".join(random.sample(["FALL", "SPRING", "SUMMER"], random.randint(1, 3))),
            
            "graduation_rate": round(random.uniform(75, 98), 1),
            "employment_rate_6_months": round(random.uniform(85, 99), 1),
            "avg_starting_salary_usd": float(round(random.uniform(50000, 120000), 2)),
        })
    
    # Generate remaining universities
    for i in range(len(top_universities), num):
        country = random.choice(countries)
        program_fields = random.sample(fields, random.randint(2, 5))
        
        # Random ranking or None
        ranking = None
        if random.random() > 0.2:
            ranking = int(random.randint(100, 800))
        
        universities.append({
            "id": i + 1,
            "name": f"{fake.city()} University",
            "country": country,
            "world_ranking": ranking,  # INTEGER or None
            "acceptance_rate": round(random.uniform(20, 70), 1),
            "website": f"https://www.{fake.domain_name()}",
            "description": f"Leading university in {country} specializing in {random.choice(program_fields)}",
            
            "min_gpa": round(random.uniform(2.5, 3.7), 1),
            "min_ielts": round(random.uniform(6.0, 7.5), 1),
            "min_toefl": random.choice([80, 85, 90, 95, None]),
            "min_gre": random.choice([300, 305, 310, None]),
            "min_gmat": random.choice([600, 620, 650, None]),
            "min_experience_years": int(random.choice([0, 0, 0, 1, 2, 3])),
            
            "program_name": f"{random.choice(program_fields)} {random.choice(program_levels)} Program",
            "program_level": random.choice(program_levels),
            "program_type": random.choice(["FULL_TIME", "PART_TIME", "ONLINE", "HYBRID"]),
            "program_duration_months": int(random.choice([12, 18, 24, 36])),
            
            "tuition_fee_usd": float(round(random.uniform(8000, 40000), 2)),
            "scholarship_available": random.choice([True, True, False]),
            "avg_scholarship_percentage": round(random.uniform(5, 70), 1) if random.random() > 0.4 else None,
            
            "fields_offered": ",".join(program_fields),
            "requires_portfolio": random.choice([True, False, False, False, False]),
            "requires_research_proposal": random.choice([True, False, False, False]),
            "requires_interview": random.choice([True, False, False]),
            
            "application_deadline": random.choice(["2024-12-01", "2025-01-15", "2025-03-01", "2025-05-01"]),
            "intake_seasons": ",".join(random.sample(["FALL", "SPRING"], random.randint(1, 2))),
            
            "graduation_rate": round(random.uniform(65, 95), 1),
            "employment_rate_6_months": round(random.uniform(70, 95), 1),
            "avg_starting_salary_usd": float(round(random.uniform(30000, 80000), 2)),
        })
    
    return universities

# Generate student admission history with proper types
def generate_student_history(num=200, max_university_id=50):
    history = []
    
    for i in range(num):
        gpa = round(random.uniform(2.8, 4.0), 2)
        ielts = round(random.uniform(6.0, 9.0), 1) if random.random() > 0.1 else None
        experience = random.randint(0, 8)
        
        # GPA influences acceptance
        acceptance_chance = min(0.95, 0.3 + (gpa - 2.8) * 0.2)
        if ielts and ielts >= 7.0:
            acceptance_chance += 0.15
        if experience >= 2:
            acceptance_chance += 0.1
            
        accepted = random.random() < acceptance_chance
        
        history.append({
            "id": i + 1,
            "student_id": int(1000 + i),
            "gpa": float(gpa),
            "ielts_score": float(ielts) if ielts else None,
            "toefl_score": int(random.randint(80, 115)) if random.random() > 0.7 else None,
            "gre_score": int(random.randint(290, 340)) if random.random() > 0.8 else None,
            "gmat_score": int(random.randint(550, 780)) if random.random() > 0.8 else None,
            "experience_years": int(experience),
            "previous_degree": random.choice(["BACHELORS", "MASTERS", "HIGH_SCHOOL"]),
            "previous_university": fake.company() + " University",
            "field_of_study": random.choice(fields),
            "research_experience": random.random() > 0.7,
            "publications_count": int(random.randint(0, 5)) if random.random() > 0.8 else 0,
            "work_experience_relevant": random.random() > 0.5,
            "leadership_experience": random.random() > 0.6,
            "university_applied_id": int(random.randint(1, max_university_id)),
            "program_applied": random.choice(program_levels),
            "application_status": "ACCEPTED" if accepted else "REJECTED",
            "scholarship_received": accepted and random.random() > 0.6,
            "scholarship_amount_usd": float(round(random.uniform(5000, 25000), 2)) if accepted and random.random() > 0.6 else None,
            "application_date": fake.date_between(start_date='-2y', end_date='today').isoformat(),
            "decision_date": fake.date_between(start_date='-1y', end_date='today').isoformat() if accepted else None,
        })
    
    return history

# Save to CSV with proper handling of None values
def save_to_csv(data, filename):
    if data:
        df = pd.DataFrame(data)
        
        # Replace NaN with empty strings for cleaner CSV
        df = df.fillna('')
        
        # Ensure proper ordering of columns for universities
        if 'id' in df.columns:
            # For universities
            column_order = [
                'id', 'name', 'country', 'world_ranking', 'acceptance_rate',
                'website', 'description', 'min_gpa', 'min_ielts', 'min_toefl',
                'min_gre', 'min_gmat', 'min_experience_years', 'program_name',
                'program_level', 'program_type', 'program_duration_months',
                'tuition_fee_usd', 'scholarship_available', 'avg_scholarship_percentage',
                'fields_offered', 'requires_portfolio', 'requires_research_proposal',
                'requires_interview', 'application_deadline', 'intake_seasons',
                'graduation_rate', 'employment_rate_6_months', 'avg_starting_salary_usd'
            ]
            # Only keep columns that exist
            column_order = [col for col in column_order if col in df.columns]
            df = df[column_order]
        
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"✅ Saved {len(data)} records to {filename}")
        
        # Show sample
        print(f"📊 Sample data (first row):")
        for key, value in df.iloc[0].to_dict().items():
            if value:  # Only show non-empty values
                print(f"  {key}: {value}")
        print()
        
        # Show data types summary
        print(f"📋 Data types summary:")
        print(f"  Total rows: {len(df)}")
        print(f"  Columns: {len(df.columns)}")
        
        # Count non-empty values for key fields
        if 'world_ranking' in df.columns:
            non_empty = df['world_ranking'].apply(lambda x: str(x).strip() != '').sum()
            print(f"  Universities with ranking: {non_empty}")
        
        if 'min_gpa' in df.columns:
            print(f"  GPA range: {df['min_gpa'].min():.1f} - {df['min_gpa'].max():.1f}")
        
        print()

# Generate and save data
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Generating University Recommendation System Data")
    print("=" * 60)
    
    print("\n📚 Generating university data (50 universities)...")
    universities = generate_universities(50)
    save_to_csv(universities, "universities.csv")
    
    print("\n👨‍🎓 Generating student admission history (200 records)...")
    student_history = generate_student_history(200, 50)
    save_to_csv(student_history, "student_admission_history.csv")
    
    print("=" * 60)
    print("🎉 Data generation complete!")
    print("=" * 60)
    
    # Show statistics
    print(f"\n📁 File Summary:")
    print(f"  universities.csv: {len(universities)} records")
    print(f"  student_admission_history.csv: {len(student_history)} records")
    
    # Calculate acceptance rate
    accepted = sum(1 for h in student_history if h.get('application_status') == 'ACCEPTED')
    acceptance_rate = accepted / len(student_history) * 100 if student_history else 0
    print(f"\n📈 Overall acceptance rate in history: {acceptance_rate:.1f}%")
    
    # Show university diversity
    countries = set(uni['country'] for uni in universities)
    print(f"\n🌍 Countries represented: {len(countries)}")
    print(f"  {', '.join(sorted(countries)[:10])}{'...' if len(countries) > 10 else ''}")
    
    print("\n✅ Ready to load data into database!")
    print("👉 Run: python load_data_to_db.py")
    print("=" * 60)