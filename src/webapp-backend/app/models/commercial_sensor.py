from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum
from uuid import UUID
from app.models.user import UserOut
from app.models.common import RDFEnumMixin

class CommercialSensorLinkEnum(RDFEnumMixin, str, Enum):
    DATASHEET = 'Datasheet'
    WEBSHOP = 'Webshop'
    MISC = 'Misc'

class CommercialSensorLogbookEnum(RDFEnumMixin, str, Enum):
    CREATED = 'Created'
    UPDATED = 'Updated'

class CommercialSensorLink(BaseModel):
    name: Optional[str]
    url: str
    type: CommercialSensorLinkEnum

class CommercialSensorLogbookEntry(BaseModel):
    type: CommercialSensorLogbookEnum
    date: datetime
    user: UserOut


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

class CommercialSensorUpdate(CommercialSensorBase):
    uuid: Optional[UUID]

# Model used internally

class CommercialSensorInDB(CommercialSensorBase):
    uuid: UUID
    logbook: List[CommercialSensorLogbookEntry]

# Models that get returned to the client

class CommercialSensorOutSlim(BaseModel):
    uuid: UUID
    name: str
    alias: str

class CommercialSensorOutFull(CommercialSensorInDB):
    pass