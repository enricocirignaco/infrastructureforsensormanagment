from uuid import UUID, uuid4
import re
import httpx

from app.repositories.node_template_repository import NodeTemplateRepository
from app.models.node_template import NodeTemplateDB, NodeTemplateUpdate, NodeTemplateCreate, ConfigurableDefinition, ConfigurableTypeEnum, NodeTemplateOutSlim, NodeTemplateOutFull, NodeTemplateLogbookEntry, NodeTemplateLogbookEnum, NodeTemplateStateEnum, ProtobufSchema, ProtobufSchemaField
from app.utils.exceptions import NotFoundError, ExternalServiceError
from app.constants import system_defined_configurables
from app.models.user import UserInDB, UserOut
from app.config import settings
from datetime import datetime
from typing import List

class NodeTemplateService:    
    def __init__(self, node_template_repository: NodeTemplateRepository):
        self.node_template_repository = node_template_repository
        self.protobuf_service_base_url = settings.PROTOBUF_SERVICE_BASE_URL

    def get_node_template_by_uuid(self, uuid: UUID) -> NodeTemplateOutFull:
        node_template_db = self.node_template_repository.find_node_template_by_uuid(uuid)
        if not node_template_db:
            raise NotFoundError("Node Template not found")
        return node_template_db
    
    def get_all_node_templates(self) -> List[NodeTemplateOutSlim]:
        return self.node_template_repository.find_all_node_templates()

    async def create_node_template(self, node_template: NodeTemplateCreate, logged_in_user: UserInDB) -> NodeTemplateDB:
        field_names = [field.field_name for field in node_template.fields]
        if len(field_names) != len(set(field_names)):
            raise ValueError("Field names must be unique")

        uuid = uuid4()
        logbook = [NodeTemplateLogbookEntry(
            type=NodeTemplateLogbookEnum.CREATED, 
            date=datetime.now(), 
            user=UserOut(**logged_in_user.model_dump()))
        ]
        node_template_db = NodeTemplateDB(
            **node_template.model_dump(), 
            uuid=uuid, 
            logbook=logbook,
            state=NodeTemplateStateEnum.UNUSED,
            protobuf_message_name=f"Msg_{uuid.hex}"
        )
        for config in system_defined_configurables:
            node_template_db.configurables.append(
                ConfigurableDefinition(
                    name=config,
                    type=ConfigurableTypeEnum.SYSTEM_DEFINED
                )
            )
        node_template_db = self.node_template_repository.create_node_template(node_template_db)
        
        await self._update_protobuf_schema()
        
        return node_template_db

    def update_node_template(self, uuid: UUID, node_template: NodeTemplateUpdate, logged_in_user: UserInDB) -> NodeTemplateDB:
        node_template_db = self.node_template_repository.find_node_template_by_uuid(uuid=uuid)
        if not node_template_db:
            raise NotFoundError("Node Template not found")
        if node_template.uuid and node_template_db.uuid != node_template.uuid:
            raise ValueError("UUID must not be changed in payload")
        
        # Check if any of the system-defined configurables have been changed
        existing_system_defined = {
            config.name for config in node_template_db.configurables
            if config.type == ConfigurableTypeEnum.SYSTEM_DEFINED
        }
        updated_system_defined = {
            config.name for config in node_template.configurables
            if config.type == ConfigurableTypeEnum.SYSTEM_DEFINED
        }
        if existing_system_defined != updated_system_defined:
            raise ValueError("System-defined configurables cannot be modified or removed")

        if node_template_db.state == NodeTemplateStateEnum.UNUSED and node_template.state == NodeTemplateStateEnum.UNUSED:
            # Update node template that is currently unused
            node_template_update = NodeTemplateDB(
                **node_template.model_dump(), 
                logbook=node_template_db.logbook)
        elif node_template_db.state != NodeTemplateStateEnum.UNUSED and node_template_db.state == node_template.state:
            # Update node template that is currently in use or archived but state is not changed
            return node_template_db
        elif node_template_db.state == NodeTemplateStateEnum.IN_USE and node_template.state == NodeTemplateStateEnum.ARCHIVED:
            # Archive node template that is currently in use
            node_template_update = NodeTemplateDB(**node_template_db.model_dump())
            node_template_update.state = NodeTemplateStateEnum.ARCHIVED
        elif node_template_db.state == NodeTemplateStateEnum.ARCHIVED and node_template.state == NodeTemplateStateEnum.IN_USE:
            # Unarchive node template that is currently archived
            node_template_update = NodeTemplateDB(**node_template_db.model_dump())
            node_template_update.state = NodeTemplateStateEnum.IN_USE
        else:
            raise ValueError("Invalid state transition")

        # Append new logbook entry no matter the state transition
        node_template_update.logbook.append(
            NodeTemplateLogbookEntry(type=NodeTemplateLogbookEnum.UPDATED, 
                                     date=datetime.now(), 
                                     user=UserOut(**logged_in_user.model_dump())))
        
        return self.node_template_repository.update_node_template(node_template=node_template_update)
    
    def set_in_use_node_template(self, uuid: UUID):
        """Used when a sensor node is created from the node template"""
        node_template_db = self.node_template_repository.find_node_template_by_uuid(uuid=uuid)
        if not node_template_db:
            raise NotFoundError("Node Template not found")
        if node_template_db.state != NodeTemplateStateEnum.UNUSED:
            return
        node_template_db.state = NodeTemplateStateEnum.IN_USE
        self.node_template_repository.update_node_template(node_template=node_template_db)
        
    def set_unused_node_template(self, uuid: UUID):
        """Used when no sensor node is using the node template anymore"""
        node_template_db = self.node_template_repository.find_node_template_by_uuid(uuid=uuid)
        if not node_template_db:
            raise NotFoundError("Node Template not found")
        if node_template_db.state != NodeTemplateStateEnum.IN_USE:
            return
        node_template_db.state = NodeTemplateStateEnum.UNUSED
        self.node_template_repository.update_node_template(node_template=node_template_db)

    def delete_node_template(self, uuid: UUID):
        node_template_db = self.node_template_repository.find_node_template_by_uuid(uuid=uuid)
        if not node_template_db:
            raise NotFoundError("Node Template not found")
        if node_template_db.state != NodeTemplateStateEnum.UNUSED:
            raise ValueError("Only unused node templates can be deleted")
        self.node_template_repository.delete_node_template(uuid=uuid)


    async def get_protobuf_schema(self, uuid: UUID) -> str:
        protobuf_schema = self.node_template_repository.find_protobuf_schema_by_uuid(uuid).model_dump()
        
        url = f"{self.protobuf_service_base_url}/protobuf/schema"
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/plain"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=url, json=protobuf_schema, headers=headers)
                if response.is_success:
                    print(response.text)
                    return response.text
                else:
                    raise ExternalServiceError(f"Protobuf service returned error: {response.status_code} - {response.text}")
                
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Request to protobuf service failed: {e}")
    
    def get_protobuf_code(self, uuid: UUID):
        pass
    
    async def _update_protobuf_schema(self) -> bytes:
        protobuf_schemas = self.node_template_repository.find_all_protobuf_schemas()
        protobuf_schemas_json = [schema.model_dump() for schema in protobuf_schemas]
        
        url = f"{self.protobuf_service_base_url}/protobuf/descriptor-file"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/octet-stream"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=url, json=protobuf_schemas_json, headers=headers)
                
                if response.is_success:
                    octet_stream = response.content
                    print(octet_stream)
                else:
                    raise ExternalServiceError(f"Protobuf service returned error: {response.status_code} - {response.text}")
                
        except httpx.RequestError as e:
            raise ExternalServiceError(f"Request to protobuf service failed: {e}")
        