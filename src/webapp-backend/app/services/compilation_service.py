from app.services.sensor_node_service import SensorNodeService
from app.services.node_template_service import NodeTemplateService
from app.utils.exceptions import NotFoundError, ExternalServiceError
from app.models.compilation import InitBuildResponse, BuildJobStatusResponse
from app.config import settings

from uuid import UUID
import httpx
from fastapi import Response

class CompilationService:

    def __init__(self, sensor_node_service: SensorNodeService,
                 node_template_service: NodeTemplateService):
        self._sensor_node_service = sensor_node_service
        self._node_template_service = node_template_service
        self._base_url = settings.COMPILER_ENGINE_BASE_URL
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def initiate_build_job(self, sensor_node_uuid: UUID) -> InitBuildResponse:
        sensor_node = self._sensor_node_service.get_sensor_node_by_uuid(sensor_node_uuid)
        if not sensor_node:
            raise NotFoundError(f"Sensor node with UUID {sensor_node_uuid} not found.")
        node_template = self._node_template_service.get_node_template_by_uuid(sensor_node.node_template_uuid)
        if not node_template:
            raise NotFoundError("Node template of sensor node not found.")

        payload = {
            "git_repo_url": str(node_template.gitlab_url),
            "firmware_tag": sensor_node.gitlab_ref,
            "board": {
                "core": node_template.board.core,
                "variant": node_template.board.variant
            },
            "config": [
                {"key": config.name, "value": config.value}
                for config in sensor_node.configurables
            ]
        }

        url = f"{self._base_url}/build"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=self._headers)

            if response.status_code == 200:
                data = response.json()
                print(data)  # TODO remove
                return InitBuildResponse(
                    job_id=data["job_id"],
                    status=data["status"],
                    message=data["message"],
                    timestamp=data["timestamp"]
                )
            else:
                raise ExternalServiceError(f"Failed to initiate build job: {response.text}")

        except httpx.RequestError as e:
            raise ExternalServiceError(f"Request to compiler service failed: {e}")

    async def get_build_job_status(self, job_id: UUID) -> BuildJobStatusResponse:
        url = f"{self._base_url}/job/{job_id}/status"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url=url, headers=self._headers)
                
            if response.status_code == 200:
                data = response.json()
                return BuildJobStatusResponse(
                    status=data["status"],
                    message=data["message"]
                )
            elif response.status_code == 404:
                raise NotFoundError(f"Build job with ID {job_id} not found.")
            else:
                raise ExternalServiceError(f"Failed to get build job status: {response.text}")

        except httpx.RequestError as e:
            raise ExternalServiceError(f"Request to compiler service failed: {e}")
        
    async def get_build_job_artifacts(self, job_id: UUID, get_source_code: bool, get_logs: bool, bin_only: bool) -> Response:
        url = f"{self._base_url}/job/{job_id}/artifacts"
        params = {
            "get_source_code": str(get_source_code).lower(),
            "get_logs": str(get_logs).lower(),
            "bin_only": str(bin_only).lower()
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=self._headers)

            if response.status_code == 200:
                return Response(
                    content=response.content,
                    headers={
                        "Content-Disposition": response.headers.get("content-disposition"),
                        "Content-Type": response.headers.get("content-type")
                    },
                    status_code=response.status_code,
                    media_type=response.headers.get("content-type")
                )
            elif response.status_code == 400:
                raise ValueError(f"Bad request: {response.text}")
            elif response.status_code == 404:
                raise NotFoundError(f"Build job with ID {job_id} not found.")
            else:
                raise ExternalServiceError(f"Failed to get build job artifacts: {response.text}")

        except httpx.RequestError as e:
            raise ExternalServiceError(f"Request to compiler service failed: {e}")
            