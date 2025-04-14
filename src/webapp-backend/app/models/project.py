from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from uuid import UUID


class LinkTypeEnum(str, Enum):
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
    type: LinkTypeEnum


class ProjectBase(BaseModel):
    id: UUID
    name: str
    short_name: str
    description: str
    external_props: List[ProjectLink]


class ProjectOut(ProjectBase):
    state: ProjectStateEnum