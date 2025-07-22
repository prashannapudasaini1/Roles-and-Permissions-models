from fastapi import HTTPException, Depends, status
from app.services.rbac_service import RBACService
from sqlalchemy.orm import Session
from app.models.session import SessionLocal
from app.services import user_service
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = user_service.get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user 
    
def require_permission(permission_name: str):


def check_permission(
current_user: User = Depends(get_current_user),
db: Session = Depends(get_db)
):
user_permissions = RBACService.get_user_permissions(db, current_user.id)
 if permission_name not in user_permissions:
 raise HTTPException(
 status_code=status.HTTP_403_FORBIDDEN,
 detail=f"Permission '{permission_name}' required"
 )
 return current_user
return check_permission
