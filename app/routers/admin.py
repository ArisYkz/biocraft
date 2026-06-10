from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.models import User, Inquiry
from app.schemas import UserOut, InquiryOut, InquiryUpdate
from app.auth import get_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=list[UserOut])
def list_users(
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin_user)],
    skip: int = 0,
    limit: int = 100,
):
    return db.query(User).offset(skip).limit(limit).all()


@router.patch("/users/{user_id}/role", response_model=UserOut)
def toggle_admin_role(
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin_user)],
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot change own role")

    user.is_admin = not user.is_admin
    db.commit()
    db.refresh(user)
    return user


@router.get("/inquiries", response_model=list[InquiryOut])
def list_inquiries(
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin_user)],
):
    return (
        db.query(Inquiry)
        .order_by(Inquiry.created_at.desc())
        .all()
    )


@router.patch("/inquiries/{inquiry_id}", response_model=InquiryOut)
def update_inquiry(
    inquiry_id: int,
    update: InquiryUpdate,
    db: Annotated[Session, Depends(get_db)],
    admin: Annotated[User, Depends(get_admin_user)],
):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    inquiry.status = update.status
    if update.admin_response:
        inquiry.admin_response = update.admin_response
    db.commit()
    db.refresh(inquiry)
    return inquiry
