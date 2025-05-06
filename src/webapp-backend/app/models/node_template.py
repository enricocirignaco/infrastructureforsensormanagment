from pydantic import BaseModel, HttpUrl
from datetime import datetime

from enum import Enum
from uuid import UUID
from typing import Optional, List
from app.models.user import UserOut
from app.models.commercial_sensor import CommercialSensorOutSlim
from app.models.common import RDFEnumMixin

class NodeTemplateLogbookEnum(RDFEnumMixin, str, Enum):
    CREATED = 'Created'
    UPDATED = 'Updated'
#    FIELDS = 'Fields'  -> fields updaten geht nicht nach initialisierung des Templates
#    GIT_REF = 'Git-Ref' -> Git ref des templates anpassen möglicherweise auch nicht?

class NodeTemplateStateEnum(RDFEnumMixin, str, Enum):
    UNUSED = 'Unused'
    IN_USE = 'In-Use'
    ARCHIVED = 'Archived'

class NodeTemplateLogbookEntry(BaseModel):
    type: NodeTemplateLogbookEnum
    date: datetime
    user: UserOut

class NodeTemplateField(BaseModel):
    field_name: str
    protbuf_datatype: str
    unit: str
    commercial_sensor: Optional[CommercialSensorOutSlim]

class NodeTemplateBase(BaseModel):
    name: str
    description: str
    fields: List[NodeTemplateField]
    gitlab_url: HttpUrl # Cannot be changed later?
    git_ref: str
    hardware_type: str


# Models used for mutations (from API)

class NodeTemplateCreate(NodeTemplateBase):
    pass

class NodeTemplateUpdate(NodeTemplateBase):
    uuid: UUID
    state: NodeTemplateStateEnum

# Models used internally

class NodeTemplateDB(NodeTemplateBase):
    uuid: UUID
    logbook: List[NodeTemplateLogbookEntry]
    inherited_sensor_nodes: List[int]
    state: NodeTemplateStateEnum

# Models used to return data

class NodeTemplateOutSlim(BaseModel):
    uuid: UUID
    name: str
    hardware_type: str

class NodeTemplateOutFull(NodeTemplateBase):
    uuid: UUID
    logbook: List[NodeTemplateLogbookEntry]
    inherited_sensor_nodes: List[int]
    state: NodeTemplateStateEnum