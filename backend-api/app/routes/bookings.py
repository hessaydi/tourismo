"""Booking management routes"""
import random
import string
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.booking import Booking
from app.models.package import Package
from app.models.client import Client
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from app.security import get_current_user

router = APIRouter()

BOOKING_REF_PREFIX = "BK"
BOOKING_REF_DIGITS = 8


def generate_booking_ref() -> str:
    """Generate a unique booking reference"""
    random_digits = "".join(random.choices(string.digits, k=BOOKING_REF_DIGITS))
    return f"{BOOKING_REF_PREFIX}{random_digits}"


@router.get("/", response_model=List[BookingResponse])
async def list_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
):
    """List all bookings"""
    query = db.query(Booking)
    if status_filter:
        query = query.filter(Booking.status == status_filter)
    bookings = query.offset(skip).limit(limit).all()
    return bookings


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get booking by ID"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    return booking


@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new booking with auto price calculation"""
    # Verify client exists
    client = db.query(Client).filter(Client.id == booking_data.client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    # Verify package exists
    package = db.query(Package).filter(Package.id == booking_data.package_id).first()
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found",
        )

    # Auto-calculate total price
    total_price = package.price_per_person * booking_data.num_travelers

    # Generate booking reference
    booking_ref = generate_booking_ref()

    booking = Booking(
        booking_ref=booking_ref,
        client_id=booking_data.client_id,
        package_id=booking_data.package_id,
        travel_date=booking_data.travel_date,
        return_date=booking_data.return_date,
        num_travelers=booking_data.num_travelers,
        total_price=total_price,
        status=booking_data.status,
        payment_status=booking_data.payment_status,
        special_requests=booking_data.special_requests,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    update_data = booking_data.dict(exclude_unset=True)

    # Recalculate price if num_travelers changes
    if "num_travelers" in update_data and update_data["num_travelers"] != booking.num_travelers:
        package = db.query(Package).filter(Package.id == booking.package_id).first()
        if package:
            update_data["total_price"] = package.price_per_person * update_data["num_travelers"]

    for field, value in update_data.items():
        setattr(booking, field, value)

    db.commit()
    db.refresh(booking)
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a booking (admin/manager only)"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and managers can delete bookings",
        )

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    db.delete(booking)
    db.commit()
