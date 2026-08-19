"""Guide schemas"""
from datetime import datetime
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, EmailStr


class GuideBase(BaseModel):
    """Base guide schema"""

    name: str
    email: EmailStr
    phone: str
    languages: str
    specialties: Optional[str] = None
    bio: Optional[str] = None
    rating: Decimal = Decimal("5.0")
    is_available: bool = True


class GuideCreate(GuideBase):
    """Guide creation schema"""

    pass


class GuideUpdate(BaseModel):
    """Guide update schema"""

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    languages: Optional[str] = None
    specialties: Optional[str] = None
    bio: Optional[str] = None
    rating: Optional[Decimal] = None
    is_available: Optional[bool] = None


class GuideResponse(GuideBase):
    """Guide response schema"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
