from app.repositories.sensor_node_repository import SensorNodeRepository
from app.models.sensor_node import SensorNodeDB, TTNKeys, SensorNodeOutSlim, ConfigurableAssignment, TimeseriesData, SensorNodeOutFull, SensorNodeUpdate, SensorNodeCreate, SensorNodeLogbookEntry, SensorNodeLogbookEnum, SensorNodeStateEnum, ConfigurableTypeEnum
from app.models.user import UserInDB, UserOut, RoleEnum
from app.models.node_template import NodeTemplateStateEnum
from app.models.project import ProjectStateEnum
from app.constants import system_defined_configurables
from app.services.project_service import ProjectService
from app.services.node_template_service import NodeTemplateService
from app.services.ttn_service import TTNService
from app.utils.exceptions import NotFoundError
from app.config import settings

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

class SensorNodeService:

    def __init__(self, sensor_node_repository: SensorNodeRepository, 
                 project_service: ProjectService,
                 node_template_service: NodeTemplateService,
                 ttn_service: TTNService):
        self._sensor_node_repository = sensor_node_repository
        self._project_service = project_service
        self._node_template_service = node_template_service
        self._ttn_service = ttn_service
        
    def get_all_sensor_nodes(self, filters: dict = None) -> List[SensorNodeOutSlim]:
        if filters is None:
            filters = {}
        sensor_nodes = self._sensor_node_repository.find_all_sensor_nodes()
        if filters.get("project_uuid"):
            sensor_nodes = [sn for sn in sensor_nodes if sn.project.uuid == filters["project_uuid"]]
        if filters.get("node_template_uuid"):
            sensor_nodes = [sn for sn in sensor_nodes if sn.node_template.uuid == filters["node_template_uuid"]]
        return sensor_nodes
    
    def get_sensor_node_by_uuid(self, uuid: UUID) -> SensorNodeOutFull:
        sensor_node_db = self._sensor_node_repository.find_sensor_node_by_uuid(uuid=uuid)
        if not sensor_node_db:
            raise NotFoundError("Sensor node not found")
        # TODO Replace with actual timeseries data retrieval
        sensor_node_out = SensorNodeOutFull(**sensor_node_db.model_dump(), last_timeseries=TimeseriesData(timestamp=datetime.now(), fields=[]))
        # TODO Based on timeseries data, set the state of the sensor node
        # sensor_node_out.state = SensorNodeStateEnum.ACTIVE if sensor_node_out.last_timeseries.timestamp < .... else SensorNodeStateEnum.INACTIVE
        return sensor_node_out
    
    def create_sensor_node(self, sensor_node: SensorNodeCreate, logged_in_user: UserInDB) -> SensorNodeOutFull:
        # Check if given uuid's exist
        try:
            project = self._project_service.get_project_by_uuid(uuid=sensor_node.project_uuid)
        except NotFoundError:
            raise NotFoundError("No project found with the given uuid")
        try:
            node_template = self._node_template_service.get_node_template_by_uuid(uuid=sensor_node.node_template_uuid)
        except NotFoundError:
            raise NotFoundError("No node template found with the given uuid")
        
        # Check if each configurable is identical to the ones defined in the node template
        user_configs_template = [config.name for config in node_template.configurables if config.type == ConfigurableTypeEnum.USER_DEFINED]
        user_configs_node = [config.name for config in sensor_node.configurables if config.type == ConfigurableTypeEnum.USER_DEFINED]
        if sorted(user_configs_template) != sorted(user_configs_node):
            raise ValueError("The user-defined configurables do not match the ones defined in the node template.")
        
        # Create the sensor node
        uuid = uuid4()
        keys = self._ttn_service.create_device(sensor_node_id=uuid)
        system_configs = [
            ConfigurableAssignment(name="APP_KEY", type=ConfigurableTypeEnum.SYSTEM_DEFINED, value=keys.app_key, display_value=f"[ {keys.app_key} ]"),
            ConfigurableAssignment(name="JOIN_EUI", type=ConfigurableTypeEnum.SYSTEM_DEFINED, value=keys.join_eui, display_value=f"[ {keys.join_eui} ]"),
            ConfigurableAssignment(name="DEV_EUI", type=ConfigurableTypeEnum.SYSTEM_DEFINED, value=keys.dev_eui, display_value=f"[ {keys.dev_eui} ]")
        ]
        user_configs = [config for config in sensor_node.configurables if config.type == ConfigurableTypeEnum.USER_DEFINED]
        configurables = user_configs + system_configs
        
        logbook = [SensorNodeLogbookEntry(type=SensorNodeLogbookEnum.CREATED, date=datetime.now(), user=UserOut(**logged_in_user.model_dump()))]
        ttn_device_link = f"https://eu1.cloud.thethings.network/console/applications/{settings.TTN_APP_ID}/devices/{uuid}"
        sensor_node_db = SensorNodeDB(
            **sensor_node.model_dump(), 
            uuid=uuid,
            state=SensorNodeStateEnum.PREPARED, 
            logbook=logbook,
            ttn_device_link=ttn_device_link)
        sensor_node_db.configurables = configurables
        sensor_node_db = self._sensor_node_repository.create_sensor_node(sensor_node_db)
        
        # Update state of the node template and project if needed
        if node_template.state == NodeTemplateStateEnum.UNUSED:
            self._node_template_service.set_in_use_node_template(node_template.uuid)
        if project.state == ProjectStateEnum.PREPARED:
            self._project_service.set_active_project(project.uuid)
                
        sensor_node_out = SensorNodeOutFull(**sensor_node_db.model_dump(), last_timeseries=None)
        return sensor_node_out
    
    def update_sensor_node(self, uuid: UUID, sensor_node: SensorNodeUpdate, logged_in_user: UserInDB) -> SensorNodeOutFull:
        sensor_node_db = self._sensor_node_repository.find_sensor_node_by_uuid(uuid=uuid)
        if not sensor_node_db:
            raise NotFoundError("Sensor node not found")
        if sensor_node.uuid and sensor_node_db.uuid != sensor_node.uuid:
            raise ValueError("UUID must not be changed in payload")
        
        # If state is still PREPARED, almost all changes should be allowed
        if sensor_node_db.state == SensorNodeStateEnum.PREPARED:
            if sensor_node.state != SensorNodeStateEnum.PREPARED:
                raise ValueError("State of sensor node must not be updated manually")
            # Check if each configurable is identical to the ones defined in the node template
            node_configurables_names = [config.name for config in sensor_node_db.configurables]
            template_configurables_names = [config.name for config in sensor_node.configurables]
            if sorted(node_configurables_names) != sorted(template_configurables_names):
                raise ValueError("The configurables do not match the ones defined in the node template.")
            # check if value of system-defined configurables is not changed
            for config in sensor_node_db.configurables:
                if config.type == ConfigurableTypeEnum.SYSTEM_DEFINED:
                    for config_update in sensor_node.configurables:
                        if config.name == config_update.name and config.value != config_update.value:
                            raise ValueError("The value of system-defined configurables cannot be changed")
            
            sensor_node_update = SensorNodeDB(
                **sensor_node.model_dump(), 
                logbook=sensor_node_db.logbook,
                project_uuid=sensor_node_db.project_uuid,
                node_template_uuid=sensor_node_db.node_template_uuid,
                ttn_device_link=sensor_node_db.ttn_device_link)
            sensor_node_update.logbook.append(
                SensorNodeLogbookEntry(
                    type=SensorNodeLogbookEnum.UPDATED, 
                    date=datetime.now(), 
                    user=UserOut(**logged_in_user.model_dump())
                ))
            return self._sensor_node_repository.update_sensor_node(sensor_node=sensor_node_update)
        
        # TODO Update mechanics when state not PREPARED
        else:
            raise ValueError("Sensor node cannot be updated, it is not in the PREPARED state")
    
    def delete_sensor_node(self, uuid: UUID) -> None:
        sensor_node_db = self._sensor_node_repository.find_sensor_node_by_uuid(uuid=uuid)
        if not sensor_node_db:
            raise NotFoundError("Sensor node not found")
        if sensor_node_db.state != SensorNodeStateEnum.PREPARED:
            raise ValueError("Sensor node cannot be deleted, it is not in the PREPARED state")
        self._sensor_node_repository.delete_sensor_node(uuid=uuid)
        self._ttn_service.delete_device(sensor_node_id=sensor_node_db.uuid)
        
        # Update state of the project back to PREPARED if no other sensor nodes are in the project
        nodes_by_project = self.get_all_sensor_nodes(filters={"project_uuid": sensor_node_db.project_uuid})
        if not nodes_by_project:
            self._project_service.set_prepared_project(sensor_node_db.project_uuid)
        # Update state of the node template back to UNUSED if no other sensor nodes are using it
        nodes_by_template = self.get_all_sensor_nodes(filters={"node_template_uuid": sensor_node_db.node_template_uuid})
        if not nodes_by_template:
            self._node_template_service.set_unused_node_template(sensor_node_db.node_template_uuid)
    
        