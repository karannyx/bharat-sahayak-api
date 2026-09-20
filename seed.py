import models
from database import SessionLocal, engine
from datetime import date

# Ensure tables exist just in case
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Our list of 5 verified Central and MP state schemes
    schemes_data = [
        {
            "name_en": "Mukhyamantri Medhavi Vidyarthi Yojana (MMVY)",
            "name_hi": "मुख्यमंत्री मेधावी विद्यार्थी योजना",
            "status": "Active",
            "benefit": "Full tuition fee waiver for undergraduate courses in premier institutions",
            "process": "Apply online through the MP State Scholarship Portal",
            "deadline": date(2026, 11, 30),
            "official_url": "https://scholarshipportal.mp.nic.in",
            "source_org": "Government of Madhya Pradesh",
            "last_verified_date": date(2026, 9, 17)
        },
        {
            "name_en": "Gaon Ki Beti Yojana",
            "name_hi": "गाँव की बेटी योजना",
            "status": "Active",
            "benefit": "Financial assistance of Rs. 500 per month for 10 months to rural girls for higher education",
            "process": "Submit application through college principal/online portal",
            "deadline": date(2026, 12, 15),
            "official_url": "https://scholarshipportal.mp.nic.in",
            "source_org": "Higher Education Department, MP",
            "last_verified_date": date(2026, 9, 17)
        },
        {
            "name_en": "Mukhyamantri Seekho Kamao Yojana",
            "name_hi": "मुख्यमंत्री सीखो कमाओ योजना",
            "status": "Active",
            "benefit": "Stipend of Rs. 8,000 to 10,000 per month during skill training with guaranteed placement assistance",
            "process": "Register on MMSKY portal, select courses, and attend interviews",
            "deadline": date(2026, 10, 31),
            "official_url": "https://mmsky.mp.gov.in",
            "source_org": "Technical Education & Skill Development, MP",
            "last_verified_date": date(2026, 9, 17)
        },
        {
            "name_en": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
            "name_hi": "प्रधानमंत्री किसान सम्मान निधि",
            "status": "Active",
            "benefit": "Rs. 6,000 per year transferred directly to bank accounts in three equal installments",
            "process": "Register via PM KISAN portal or CSC centers with Aadhaar and bank details",
            "deadline": date(2027, 3, 31),
            "official_url": "https://pmkisan.gov.in",
            "source_org": "Ministry of Agriculture and Farmers Welfare",
            "last_verified_date": date(2026, 9, 17)
        },
        {
            "name_en": "National Means-cum-Merit Scholarship (NMMS)",
            "name_hi": "राष्ट्रीय साधन-सह-मेधा छात्रवृत्ति",
            "status": "Active",
            "benefit": "Rs. 12,000 per annum for students studying in class IX to XII",
            "process": "Apply via National Scholarship Portal after clearing the state-level selection test",
            "deadline": date(2026, 11, 15),
            "official_url": "https://scholarships.gov.in",
            "source_org": "Ministry of Education",
            "last_verified_date": date(2026, 9, 17)
        }
    ]
    
    print("Seeding database...")
    
    # Loop through our data and add it to the database session
    for data in schemes_data:
        scheme = models.Scheme(**data)
        db.add(scheme)
    
    # Commit the changes to permanently save them
    db.commit()
    db.close()
    
    print(f"Boom! Successfully seeded {len(schemes_data)} schemes into the database.")

if __name__ == "__main__":
    seed_data()