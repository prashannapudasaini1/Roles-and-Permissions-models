from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.db.models.roles.role import Role, Permission
from app.db.models.users.user import User
from app.api.v1.schemas.role import RoleCreate, PermissionCreate
from fastapi import HTTPException, status

class RBACService:
@staticmethod
def create_role(db: Session, data: RoleCreate) -> Role:
 """Create a new role"""
 # Check if role name already exists
 existing_role = db.execute(
 select(Role).where(Role.name == data.name)
 ).scalar_one_or_none()
 if existing_role:
 raise HTTPException(
 status_code=status.HTTP_400_BAD_REQUEST,
 detail="Role with this name already exists"
 )

role = Role(name=data.name, description=data.description)
 db.add(role)
 db.commit()
 db.refresh(role)
return role
@staticmethod
def create_permission(db: Session, data: PermissionCreate) -> Permission:
 """Create a new permission"""
 # Check if permission name already exists
 existing_permission = db.execute(
 select(Permission).where(Permission.name == data.name)
 ).scalar_one_or_none()
 if existing_permission:
 raise HTTPException(
 status_code=status.HTTP_400_BAD_REQUEST,
 detail="Permission with this name already exists"
 )
 permission = Permission(name=data.name, description=data.description)
 db.add(permission)
 db.commit()
 db.refresh(permission)
 return permission
@staticmethod
def assign_permission_to_role(db: Session, role_id: UUID, perm_id: UUID) -> Role:
 """Assign a permission to a role"""
 role = db.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
 if not role:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail="Role not found"
 )
 permission = db.execute(
ermission.id == perm_id)
 ).scalar_one_or_none()
 if not permission:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail="Permission not found"
 )

# Check if permission is already assigned to role
 if permission in role.permissions:
 raise HTTPException(
 status_code=status.HTTP_400_BAD_REQUEST,
 detail="Permission already assigned to this role"
 )
 role.permissions.append(permission)
 db.commit()
 db.refresh(role)
 return role
@staticmethod
def remove_permission_from_role(db: Session, role_id: UUID, perm_id: UUID) -> Role:
 """Remove a permission from a role"""
 role = db.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
 if not role:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail="Role not found"
 )
 permission = db.execute(
 select(Permission).where(Permission.id == perm_id)
 ).scalar_one_or_none()
 if not permission:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail="Permission not found"
 )

 # Check if permission is assigned to role
 if permission not in role.permissions:
 raise HTTPException(
 status_code=status.HTTP_400_BAD_REQUEST,
 detail="Permission not assigned to this role"
 )
 role.permissions.remove(permission)
 db.commit()
 db.refresh(role)

 return role
@staticmethod
def get_role_permissions(db: Session, role_id: UUID) -> List[Permission]:
 """Get all permissions for a role"""
 role = db.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
 if not role:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail="Role not found"
 )
 return role.permissions
@staticmethod
def get_user_roles(db: Session, user_id: UUID) -> List[Role]:
 """Get all roles for a user"""
 user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
 if not user:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail="User not found"
)
 return user.roles
@staticmethod
def assign_role_to_user(db: Session, user_id: UUID, role_id: UUID) -> User:
 """Assign a role to a user"""
 user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
 if not user:
 raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail="User not found"
 )
 role = db.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
 if not role:
raise HTTPException(
 status_code=status.HTTP_404_NOT_FOUND,
 detail="Role not found"
 )
 if role in user.roles:
 raise HTTPException(
 status_code=status.HTTP_400_BAD_REQUEST,
 detail="Role already assigned to this user"
 )
 user.roles.append(role)
 db.commit()
 db.refresh(user)
 return user
@staticmethod
def get_user_permissions(db: Session, user_id: UUID) -> List[str]:
 """Get all permission names for a user (through their roles)"""
 user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
 if not user:
 return []
 permissions = set()
 for role in user.roles:
 for permission in role.permissions:
 permissions.add(permission.name)
 return list(permissions)
