from app.repositories.sensor_node_repository import SensorNodeRepository
from app.models.sensor_node import SensorNodeDB, SensorNodeOutSlim, SensorNodeOutFull, SensorNodeUpdate, SensorNodeCreate
from app.models.user import UserInDB, UserOut, RoleEnum
from app.utils.exceptions import NotFoundError

from fastapi import HTTPException, status
from datetime import datetime
from typing import List
from uuid import UUID, uuid4

class SensorNodeService:

    def __init__(self, sensor_node_repository: SensorNodeRepository):
        self._sensor_node_repository = sensor_node_repository
        
    def get_all_sensor_nodes(self, filters: dict = None) -> List[SensorNodeOutSlim]:
        if filters is None:
            filters = {}
        pass
    
    def get_sensor_node_by_uuid(self, uuid: UUID) -> SensorNodeOutFull:
        pass
    
    def create_sensor_node(self, sensor_node: SensorNodeCreate, logged_in_user: UserInDB) -> SensorNodeOutFull:
        pass
    
    def update_sensor_node(self, uuid: UUID, sensor_node: SensorNodeUpdate, logged_in_user: UserInDB) -> SensorNodeOutFull:
        pass
    
    def delete_sensor_node(self, uuid: UUID) -> None:
        pass
    
    