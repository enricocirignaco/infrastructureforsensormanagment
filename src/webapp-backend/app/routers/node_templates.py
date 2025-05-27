from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List
from uuid import UUID

from ..dependencies import require_roles_or_owner, get_node_template_service
from app.utils.exceptions import NotFoundError
from app.models.user import UserInDB, RoleEnum
from app.models.node_template import NodeTemplateOutSlim, NodeTemplateOutFull, NodeTemplateUpdate, NodeTemplateCreate
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
    return node_template_service.get_all_node_templates()


@router.get("/{uuid}", response_model=NodeTemplateOutFull)
async def read_specific_node_template(uuid: UUID,
                                      _: UserInDB = Depends(require_roles_or_owner([RoleEnum.RESEARCHER, RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                      node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> NodeTemplateOutFull:
    try:
        return node_template_service.get_node_template_by_uuid(uuid=uuid)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

@router.post("/", status_code=201, response_model=NodeTemplateOutFull)
async def create_new_node_template(project: NodeTemplateCreate,
                             logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                             node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> NodeTemplateOutFull:
    return await node_template_service.create_node_template(node_template=project, logged_in_user=logged_in_user)

@router.put("/{uuid}", response_model=NodeTemplateOutFull)
async def update_specific_node_template(uuid: UUID,
                                        node_template: NodeTemplateUpdate,
                                        logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                        node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> NodeTemplateOutFull:
    try:
        return node_template_service.update_node_template(uuid=uuid, node_template=node_template, logged_in_user=logged_in_user)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

@router.delete("/{uuid}", status_code=204)
async def delete_specific_node_template(uuid: UUID,
                                        _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                        node_template_service: NodeTemplateService = Depends(get_node_template_service)):
    try:
        node_template_service.delete_node_template(uuid=uuid)
    except NotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

@router.get("/{uuid}/schema", responses={
                200: {"description": "Protobug schema ready and returned"},
                202: {"description": "Schema generation in progress"},
                404: {"description": "Node template not found"}
            })
async def download_protobuf_schema_of_node_template(uuid: UUID,
                                                request: Request,
                                                _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                                node_template_service: NodeTemplateService = Depends(get_node_template_service)):
    schema = await node_template_service.get_protobuf_schema(uuid=uuid)

    accept_header = request.headers.get("accept", "")
    if "application/json" in accept_header:
        return JSONResponse(content={"schema": schema})
    else:
        return Response(
            content=schema,
            media_type="text/plain",
            headers={"Content-Disposition": "attachment; filename=schema.proto"}
        )


@router.get("/{uuid}/code", response_class=StreamingResponse)
async def download_generated_protobuf_code(uuid: UUID,
                                           _: UserInDB = Depends(require_roles_or_owner([RoleEnum.TECHNICIAN, RoleEnum.ADMIN])),
                                           node_template_service: NodeTemplateService = Depends(get_node_template_service)) -> StreamingResponse:
    raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Protobuf-Code-Generierung ist noch nicht implementiert."
        )
    return node_template_service.get_protobuf_code(uuid=uuid)