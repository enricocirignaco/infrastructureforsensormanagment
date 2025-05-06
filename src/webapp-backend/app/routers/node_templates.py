from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from typing import List
from uuid import UUID

from ..dependencies import require_roles_or_owner, get_node_template_service
from app.utils.exceptions import NotFoundError
from app.models.user import UserInDB, RoleEnum
from app.models.node_template import NodeTemplateOutSlim, NodeTemplateOutFull, NodeTemplateUpdate
from app.services.node_template_service import NodeTemplateService

router = APIRouter(
    prefix="/node-templates",
    tags=["node templates"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[NodeTemplateOutSlim])
async def read_all_node_templates(_: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                  node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> List[NodeTemplateOutSlim]:
    pass


@router.get("/{uuid}", response_model=NodeTemplateOutFull)
async def read_specific_node_template(uuid: UUID,
                                      _: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                      node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> NodeTemplateOutFull:
    pass


@router.put("/{uuid}", response_model=NodeTemplateOutFull)
async def update_specific_node_template(uuid: UUID,
                                        node_template: NodeTemplateUpdate,
                                        logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                        node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> NodeTemplateOutFull:
    pass

@router.delete("/{uuid}", status_code=204)
async def delete_specific_node_template(uuid: UUID,
                                        _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                        node_template_service: NodeTemplateService = Depends(get_node_template_service)):
    pass


@router.get("/{uuid}/schema", response_class=Response)
async def download_protobuf_schema_of_node_template(uuid: UUID,
                                                _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                                node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> Response:
    pass


@router.get("/{uuid}/code", response_class=StreamingResponse)
async def download_generated_protobuf_code(uuid: UUID,
                                           _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                           node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> StreamingResponse:
    pass