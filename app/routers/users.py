from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.models import User
from app.schemas import UserOut
from app.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
