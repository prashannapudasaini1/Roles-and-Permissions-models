from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from uuid import UUID

class PermissionBase(BaseModel):
name: str
description: Optional[str] = None
class PermissionCreate(PermissionBase):
pass
class PermissionRead(PermissionBase):
model_config = ConfigDict(from_attributes=True)
id: UUID

class RoleBase(BaseModel):
name: str
description: Optional[str] = None
class RoleCreate(RoleBase):
pass
class RoleRead(RoleBase):
model_config = ConfigDict(from_attributes=True)
id: UUID
permissions: List[PermissionRead] = []
class AssignPermissionRequest(BaseModel):
permission_id: UUID

