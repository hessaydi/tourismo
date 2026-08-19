"""Destination management routes"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.destination import Destination
from app.models.user import User
from app.schemas.destination import DestinationCreate, DestinationResponse, DestinationUpdate
from app.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[DestinationResponse])
async def list_destinations(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """List all destinations"""
    destinations = db.query(Destination).offset(skip).limit(limit).all()
    return destinations


@router.get("/{destination_id}", response_model=DestinationResponse)
async def get_destination(destination_id: int, db: Session = Depends(get_db)):
    """Get destination by ID"""
    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found",
        )
    return destination


@router.post("/", response_model=DestinationResponse)
async def create_destination(
    destination_data: DestinationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new destination (admin/manager only)"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and managers can create destinations",
        )

    destination = Destination(**destination_data.dict())
    db.add(destination)
    db.commit()
    db.refresh(destination)
    return destination


@router.put("/{destination_id}", response_model=DestinationResponse)
async def update_destination(
    destination_id: int,
    destination_data: DestinationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a destination (admin/manager only)"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and managers can update destinations",
        )

    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found",
        )

    update_data = destination_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(destination, field, value)

    db.commit()
    db.refresh(destination)
    return destination


@router.delete("/{destination_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_destination(
    destination_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a destination (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete destinations",
        )

    destination = db.query(Destination).filter(Destination.id == destination_id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found",
        )

    db.delete(destination)
    db.commit()
