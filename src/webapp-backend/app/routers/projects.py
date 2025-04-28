from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from app.dependencies import require_roles_or_owner, get_project_service
from app.utils.exceptions import NotFoundError
from app.models.user import UserInDB, RoleEnum
from app.models.project import ProjectBase, ProjectOutSlim, ProjectOutFull
from app.services.project_service import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["project"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ProjectOutSlim])
async def read_all_projects(_: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                            project_service: ProjectService = Depends(get_project_service)) -> List[ProjectOutSlim]:
    return project_service.get_all_projects()

@router.get("/{uuid}", response_model=ProjectOutFull)
async def read_specific_project(uuid: UUID,
                                _: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                project_service: ProjectService = Depends(get_project_service)) -> ProjectOutFull:
    try:
        return project_service.get_project_by_uuid(uuid=uuid)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

@router.post("/", status_code=201, response_model=ProjectOutFull)
async def create_new_project(project: ProjectBase,
                             _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                             project_service: ProjectService = Depends(get_project_service)) -> ProjectOutFull:
    return project_service.create_project(project)

@router.put("/{uuid}", response_model=ProjectOutFull)
async def update_specific_project(uuid: UUID,
                                  project: ProjectOutFull,
                                  _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                  project_service: ProjectService = Depends(get_project_service)) -> ProjectOutFull:
    try:
        return project_service.update_project(uuid=uuid, project=project)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

@router.delete("/{uuid}", status_code=204)
async def delete_specific_project(uuid: UUID,
                                  _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                  project_service: ProjectService = Depends(get_project_service)):
    try:
        project_service.delete_project(uuid=uuid)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))