# services/ttn/mock.py
from app.services.ttn.ttn_service_base import TtnServiceBase
from app.models.sensor_node import TTNKeys
from uuid import UUID

class TtnServiceMock(TtnServiceBase):
    
    async def create_device(self, sensor_node_id: UUID) -> TTNKeys:
        return TTNKeys(app_key="00000000000000000000000000000000", dev_eui="0000000000000000", join_eui="0000000000000000")

    async def delete_device(self, sensor_node_id: str):
        pass
    
    def build_device_link(self, sensor_node_id: UUID) -> str:
        return "https://eu1.cloud.thethings.network/console"
