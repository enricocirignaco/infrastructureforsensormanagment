from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ..dependencies import require_roles_or_owner, get_commercial_sensor_service
from app.utils.exceptions import NotFoundError
from app.models.user import UserInDB, RoleEnum
from app.models.commercial_sensor import CommercialSensorIn, CommercialSensorOutSlim, CommercialSensorOutFull, CommercialSensorUpdate
from app.services.commercial_sensor_service import CommercialSensorService

router = APIRouter(
    prefix="/commercial-sensors",
    tags=["commercial sensors"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[CommercialSensorOutSlim])
async def read_all_commercial_sensors(_: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                      commercial_sensor_service: CommercialSensorService = Depends(get_commercial_sensor_service)) -> List[CommercialSensorOutSlim]:
    return commercial_sensor_service.get_all_commercial_sensors()

@router.get("/{uuid}", response_model=CommercialSensorOutFull)
async def read_specific_commercial_sensors(uuid: UUID,
                                _: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                commercial_sensor_service: CommercialSensorService = Depends(get_commercial_sensor_service)) -> CommercialSensorOutFull:
    try:
        return commercial_sensor_service.get_commercial_sensor_by_uuid(uuid=uuid)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

@router.post("/", status_code=201, response_model=CommercialSensorOutFull)
async def create_new_commercial_sensor(commercial_sensor: CommercialSensorIn,
                             logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                             commercial_sensor_service: CommercialSensorService = Depends(get_commercial_sensor_service)) -> CommercialSensorOutFull:
    return commercial_sensor_service.create_commercial_sensor(commercial_sensor, logged_in_user=logged_in_user)

@router.put("/{uuid}", response_model=CommercialSensorOutFull)
async def update_specific_commercial_sensor(uuid: UUID,
                                  commercial_sensor: CommercialSensorUpdate,
                                  logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                  commercial_sensor_service: CommercialSensorService = Depends(get_commercial_sensor_service)) -> CommercialSensorOutFull:
    try:
        return commercial_sensor_service.update_commercial_sensor(uuid=uuid, commercial_sensor=commercial_sensor, logged_in_user=logged_in_user)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

@router.delete("/{uuid}", status_code=204)
async def delete_specific_commercial_sensor(uuid: UUID,
                                  _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                  commercial_sensor_service: CommercialSensorService = Depends(get_commercial_sensor_service)):
    try:
        commercial_sensor_service.delete_commercial_sensor(uuid=uuid)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))