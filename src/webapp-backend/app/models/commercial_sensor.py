from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from uuid import UUID

class CommercialSensorLinkEnum(str, Enum):
    DATASHEET = 'Datasheet'
    WEBSHOP = 'Webshop'
    MISC = 'Misc'

class CommercialSensorLink(BaseModel):
    name: Optional[str]
    url: str
    type: CommercialSensorLinkEnum

class CommercialSensorRange(BaseModel):
    min: int
    max: int

class CommercialSensorProps(BaseModel):
    name: str
    unit: str
    precision: int
    range: CommercialSensorRange

class CommercialSensorBase(BaseModel):
    name: str
    alias: str
    description: str
    external_props: Optional[List[CommercialSensorLink]]
    sensor_props: Optional[List[CommercialSensorProps]]

# Model used to create new commercial sensor (alias for base)

class CommercialSensorIn(CommercialSensorBase):
    pass

# Model used internally

class CommercialSensorInDB(CommercialSensorBase):
    uuid: UUID
    #logbook: List[]

# Models that get returned to the client

class CommercialSensorOutSlim(BaseModel):
    uuid: UUID
    name: str
    alias: str

class CommercialSensorOutFull(CommercialSensorInDB):
    pass