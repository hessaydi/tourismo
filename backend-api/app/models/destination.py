"""Destination model"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.database import Base


class Destination(Base):
    """Travel destination model"""

    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    country = Column(String(100))
    description = Column(Text)
    image_url = Column(String(500), nullable=True)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Destination {self.name}>"
