"""Guide model"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text

from app.database import Base


class Guide(Base):
    """Tour guide model"""

    __tablename__ = "guides"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(30))
    languages = Column(String(200))  # Comma-separated
    specialties = Column(String(200), nullable=True)
    bio = Column(Text, nullable=True)
    rating = Column(Numeric(3, 1), default=5.0)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Guide {self.name}>"
