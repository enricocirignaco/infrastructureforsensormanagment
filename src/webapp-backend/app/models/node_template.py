from pydantic import BaseModel, HttpUrl
from datetime import datetime

from enum import Enum
from uuid import UUID
from typing import Optional, List
from app.models.user import UserOut
from app.models.commercial_sensor import CommercialSensorOutSlim
from app.models.sensor_node import SensorNodeOutSlim
from app.models.common import RDFEnumMixin

class ProtobufDatatypeEnum(RDFEnumMixin, str, Enum):
    DOUBLE = 'double'
    FLOAT = 'float'
    INT32 = 'int32'
    INT64 = 'int64'
    UINT32 = 'uint32'
    UINT64 = 'uint64'
    SINT32 = 'sint32'
    SINT64 = 'sint64'
    FIXED32 = 'fixed32'
    FIXED64 = 'fixed64'
    SFIXED32 = 'sfixed32'
    SFIXED64 = 'sfixed64'
    BOOL = 'bool'
    STRING = 'string'
    BYTES = 'bytes'

class NodeTemplateLogbookEnum(RDFEnumMixin, str, Enum):
    CREATED = 'Created'
    UPDATED = 'Updated'

class NodeTemplateStateEnum(RDFEnumMixin, str, Enum):
    UNUSED = 'Unused'
    IN_USE = 'In-Use'
    ARCHIVED = 'Archived'

class HardwareBoard(BaseModel):
    core: str
    variant: str

class ConfigurableDefinition(BaseModel):
    name: str

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
    gitlab_url: HttpUrl
    board: HardwareBoard
    configurables: List[ConfigurableDefinition]


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
    inherited_sensor_nodes: List[SensorNodeOutSlim]
    state: NodeTemplateStateEnum

# Models used to return data

class NodeTemplateOutSlim(BaseModel):
    uuid: UUID
    name: str
    board: HardwareBoard
    state: NodeTemplateStateEnum

class NodeTemplateOutFull(NodeTemplateBase):
    uuid: UUID
    logbook: List[NodeTemplateLogbookEntry]
    inherited_sensor_nodes: List[SensorNodeOutSlim]
    state: NodeTemplateStateEnum