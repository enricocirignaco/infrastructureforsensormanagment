from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum
from uuid import UUID
from app.models.user import UserOut
from app.models.common import RDFEnumMixin

class ProjectLinkEnum(RDFEnumMixin, str, Enum):
    WEBSITE = 'Website'
    MS_TEAMS = 'MS-Teams'
    REPORT = 'Report'
    DOCUMENTATION = 'Documentation'
    MISC = 'Misc'

class ProjectStateEnum(RDFEnumMixin, str, Enum):
    PREPARED = 'Prepared'
    ACTIVE = 'Active'
    ARCHIVED = 'Archived'

class ProjectLogbookEnum(RDFEnumMixin, str, Enum):
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