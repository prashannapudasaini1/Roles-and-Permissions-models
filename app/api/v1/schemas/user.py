from pydantic import EmailStr, BaseModel
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool

class Token(BaseModel):
    access_token: str
    token_type: str