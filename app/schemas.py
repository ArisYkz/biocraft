from pydantic import BaseModel
from datetime import datetime


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InquiryCreate(BaseModel):
    subject: str
    message: str


class InquiryOut(BaseModel):
    id: int
    user_id: int | None = None
    subject: str
    message: str
    status: str
    admin_response: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InquiryUpdate(BaseModel):
    status: str
    admin_response: str = ""


class ContactCreate(BaseModel):
    name: str
    email: str
    message: str
