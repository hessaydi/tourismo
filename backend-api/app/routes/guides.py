"""Guide management routes"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.guide import Guide
from app.models.user import User
from app.schemas.guide import GuideCreate, GuideResponse, GuideUpdate
from app.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[GuideResponse])
async def list_guides(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    available_only: bool = False,
):
    """List all guides"""
    query = db.query(Guide)
    if available_only:
        query = query.filter(Guide.is_available == True)
    guides = query.offset(skip).limit(limit).all()
    return guides


@router.get("/{guide_id}", response_model=GuideResponse)
async def get_guide(guide_id: int, db: Session = Depends(get_db)):
    """Get guide by ID"""
    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guide not found",
        )
    return guide


@router.post("/", response_model=GuideResponse)
async def create_guide(
    guide_data: GuideCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new guide (admin/manager only)"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and managers can create guides",
        )

    # Check if email already exists
    existing_guide = db.query(Guide).filter(Guide.email == guide_data.email).first()
    if existing_guide:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    guide = Guide(**guide_data.dict())
    db.add(guide)
    db.commit()
    db.refresh(guide)
    return guide


@router.put("/{guide_id}", response_model=GuideResponse)
async def update_guide(
    guide_id: int,
    guide_data: GuideUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a guide (admin/manager only)"""
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins and managers can update guides",
        )

    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guide not found",
        )

    update_data = guide_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(guide, field, value)

    db.commit()
    db.refresh(guide)
    return guide


@router.delete("/{guide_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guide(
    guide_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a guide (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete guides",
        )

    guide = db.query(Guide).filter(Guide.id == guide_id).first()
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Guide not found",
        )

    db.delete(guide)
    db.commit()
