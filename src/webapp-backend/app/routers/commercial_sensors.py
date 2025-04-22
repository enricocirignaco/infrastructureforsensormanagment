from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

from ..dependencies import require_roles_or_owner
from app.models.user import UserInDB, RoleEnum
from app.models.commercial_sensor import CommercialSensorIn, CommercialSensorOutSlim, CommercialSensorOutFull

router = APIRouter(
    prefix="/commercial-sensors",
    tags=["commercial sensors"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[CommercialSensorOutSlim])
async def read_all_commercial_sensors(_: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))) -> List[CommercialSensorOutSlim]:
    pass

@router.get("/{uuid}", response_model=CommercialSensorOutFull)
async def read_specific_commercial_sensors(uuid: UUID,
                                _: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))) -> CommercialSensorOutFull:
    pass

@router.post("/", response_model=CommercialSensorOutFull)
async def create_new_commercial_sensor(commercial_sensor: CommercialSensorIn,
                             _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))) -> CommercialSensorOutFull:
    pass

@router.put("/{uuid}", response_model=CommercialSensorOutFull)
async def update_specific_commercial_sensor(uuid: UUID,
                                  commercial_sensor: CommercialSensorIn,
                                  _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))) -> CommercialSensorOutFull:
    pass

@router.delete("/{uuid}")
async def delete_specific_commercial_sensor(uuid: UUID,
                                  _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))):
    pass