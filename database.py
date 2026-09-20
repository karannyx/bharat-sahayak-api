import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Render ke environment variable se URL lega
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bharat_admin:1234@localhost:5432/bharat_sahayak")

# Render postgres:// deta hai, SQLAlchemy 2.0+ ko postgresql:// chahiye hota hai
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()