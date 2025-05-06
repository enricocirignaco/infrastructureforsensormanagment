from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID

from app.dependencies import require_roles_or_owner, get_project_service ,get_node_template_service
from app.utils.exceptions import NotFoundError
from app.models.user import UserInDB, RoleEnum
from app.models.project import ProjectBase, ProjectOutSlim, ProjectOutFull, ProjectUpdate
from app.models.node_template import NodeTemplateOutSlim, NodeTemplateOutFull, NodeTemplateCreate
from app.services.project_service import ProjectService
from app.services.node_template_service import NodeTemplateService


router = APIRouter(
    prefix="/projects",
    tags=["project"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

# Projects

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
                             logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                             project_service: ProjectService = Depends(get_project_service)) -> ProjectOutFull:
    return project_service.create_project(project, logged_in_user=logged_in_user)

@router.put("/{uuid}", response_model=ProjectOutFull)
async def update_specific_project(uuid: UUID,
                                  project: ProjectUpdate,
                                  logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                  project_service: ProjectService = Depends(get_project_service)) -> ProjectOutFull:
    try:
        return project_service.update_project(uuid=uuid, project=project, logged_in_user=logged_in_user)
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
    

# Node Templates

@router.get("/{uuid}/node-templates", response_model=List[NodeTemplateOutSlim])
async def read_all_node_templates_by_project(_: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                            node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> List[NodeTemplateOutSlim]:
    pass

@router.post("/{uuid}/node-templates", status_code=201, response_model=NodeTemplateOutFull)
async def create_new_node_template_in_project(project: NodeTemplateCreate,
                             logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                             node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> NodeTemplateOutFull:
    pass