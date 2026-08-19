"""Client schemas"""
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    """Base client schema"""

    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    passport_number: Optional[str] = None
    nationality: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    """Client creation schema"""

    pass


class ClientUpdate(BaseModel):
    """Client update schema"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    passport_number: Optional[str] = None
    nationality: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    notes: Optional[str] = None


class ClientResponse(ClientBase):
    """Client response schema"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
