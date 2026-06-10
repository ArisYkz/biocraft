from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.models import User, Inquiry
from app.schemas import InquiryCreate, InquiryOut, ContactCreate
from app.auth import get_current_active_user

router = APIRouter(prefix="/inquiries", tags=["inquiries"])


@router.post("", response_model=InquiryOut, status_code=status.HTTP_201_CREATED)
def create_inquiry(
    inquiry_in: InquiryCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    inquiry = Inquiry(
        user_id=current_user.id,
        subject=inquiry_in.subject,
        message=inquiry_in.message,
    )
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry


@router.post("/contact", response_model=InquiryOut, status_code=status.HTTP_201_CREATED)
def contact_us(
    contact: ContactCreate,
    db: Annotated[Session, Depends(get_db)],
):
    inquiry = Inquiry(
        user_id=None,
        subject="Contact: " + contact.name,
        message="From: " + contact.email + "\n\n" + contact.message,
    )
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry


@router.get("/mine", response_model=list[InquiryOut])
def get_my_inquiries(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return (
        db.query(Inquiry)
        .filter(Inquiry.user_id == current_user.id)
        .order_by(Inquiry.created_at.desc())
        .all()
    )
