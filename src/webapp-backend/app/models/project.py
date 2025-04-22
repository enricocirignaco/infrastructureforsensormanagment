from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from uuid import UUID


class ProjectLinkEnum(str, Enum):
    WEBSITE = 'Website'
    MS_TEAMS = 'MS Teams'
    REPORT = 'Report'
    DOCUMENTATION = 'Documentation'
    MISC = 'Misc'

class ProjectStateEnum(str, Enum):
    ACTIVE = 'Active'
    ARCHIVED = 'Archived'
    DELETED = 'Deleted'

class ProjectLink(BaseModel):
    name: Optional[str]
    url: str
    type: ProjectLinkEnum


class ProjectBase(BaseModel):
    name: str
    short_name: str
    description: str
    external_props: List[ProjectLink]


class ProjectInDB(ProjectBase):
    id: UUID
    state: ProjectStateEnum
   
class ProjectOut(ProjectInDB):
    pass