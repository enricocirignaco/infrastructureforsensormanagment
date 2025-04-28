from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum
from uuid import UUID
from app.models.user import UserOut


class ProjectLinkEnum(str, Enum):
    WEBSITE = 'Website'
    MS_TEAMS = 'MS-Teams'
    REPORT = 'Report'
    DOCUMENTATION = 'Documentation'
    MISC = 'Misc'

    @property
    def rdf_uri(self) -> str:
        """Return the RDF URI corresponding to the ProjectLinkType."""
        return f'http://data.bfh.ch/ProjectLinkType/{self.value}'

    @classmethod
    def from_rdf_uri(cls, rdf_uri: str):
        """Create a RoleEnum from the RDF URI."""
        # The RDF URI structure is expected to be in the format: http://data.bfh.ch/ProjectLinkType/<type>
        cleaned_uri = rdf_uri.strip('<>')
        type_name = cleaned_uri.split('/')[-1]
        try:
            return cls(type_name)
        except ValueError:
            raise ValueError(f"Invalid RDF URI: {rdf_uri} does not correspond to a valid ProjectLinkType.")

class ProjectStateEnum(str, Enum):
    ACTIVE = 'Active'
    ARCHIVED = 'Archived'
    DELETED = 'Deleted'

    @property
    def rdf_uri(self) -> str:
        """Return the RDF URI corresponding to the ProjectState."""
        return f'http://data.bfh.ch/ProjectState/{self.value}'

    @classmethod
    def from_rdf_uri(cls, rdf_uri: str):
        """Create a RoleEnum from the RDF URI."""
        # The RDF URI structure is expected to be in the format: http://data.bfh.ch/ProjectState/<state>
        cleaned_uri = rdf_uri.strip('<>')
        state_name = cleaned_uri.split('/')[-1]
        try:
            return cls(state_name)
        except ValueError:
            raise ValueError(f"Invalid RDF URI: {rdf_uri} does not correspond to a valid ProjectState.")

class ProjectLogbookEnum(str, Enum):
    CREATED = 'Created'
    UPDATED = 'Updated'


class ProjectLink(BaseModel):
    name: Optional[str]
    url: str
    type: ProjectLinkEnum


class ProjectLogbookEntry(BaseModel):
    type: ProjectLogbookEnum
    date: datetime
    user: UserOut

class ProjectBase(BaseModel):
    name: str
    short_name: str
    description: str
    external_props: List[ProjectLink]

# Model used to create new project

class ProjectIn(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    uuid: Optional[UUID]
    state: ProjectStateEnum

# Model used internally

class ProjectInDB(ProjectBase):
    uuid: UUID
    state: ProjectStateEnum
    logbook: List[ProjectLogbookEntry]
   
# Models used to send data back to user

class ProjectOutSlim(BaseModel):
    uuid: UUID
    name: str
    short_name: str
    state: ProjectStateEnum

class ProjectOutFull(ProjectInDB):
    pass