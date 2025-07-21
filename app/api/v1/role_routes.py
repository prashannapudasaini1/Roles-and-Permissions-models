from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.deps import get_db, get_current_user, require_permission
from app.services.rbac_service import RBACService
from app.api.v1.schemas.role import (
RoleCreate, RoleRead, PermissionCreate, PermissionRead,
AssignPermissionRequest
)
from app.db.models.users.user import User
router = APIRouter(prefix="/roles", tags=["roles"])
permission_router = APIRouter(prefix="/permissions", tags=["permissions"])


# Role endpoints
@router.post("/", response_model=RoleRead)
def create_role(
role_data: RoleCreate,
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("role:create"))
):
"""Create a new role (requires role:create permission)"""
return RBACService.create_role(db, role_data)
@router.get("/", response_model=List[RoleRead])
def list_roles(
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("role:read"))
):
"""List all roles (requires role:read permission)"""
roles = db.execute(select(Role)).scalars().all()
return roles
@router.get("/{role_id}", response_model=RoleRead)
def get_role(
role_id: UUID,
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("role:read"))
):
"""Get a specific role by ID"""
role = db.execute(select(Role).where(
Role.id == role_id)).scalar_one_or_none()
if not role:
raise HTTPException(
status_code=status.HTTP_404_NOT_FOUND,
detail="Role not found"
)
return role
@router.post("/{role_id}/perms/", response_model=RoleRead)
def assign_permission_to_role(
role_id: UUID,
permission_request: AssignPermissionRequest,
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("role:manage"))
):
"""Assign a permission to a role"""
return RBACService.assign_permission_to_role(
    db, role_id, permission_request.permission_id
)
@router.delete("/{role_id}/perms/{perm_id}/", response_model=RoleRead)
def remove_permission_from_role(
role_id: UUID,
perm_id: UUID,
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("role:manage"))
):
"""Remove a permission from a role"""
return RBACService.remove_permission_from_role(db, role_id, perm_id)
@router.get("/{role_id}/perms/", response_model=List[PermissionRead])
def get_role_permissions(
role_id: UUID,
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("role:read"))
):
"""Get all permissions for a role"""
permissions = RBACService.get_role_permissions(db, role_id)
return permissions

# Permission endpoints
@permission_router.post("/", response_model=PermissionRead)
def create_permission(
permission_data: PermissionCreate,
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("permission:create"))
):
"""Create a new permission"""
return RBACService.create_permission(db, permission_data)
@permission_router.get("/", response_model=List[PermissionRead])
def list_permissions(
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("permission:read"))
):
"""List all permissions"""
permissions = db.execute(select(Permission)).scalars().all()
return permissions

# User role management endpoints
@router.post("/users/{user_id}/roles/{role_id}/")
def assign_role_to_user(
user_id: UUID,
role_id: UUID,
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("user:manage"))
):

"""Assign a role to a user"""
user = RBACService.assign_role_to_user(db, user_id, role_id)
return {"message": "Role assigned successfully"}
@router.get("/users/{user_id}/roles/", response_model=List[RoleRead])
def get_user_roles(
user_id: UUID,
db: Session = Depends(get_db),
current_user: User = Depends(require_permission("user:read"))
):
"""Get all roles for a user"""
return RBACService.get_user_roles(db, user_id)
