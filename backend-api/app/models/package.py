"""Package model"""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text

from app.database import Base


class Package(Base):
    """Travel package model"""

    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    category = Column(String(50))  # adventure, cultural, relaxation, etc.
    description = Column(Text)
    duration_days = Column(Integer)
    price_per_person = Column(Numeric(10, 2))
    max_capacity = Column(Integer)
    status = Column(String(20), default="active")  # active, inactive, archived
    includes = Column(Text, nullable=True)  # Comma-separated list
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Package {self.title}>"
