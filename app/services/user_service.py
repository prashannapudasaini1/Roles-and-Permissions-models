from sqlalchemy.orm import Session
from app.db.models.users.user import User
from app.api.v1.schemas.user import UserCreate
from app.core.security import get_password_hash,verify_password
from jose import JWTError
from fastapi import HTTPException,status
from app.core import security
def create_user(db:Session,user_in:UserCreate):
    hashed_password=security.get_password_hash(user_in.password)
    user=User(email=user_in.email,hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db:Session,email:str,password:str):
    user=db.query(User).filter(User.email==email).first()
    if not user:
        return None
    if not security.verify_password(password,user.hashed_password):
        return None
    return user

def get_current_user(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        raise credentials_exception
    return user 