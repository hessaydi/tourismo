"""Booking schemas"""
from datetime import datetime, date
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel


class BookingBase(BaseModel):
    """Base booking schema"""

    client_id: int
    package_id: int
    travel_date: date
    return_date: date
    num_travelers: int = 1
    total_price: Decimal
    status: str = "pending"
    payment_status: str = "unpaid"
    special_requests: Optional[str] = None


class BookingCreate(BookingBase):
    """Booking creation schema"""

    pass


class BookingUpdate(BaseModel):
    """Booking update schema"""

    travel_date: Optional[date] = None
    return_date: Optional[date] = None
    num_travelers: Optional[int] = None
    total_price: Optional[Decimal] = None
    status: Optional[str] = None
    payment_status: Optional[str] = None
    special_requests: Optional[str] = None


class BookingResponse(BookingBase):
    """Booking response schema"""

    id: int
    booking_ref: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
