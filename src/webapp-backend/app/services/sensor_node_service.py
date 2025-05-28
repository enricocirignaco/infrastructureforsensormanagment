from app.repositories.sensor_node_repository import SensorNodeRepository
from app.models.sensor_node import SensorNodeDB, TTNKeys, SensorNodeOutSlim, ConfigurableAssignment, TimeseriesData, SensorNodeOutFull, SensorNodeUpdate, SensorNodeCreate, SensorNodeLogbookEntry, SensorNodeLogbookEnum, SensorNodeStateEnum, ConfigurableTypeEnum
from app.models.user import UserInDB, UserOut, RoleEnum
from app.models.node_template import NodeTemplateStateEnum
from app.models.project import ProjectStateEnum
from app.constants import system_defined_configurables
from app.services.project_service import ProjectService
from app.services.node_template_service import NodeTemplateService
from app.services.ttn.ttn_service_base import TtnServiceBase
from app.utils.exceptions import NotFoundError
from app.config import settings

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from typing import List
from uuid import UUID, uuid4

active_states = {SensorNodeStateEnum.ACTIVE, SensorNodeStateEnum.INACTIVE, SensorNodeStateEnum.IN_USE}

class SensorNodeService:

    def __init__(self, sensor_node_repository: SensorNodeRepository, 
                 project_service: ProjectService,
                 node_template_service: NodeTemplateService,
                 ttn_service: TtnServiceBase):
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

        # TODO this is extremely inefficient, replace with a more sofisticated solution in future
        # This way we can extract if sensor node is active or not
        for node in sensor_nodes:
            if node.state == SensorNodeStateEnum.IN_USE:
                node_detail = self.get_sensor_node_by_uuid(uuid=node.uuid)
                node.state = node_detail.state
        
        return sensor_nodes
    
    def get_sensor_node_by_uuid(self, uuid: UUID) -> SensorNodeOutFull:
        sensor_node_db = self._sensor_node_repository.find_sensor_node_by_uuid(uuid=uuid)
        if not sensor_node_db:
            raise NotFoundError("Sensor node not found")
        
        timeseries = self._sensor_node_repository.find_timeseries_by_sensor_node_uuid(uuid=uuid)
        sensor_node_out = SensorNodeOutFull(
            **sensor_node_db.model_dump(), 
            last_timeseries=timeseries
        )
        
        # Set sensor node to IN_USE state if it has timeseries data for the first time
        if timeseries and sensor_node_out.state == SensorNodeStateEnum.PREPARED:
            self.set_inuse_sensor_node(uuid=uuid)
            # This is only applied temporarily for not load the sensor node again
            sensor_node_out.state = SensorNodeStateEnum.IN_USE
        
        if timeseries and sensor_node_out.state == SensorNodeStateEnum.IN_USE:
            max_interval = timedelta(hours=settings.SENSOR_NODE_MAX_ACTIVE_HOURS)
            now = datetime.now().astimezone()
            if timeseries.timestamp < now - max_interval:
                sensor_node_out.state = SensorNodeStateEnum.INACTIVE
            else:
                sensor_node_out.state = SensorNodeStateEnum.ACTIVE

        return sensor_node_out
    
    async def create_sensor_node(self, sensor_node: SensorNodeCreate, logged_in_user: UserInDB) -> SensorNodeOutFull:
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
        keys = await self._ttn_service.create_device(sensor_node_id=uuid)
        system_configs = [
            ConfigurableAssignment(name="APP_KEY", type=ConfigurableTypeEnum.SYSTEM_DEFINED, display_value=keys.app_key, value=self._to_c_array(keys.app_key)),
            ConfigurableAssignment(name="JOIN_EUI", type=ConfigurableTypeEnum.SYSTEM_DEFINED, display_value=keys.join_eui, value=self._to_c_array(keys.join_eui)),
            ConfigurableAssignment(name="DEV_EUI", type=ConfigurableTypeEnum.SYSTEM_DEFINED, display_value=keys.dev_eui, value=self._to_c_array(keys.dev_eui)),
        ]
        user_configs = [config for config in sensor_node.configurables if config.type == ConfigurableTypeEnum.USER_DEFINED]
        configurables = user_configs + system_configs
        
        logbook = [SensorNodeLogbookEntry(type=SensorNodeLogbookEnum.CREATED, date=datetime.now(), user=UserOut(**logged_in_user.model_dump()))]
        ttn_device_link = self._ttn_service.build_device_link(sensor_node_id=uuid)
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
        elif sensor_node_db.state in active_states and sensor_node.state == SensorNodeStateEnum.ARCHIVED:
            # Archive sensor node that is currently ACTIVE/INACTIVE
            sensor_node_update = SensorNodeDB(**sensor_node_db.model_dump())
            sensor_node_update.state = SensorNodeStateEnum.ARCHIVED
        elif sensor_node_db.state == SensorNodeStateEnum.ARCHIVED and sensor_node.state in active_states:
            # Unarchive sensor node that is currently ARCHIVED
            sensor_node_update = SensorNodeDB(**sensor_node_db.model_dump())
            sensor_node_update.state = SensorNodeStateEnum.IN_USE
        elif (sensor_node_db.state == sensor_node.state == SensorNodeStateEnum.ARCHIVED) or \
            (sensor_node_db.state in active_states and sensor_node.state in active_states):
            if sensor_node_db.description != sensor_node.description:
                # Description is the only field that may be update after prepared state
                sensor_node_update = SensorNodeDB(**sensor_node_db.model_dump())
                sensor_node_update.description = sensor_node.description
            else:
                # Nothing has changed, return the existing sensor node
                return sensor_node_db
        else:
            raise ValueError("Sensor node cannot be updated, it is not in the PREPARED state")
        
        sensor_node_update.logbook.append(
                SensorNodeLogbookEntry(
                    type=SensorNodeLogbookEnum.UPDATED, 
                    date=datetime.now(), 
                    user=UserOut(**logged_in_user.model_dump())
                ))
        
        sensor_node_db = self._sensor_node_repository.update_sensor_node(sensor_node=sensor_node_update)
        return sensor_node_db
        
    def set_inuse_sensor_node(self, uuid: UUID):
        """Used exactly once when a sensor node has first observations"""
        sensor_node_db = self._sensor_node_repository.find_sensor_node_by_uuid(uuid=uuid)
        if not sensor_node_db:
            raise NotFoundError("Sensor node not found")
        if sensor_node_db.state != SensorNodeStateEnum.PREPARED:
            return
        sensor_node_db.state = SensorNodeStateEnum.IN_USE
        self._sensor_node_repository.update_sensor_node(sensor_node=sensor_node_db)

    async def delete_sensor_node(self, uuid: UUID) -> None:
        sensor_node_db = self._sensor_node_repository.find_sensor_node_by_uuid(uuid=uuid)
        if not sensor_node_db:
            raise NotFoundError("Sensor node not found")
        if sensor_node_db.state != SensorNodeStateEnum.PREPARED:
            raise ValueError("Sensor node cannot be deleted, it is not in the PREPARED state")
        self._sensor_node_repository.delete_sensor_node(uuid=uuid)
        await self._ttn_service.delete_device(sensor_node_id=sensor_node_db.uuid)
        
        # Update state of the project back to PREPARED if no other sensor nodes are in the project
        nodes_by_project = self.get_all_sensor_nodes(filters={"project_uuid": sensor_node_db.project_uuid})
        if not nodes_by_project:
            self._project_service.set_prepared_project(sensor_node_db.project_uuid)
        # Update state of the node template back to UNUSED if no other sensor nodes are using it
        nodes_by_template = self.get_all_sensor_nodes(filters={"node_template_uuid": sensor_node_db.node_template_uuid})
        if not nodes_by_template:
            self._node_template_service.set_unused_node_template(sensor_node_db.node_template_uuid)
    
        
    def _to_c_array(self, hex_string: str) -> str:
        if len(hex_string) % 2 != 0:
            raise ValueError("Hex string must have even length")
        
        bytes_list = [f"0x{hex_string[i:i+2]}" for i in range(0, len(hex_string), 2)]
        formatted_bytes = ", ".join(bytes_list)
        return f"{{ {formatted_bytes} }};"
