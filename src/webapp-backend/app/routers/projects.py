from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

from ..dependencies import require_roles_or_owner
from app.models.user import UserInDB, RoleEnum
from app.models.project import ProjectStateEnum, ProjectBase, ProjectLink, ProjectOut


router = APIRouter(
    prefix="/projects",
    tags=["project"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ProjectOut])
async def read_all_projects(_: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))) -> List[ProjectOut]:
    pass

@router.get("/{uuid}", response_model=ProjectOut)
async def read_specific_project(uuid: UUID,
                                _: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))) -> ProjectOut:
    pass

@router.post("/", response_model=ProjectOut)
async def create_new_project(project: ProjectBase,
                             _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))) -> ProjectOut:
    pass

@router.put("/{uuid}", response_model=ProjectOut)
async def update_specific_project(uuid: UUID,
                                  project: ProjectOut,
                                  _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))) -> ProjectOut:
    pass

@router.delete("/{uuid}")
async def delete_specific_project(uuid: UUID,
                                  _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN]))):
    pass