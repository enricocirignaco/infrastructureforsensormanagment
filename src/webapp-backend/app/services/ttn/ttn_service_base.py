from abc import ABC, abstractmethod
from uuid import UUID
from app.models.sensor_node import TTNKeys

class TtnServiceBase(ABC):

    @abstractmethod
    async def create_device(self, sensor_node_id: UUID) -> TTNKeys:
        pass

    @abstractmethod
    async def delete_device(self, sensor_node_id: str):
        pass

    @abstractmethod
    def build_device_link(self, sensor_node_id: UUID) -> str:
        pass