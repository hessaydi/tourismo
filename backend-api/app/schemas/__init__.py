"""Pydantic schemas"""
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from app.schemas.destination import DestinationCreate, DestinationUpdate, DestinationResponse
from app.schemas.package import PackageCreate, PackageUpdate, PackageResponse
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.schemas.booking import BookingCreate, BookingUpdate, BookingResponse
from app.schemas.guide import GuideCreate, GuideUpdate, GuideResponse
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationResponse

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "DestinationCreate",
    "DestinationUpdate",
    "DestinationResponse",
    "PackageCreate",
    "PackageUpdate",
    "PackageResponse",
    "ClientCreate",
    "ClientUpdate",
    "ClientResponse",
    "BookingCreate",
    "BookingUpdate",
    "BookingResponse",
    "GuideCreate",
    "GuideUpdate",
    "GuideResponse",
    "NotificationCreate",
    "NotificationUpdate",
    "NotificationResponse",
]
