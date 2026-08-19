"""Notification schemas"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NotificationBase(BaseModel):
    """Base notification schema"""

    user_id: int
    title: str
    message: Optional[str] = None
    link: Optional[str] = None
    is_read: bool = False


class NotificationCreate(BaseModel):
    """Notification creation schema"""

    title: str
    message: Optional[str] = None
    link: Optional[str] = None


class NotificationUpdate(BaseModel):
    """Notification update schema"""

    is_read: Optional[bool] = None
    message: Optional[str] = None
    link: Optional[str] = None


class NotificationResponse(NotificationBase):
    """Notification response schema"""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
