from fastapi import HTTPException, Depends, status
from app.services.rbac_service import RBACService
def require_permission(permission_name: str):
"""Dependency to check if current user has required permission"""
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
