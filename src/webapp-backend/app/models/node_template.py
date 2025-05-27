from pydantic import BaseModel, HttpUrl, field_validator
from datetime import datetime
import re

from enum import Enum
from uuid import UUID
from typing import Optional, List
from app.models.user import UserOut
from app.models.commercial_sensor import CommercialSensorOutSlim
from app.models.common import RDFEnumMixin, ConfigurableTypeEnum

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
    type: ConfigurableTypeEnum

class NodeTemplateLogbookEntry(BaseModel):
    type: NodeTemplateLogbookEnum
    date: datetime
    user: UserOut

class NodeTemplateField(BaseModel):
    field_name: str
    protbuf_datatype: ProtobufDatatypeEnum
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
    state: NodeTemplateStateEnum
    protobuf_message_name: Optional[str] = None

# Models used to return data

class NodeTemplateOutSlim(BaseModel):
    uuid: UUID
    name: str
    board: HardwareBoard
    state: NodeTemplateStateEnum

class NodeTemplateOutFull(NodeTemplateBase):
    uuid: UUID
    logbook: List[NodeTemplateLogbookEntry]
    state: NodeTemplateStateEnum

# Models used for API requests to protobuf service
class ProtobufSchemaField(BaseModel):
    field_name: str
    protobuf_datatype: ProtobufDatatypeEnum
    
    @field_validator('field_name')
    @classmethod
    def validate_field_name(cls, v):
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', v):
            raise ValueError('Invalid field_name: must be a valid identifier without spaces')
        return v

class ProtobufSchema(BaseModel):
    message_name: str
    fields: List[ProtobufSchemaField]
    
    @field_validator('message_name')
    @classmethod
    def validate_message_name(cls, v):
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', v):
            raise ValueError('Invalid message_name: must be a valid identifier without spaces')
        return v
