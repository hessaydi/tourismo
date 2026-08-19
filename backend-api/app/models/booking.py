"""Booking model"""
from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import Column, DateTime, Date, ForeignKey, Integer, Numeric, String, Text

from app.database import Base


class Booking(Base):
    """Booking model"""

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_ref = Column(String(20), unique=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    package_id = Column(Integer, ForeignKey("packages.id"))
    travel_date = Column(Date)
    return_date = Column(Date)
    num_travelers = Column(Integer, default=1)
    total_price = Column(Numeric(12, 2))
    status = Column(String(20), default="pending")  # pending, confirmed, cancelled, completed
    payment_status = Column(String(20), default="unpaid")  # unpaid, partial, paid, refunded
    special_requests = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Booking {self.booking_ref}>"
