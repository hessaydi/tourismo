"""Destination schemas"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DestinationBase(BaseModel):
    """Base destination schema"""

    name: str
    country: str
    description: str
    image_url: Optional[str] = None
    is_featured: bool = False


class DestinationCreate(DestinationBase):
    """Destination creation schema"""

    pass


class DestinationUpdate(BaseModel):
    """Destination update schema"""

    name: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_featured: Optional[bool] = None


class DestinationResponse(DestinationBase):
    """Destination response schema"""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
