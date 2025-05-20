from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from uuid import UUID

from app.dependencies import require_roles_or_owner, get_compilation_service
from app.services.compilation_service import CompilationService
from app.models.user import UserInDB, RoleEnum
from app.models.compilation import InitBuildResponse, BuildJobStatusResponse
from app.utils.exceptions import NotFoundError, ExternalServiceError


router = APIRouter(
    prefix="/compilation",
    tags=["compilation"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/build/{sensor_node_uuid}", response_model=InitBuildResponse)
async def create_build_job(sensor_node_uuid: UUID,
                           _: UserInDB = Depends(require_roles_or_owner([RoleEnum.ADMIN, RoleEnum.TECHNICIAN])),
                           compilation_service: CompilationService = Depends(get_compilation_service)) -> InitBuildResponse:
    try:
        return await compilation_service.initiate_build_job(sensor_node_uuid)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/job/{job_id}/status", response_model=BuildJobStatusResponse)
async def get_build_job_status(job_id: UUID,
                              _: UserInDB = Depends(require_roles_or_owner([RoleEnum.ADMIN, RoleEnum.TECHNICIAN])),
                              compilation_service: CompilationService = Depends(get_compilation_service)) -> BuildJobStatusResponse:
    try:
        return await compilation_service.get_build_job_status(job_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/job/{job_id}/artifacts", response_class=Response)
async def get_build_job_artifacts(job_id: UUID, get_source_code: bool = False, get_logs: bool = False, bin_only: bool = False,
                                 _: UserInDB = Depends(require_roles_or_owner([RoleEnum.ADMIN, RoleEnum.TECHNICIAN])),
                                 compilation_service: CompilationService = Depends(get_compilation_service)) -> Response:
    try:
        return await compilation_service.get_build_job_artifacts(job_id, get_source_code, get_logs, bin_only)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))