from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum
from uuid import UUID
from app.models.user import UserOut


class CommercialSensorLinkEnum(str, Enum):
    DATASHEET = 'Datasheet'
    WEBSHOP = 'Webshop'
    MISC = 'Misc'

    @property
    def rdf_uri(self) -> str:
        """Return the RDF URI corresponding to the CommercialSensorLinkEnum."""
        return f'http://data.bfh.ch/CommercialSensorLinkType/{self.value}'

    @classmethod
    def from_rdf_uri(cls, rdf_uri: str):
        """Create a CommercialSensorLinkEnum from the RDF URI."""
        # The RDF URI structure is expected to be in the format: http://data.bfh.ch/CommercialSensorLinkType/<type>
        cleaned_uri = rdf_uri.strip('<>')
        type_name = cleaned_uri.split('/')[-1]
        try:
            return cls(type_name)
        except ValueError:
            raise ValueError(f"Invalid RDF URI: {rdf_uri} does not correspond to a valid CommercialSensorLinkType.")


class CommercialSensorLogbookEnum(str, Enum):
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