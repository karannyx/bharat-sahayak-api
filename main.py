from typing import List, Optional
from datetime import date
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

import models
from database import engine, get_db

# Create DB tables if they do not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bharat Sahayak API",
    version="1.0.0",
    description="API for Indian government scholarships and public services."
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class SchemeBase(BaseModel):
    name_en: str
    name_hi: Optional[str] = None
    benefit: Optional[str] = None
    process: Optional[str] = None
    status: Optional[str] = "Active"
    deadline: Optional[date] = None
    official_url: Optional[str] = None
    source_org: Optional[str] = None

class SchemeCreate(SchemeBase):
    pass

class SchemeUpdate(BaseModel):
    name_en: Optional[str] = None
    name_hi: Optional[str] = None
    benefit: Optional[str] = None
    process: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[date] = None
    official_url: Optional[str] = None
    source_org: Optional[str] = None

class SchemeResponse(SchemeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to Bharat Sahayak API", "status": "online"}

@app.get("/api/v1/schemes")
def get_schemes(db: Session = Depends(get_db)):
    schemes = db.query(models.Scheme).all()
    return {"status": "success", "total": len(schemes), "data": schemes}

@app.post("/api/v1/schemes", status_code=status.HTTP_201_CREATED)
def create_scheme(scheme: SchemeCreate, db: Session = Depends(get_db)):
    db_scheme = models.Scheme(**scheme.model_dump())
    db.add(db_scheme)
    db.commit()
    db.refresh(db_scheme)
    return {"status": "success", "data": db_scheme}

@app.put("/api/v1/schemes/{scheme_id}")
def update_scheme(scheme_id: int, scheme_in: SchemeUpdate, db: Session = Depends(get_db)):
    db_scheme = db.query(models.Scheme).filter(models.Scheme.id == scheme_id).first()
    if not db_scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    
    update_data = scheme_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_scheme, field, value)
        
    db.commit()
    db.refresh(db_scheme)
    return {"status": "success", "data": db_scheme}

@app.delete("/api/v1/schemes/{scheme_id}")
def delete_scheme(scheme_id: int, db: Session = Depends(get_db)):
    scheme = db.query(models.Scheme).filter(models.Scheme.id == scheme_id).first()
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scheme with ID {scheme_id} not found"
        )
    db.delete(scheme)
    db.commit()
    return {"status": "success", "message": f"Scheme {scheme_id} deleted successfully"}

@app.get("/api/v1/schemes/search")
def search_schemes(q: str = "", db: Session = Depends(get_db)):
    search_term = q.strip()
    if not search_term:
        results = db.query(models.Scheme).all()
        return {"status": "success", "total_results": len(results), "data": results}

    pattern = f"%{search_term}%"

    results = db.query(models.Scheme).filter(
        or_(
            func.coalesce(models.Scheme.name_en, "").ilike(pattern),
            func.coalesce(models.Scheme.name_hi, "").ilike(pattern),
            func.coalesce(models.Scheme.benefit, "").ilike(pattern),
            func.coalesce(models.Scheme.process, "").ilike(pattern),
            func.coalesce(models.Scheme.source_org, "").ilike(pattern),
        )
    ).all()

    return {"status": "success", "total_results": len(results), "data": results}