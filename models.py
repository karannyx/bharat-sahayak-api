from sqlalchemy import Column, Integer, String, Text, Date
from database import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True)
    name_en = Column(String, index=True)
    name_hi = Column(String)
    status = Column(String) 
    benefit = Column(Text)
    process = Column(Text)
    deadline = Column(Date)
    official_url = Column(String)
    source_org = Column(String)
    last_verified_date = Column(Date)