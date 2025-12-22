from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True)
    original_url = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    clicks = Column(Integer, default=0)