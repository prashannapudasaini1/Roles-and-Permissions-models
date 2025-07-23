from fastapi import Depends, HTTPException, status
from app.db.models.user import User
from sqlalchemy.orm import Session
from app.db.database import get_db


def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).first()  
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_permission(permission: str):
    def checker(user: User = Depends(get_current_user)):
        allowed_permissions = ["post:create", "post:read", "post:update", "post:delete"]
        if permission not in allowed_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission"
            )
        return True
    return checker

