from pydantic import BaseModel
from datetime import date
from typing import Optional

class SchemeCreate(BaseModel):
    name_en: str
    name_hi: Optional[str] = None
    status: Optional[str] = "Active"
    benefit: Optional[str] = None
    process: Optional[str] = None
    deadline: Optional[date] = None
    official_url: str
    source_org: str
    last_verified_date: date

    class Config:
        orm_mode = True