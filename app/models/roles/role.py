from sqlalchemy import Column, String, Text, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

# Association table for role-permissions many-tomany relationship
role_permissions = Table(
'role_permissions',
Base.metadata,
Column('role_id', UUID(as_uuid=True), ForeignKey('
roles.id', ondelete='CASCADE'), primary_key=True),
Column('permission_id', UUID(as_uuid=True), ForeignKey('
permissions.id', ondelete='CASCADE'), primary_key=True)
)

# Association table for user-roles many-to-many relationship
user_roles = Table(
'user_roles',
Base.metadata,
Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True))
class Role(Base):
tablename = "roles"
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
name = Column(String(100), unique=True, nullable=False, index=True)
description = Column(Text, nullable=True)
# Relationships
permissions = relationship("Permission", secondary=role_permissions, back_populates="r
oles")
users = relationship("User", secondary=user_roles, back_populates="roles")
class Permission(Base):
tablename = "permissions"
id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
name = Column(String(100), unique=True, nullable=False, index=True)
description = Column(Text, nullable=True)
# Relationships
roles = relationship("Role", secondary=role_permissions, back_populates="permissions")