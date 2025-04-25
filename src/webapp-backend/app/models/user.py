from pydantic import BaseModel, EmailStr
from enum import Enum
from uuid import UUID

class RoleEnum(str, Enum):
    RESEARCHER = 'Researcher'
    TECHNICIAN = 'Technician'
    ADMIN = 'Admin'
        
    @property
    def rdf_uri(self) -> str:
        """Return the RDF URI corresponding to the Role."""
        return f'<http://data.bfh.ch/Roles/{self.value}>'

    @classmethod
    def from_rdf_uri(cls, rdf_uri: str):
        """Create a RoleEnum from the RDF URI."""
        # The RDF URI structure is expected to be in the format: http://data.bfh.ch/Roles/<role>
        cleaned_uri = rdf_uri.strip('<>')
        role_name = cleaned_uri.split('/')[-1]
        try:
            return cls(role_name)
        except ValueError:
            raise ValueError(f"Invalid RDF URI: {rdf_uri} does not correspond to a valid Role.")


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