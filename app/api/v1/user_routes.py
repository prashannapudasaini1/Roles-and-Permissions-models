from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.schemas.user import UserCreate, UserRead, Token
from app.services import user_service
from app.deps import get_db
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core import security
from app.core.config import Setting
from app.deps import get_current_user
router = APIRouter()

@router.post("/users/", response_model=UserRead)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, user_in)
    return user
@router.post("/login/", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = security.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=Setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=UserRead)
def read_users_me(current_user = Depends(get_current_user)):
    return current_user 