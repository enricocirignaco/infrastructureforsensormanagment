from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from ..dependencies import require_roles_or_owner, get_sensor_node_service
from app.utils.exceptions import NotFoundError
from app.models.user import UserInDB, RoleEnum
from app.models.sensor_node import SensorNodeOutSlim, SensorNodeOutFull, SensorNodeUpdate, SensorNodeCreate
from app.services.sensor_node_service import SensorNodeService

router = APIRouter(
    prefix="/sensor-nodes",
    tags=["sensor nodes"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[SensorNodeOutSlim])
async def read_all_sensor_nodes(
    project_uuid: UUID | None = None,
    node_template_uuid: UUID | None = None,
    _: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
    sensor_node_service: SensorNodeService = Depends(get_sensor_node_service)
) -> List[SensorNodeOutSlim]:
    return sensor_node_service.get_all_sensor_nodes(
        filters={"project_uuid": project_uuid, "node_template_uuid": node_template_uuid}
    )

@router.post("/", status_code=201, response_model=SensorNodeOutFull)
async def create_new_sensor_node(
    sensor_node: SensorNodeCreate,
    logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
    sensor_node_service: SensorNodeService = Depends(get_sensor_node_service)
) -> SensorNodeOutFull:
    return sensor_node_service.create_sensor_node(sensor_node=sensor_node, logged_in_user=logged_in_user)

@router.get("/{uuid}", response_model=SensorNodeOutFull)
async def read_specific_sensor_node(
    uuid: UUID,
    _: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
    sensor_node_service: SensorNodeService = Depends(get_sensor_node_service)
) -> SensorNodeOutFull:
    try:
        return sensor_node_service.get_sensor_node_by_uuid(uuid=uuid)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    
@router.put("/{uuid}", response_model=SensorNodeOutFull)
async def update_specific_sensor_node(
    uuid: UUID,
    sensor_node: SensorNodeUpdate,
    logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
    sensor_node_service: SensorNodeService = Depends(get_sensor_node_service)
) -> SensorNodeOutFull:
    try:
        return sensor_node_service.update_sensor_node(uuid=uuid, sensor_node=sensor_node, logged_in_user=logged_in_user)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    
@router.delete("/{uuid}", status_code=204)
async def delete_specific_sensor_node(
    uuid: UUID,
    _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
    sensor_node_service: SensorNodeService = Depends(get_sensor_node_service)
):
    try:
        sensor_node_service.delete_sensor_node(uuid=uuid)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))