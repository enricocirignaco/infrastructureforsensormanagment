from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class InitBuildResponse(BaseModel):
    job_id: UUID
    status: str
    message: str
    timestamp: datetime
    
class BuildJobStatusResponse(BaseModel):
    status: str
    message: str