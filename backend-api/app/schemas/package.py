"""Package schemas"""
from datetime import datetime
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel


class PackageBase(BaseModel):
    """Base package schema"""

    title: str
    destination_id: int
    category: str
    description: str
    duration_days: int
    price_per_person: Decimal
    max_capacity: int
    status: str = "active"
    includes: Optional[str] = None
    image_url: Optional[str] = None


class PackageCreate(PackageBase):
    """Package creation schema"""

    pass


class PackageUpdate(BaseModel):
    """Package update schema"""

    title: Optional[str] = None
    destination_id: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    duration_days: Optional[int] = None
    price_per_person: Optional[Decimal] = None
    max_capacity: Optional[int] = None
    status: Optional[str] = None
    includes: Optional[str] = None
    image_url: Optional[str] = None


class PackageResponse(PackageBase):
    """Package response schema"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
