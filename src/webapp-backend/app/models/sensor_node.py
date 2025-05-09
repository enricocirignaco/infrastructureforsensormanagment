from pydantic import BaseModel, HttpUrl
from datetime import datetime

from enum import Enum
from uuid import UUID
from typing import Optional, List
from app.models.user import UserOut
from app.models.common import RDFEnumMixin


class SensorNodeStateEnum(RDFEnumMixin, str, Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    ARCHIVED = 'Archived'


class SensorNodeBase(BaseModel):
    pass

# Models used to return data

class SensorNodeOutSlim(BaseModel):
    uuid: UUID
    name: str
    state: SensorNodeStateEnum