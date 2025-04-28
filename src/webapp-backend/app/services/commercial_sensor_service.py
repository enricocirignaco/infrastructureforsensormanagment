from app.repositories.commercial_sensor_repository import CommercialSensorRepository
from app.models.commercial_sensor import CommercialSensorInDB, CommercialSensorIn, CommercialSensorOutSlim, CommercialSensorOutFull
from app.utils.exceptions import NotFoundError

from typing import List
from uuid import UUID, uuid4

class CommercialSensorService:

    def __init__(self, commercial_sensor_repository: CommercialSensorRepository):
        self._commercial_sensor_repository = commercial_sensor_repository

    def get_commercial_sensor_by_uuid(self, uuid: UUID) -> CommercialSensorInDB:
        commercial_sensor_db = self._commercial_sensor_repository.find_commercial_sensor_by_uuid(uuid)
        if not commercial_sensor_db:
            raise NotFoundError("Commercial Sensor not found")
        return commercial_sensor_db

    def get_all_commercial_sensors(self) -> List[CommercialSensorOutSlim]:
        return self._commercial_sensor_repository.find_all_commercial_sensors()

    def create_commercial_sensor(self, commercial_sensor: CommercialSensorIn) -> CommercialSensorInDB:
        uuid = uuid4()
        commercial_sensor_db = CommercialSensorInDB(**commercial_sensor.model_dump(), uuid=uuid)
        return self._commercial_sensor_repository.create_commercial_sensor(commercial_sensor_db)

    def update_commercial_sensor(self, uuid: UUID, commercial_sensor: CommercialSensorOutFull) -> CommercialSensorInDB:
        commercial_sensor_db = self._commercial_sensor_repository.find_commercial_sensor_by_uuid(uuid=uuid)
        if not commercial_sensor_db:
            raise NotFoundError("Commercial Sensor not found")
        if commercial_sensor_db.uuid != commercial_sensor.uuid:
            raise ValueError("UUID must not be changed in payload")
        return self._commercial_sensor_repository.update_commercial_sensor(commercial_sensor=commercial_sensor)

    def delete_commercial_sensor(self, uuid: UUID):
        commercial_sensor_db = self._commercial_sensor_repository.find_commercial_sensor_by_uuid(uuid=uuid)
        if not commercial_sensor_db:
            raise NotFoundError("Commercial Sensor not found")
        # TODO Check if project is not used anywhere
        self._commercial_sensor_repository.delete_commercial_sensor(uuid=uuid)