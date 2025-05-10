from pydantic import BaseModel, HttpUrl
from datetime import datetime

from enum import Enum
from uuid import UUID
from typing import Optional, List
from app.models.user import UserOut
from app.models.common import RDFEnumMixin
from app.models.node_template import NodeTemplateOutSlim
from app.models.project import ProjectOutSlim

class SensorNodeStateEnum(RDFEnumMixin, str, Enum):
    PREPARED = 'Prepared'
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    ARCHIVED = 'Archived'
    
class SensorNodeLogbookEnum(RDFEnumMixin, str, Enum):
    CREATED = 'Created'
    UPDATED = 'Updated'
    
class ConfigurableTypeEnum(RDFEnumMixin, str, Enum):
    USER_DEFINED = 'UserDefined'
    SYSTEM_DEFINED = 'SystemDefined'

class SensorNodeLocation(BaseModel):
    latitude: Optional[float]
    longitude: Optional[float]
    altitude: Optional[int]
    postalcode: Optional[str]

class SensorNodeLogbookEntry(BaseModel):
    type: SensorNodeLogbookEnum
    date: datetime
    user: UserOut

class ConfigurableAssignment(BaseModel):
    name: str
    type: ConfigurableTypeEnum
    value: str
    
class TimeseriesField(BaseModel):
    field_name: str
    protobuf_datatype: str
    unit: str
    value: str    

class TimeseriesData(BaseModel):
    timestamp: datetime
    fields: List[TimeseriesField]

class SensorNodeBase(BaseModel):
    name: str
    description: Optional[str]
    location: SensorNodeLocation
    configurables: List[ConfigurableAssignment]

# Models used for mutations (from API)

class SensorNodeCreate(SensorNodeBase):
    project_uuid: UUID
    node_template_uuid: UUID

class SensorNodeUpdate(SensorNodeBase):
    uuid: UUID
    state: SensorNodeStateEnum
    
# Models used internally

class SensorNodeDB(SensorNodeLocation):
    uuid: UUID
    logbook: List[SensorNodeLogbookEntry]
    state: SensorNodeStateEnum
    project_uuid: UUID
    node_template_uuid: UUID
    ttn_device_link: HttpUrl

# Models used to return data

class SensorNodeOutSlim(BaseModel):
    uuid: UUID
    name: str
    state: SensorNodeStateEnum
    node_template: NodeTemplateOutSlim
    project: ProjectOutSlim
    
class SensorNodeOutFull(SensorNodeBase):
    uuid: UUID
    logbook: List[SensorNodeLogbookEntry]
    state: SensorNodeStateEnum
    project_uuid: UUID
    node_template_uuid: UUID
    ttn_device_link: HttpUrl
    last_timeseries: TimeseriesData
    
    
    
# TODO datenmodell ausskizzieren


#{
#    "timestamp": "2023-10-01T12:00:00Z",
#    "fields": [
#        {
#            "field_name": "temp1",
#            "protobuf_datatype": "double",
#            "unit": "°C",
#            "value": "22.5"
#        },
#        {
#            "field_name": "hum1",
#            "protobuf_datatype": "double",
#            "unit": "%",
#            "value": "34"
#        }
#    ]
#}
