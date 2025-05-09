from pydantic import BaseModel, EmailStr
from enum import Enum
from uuid import UUID
from app.models.common import RDFEnumMixin

class RoleEnum(RDFEnumMixin, str, Enum):
    RESEARCHER = 'Researcher'
    TECHNICIAN = 'Technician'
    ADMIN = 'Admin'


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: RoleEnum

class UserIn(UserBase):
    """Model used when new user gets created"""
    password: str

class UserOut(UserBase):
    """Model used to send data back over API"""
    uuid: UUID

class UserInDB(UserBase):
    """Model used internally to handle auth logic"""
    uuid: UUID
    hashed_password: str

class UserChangePw(BaseModel):
    """Model used when some field on an user get updated"""
    current_password: str
    new_password: str

class UserLogin(BaseModel):
    """Model used when user tries to login over API"""
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str