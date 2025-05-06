from uuid import UUID, uuid4

from app.repositories.node_template_repository import NodeTemplateRepository
from app.models.node_template import NodeTemplateDB, NodeTemplateUpdate, NodeTemplateCreate, NodeTemplateOutSlim, NodeTemplateOutFull, NodeTemplateLogbookEntry, NodeTemplateLogbookEnum, NodeTemplateStateEnum
from app.utils.exceptions import NotFoundError
from app.models.user import UserInDB, UserOut
from datetime import datetime
from typing import List

class NodeTemplateService:    
    def __init__(self, node_template_repository: NodeTemplateRepository):
        self.node_template_repository = node_template_repository

    def get_node_template_by_uuid(self, uuid: UUID) -> NodeTemplateOutFull:
        node_template_db = self.node_template_repository.find_node_template_by_uuid(uuid)
        if not node_template_db:
            raise NotFoundError("Node Template not found")
        return node_template_db
    
    def get_all_node_templates(self) -> List[NodeTemplateOutSlim]:
        return self.node_template_repository.find_all_node_templates()

    def create_node_template(self, node_template: NodeTemplateCreate, logged_in_user: UserInDB) -> NodeTemplateDB:
        uuid = uuid4()
        logbook = [NodeTemplateLogbookEntry(type=NodeTemplateLogbookEnum.CREATED, date=datetime.now(), user=UserOut(**logged_in_user.model_dump()))]
        node_template_db = NodeTemplateDB(**node_template.model_dump(), uuid=uuid, logbook=logbook, inherited_sensor_nodes=[], state=NodeTemplateStateEnum.UNUSED)
        return self.node_template_repository.create_node_template(node_template_db)

    def update_node_template(self, uuid: UUID, node_template: NodeTemplateUpdate, logged_in_user: UserInDB) -> NodeTemplateDB:
        node_template_db = self.node_template_repository.find_node_template_by_uuid(uuid=uuid)
        if not node_template_db:
            raise NotFoundError("Node Template not found")
        if node_template.uuid and node_template_db.uuid != node_template.uuid:
            raise ValueError("UUID must not be changed in payload")
        node_template_update = NodeTemplateDB(
            **node_template.model_dump(), 
            logbook=node_template_db.logbook, 
            inherited_sensor_nodes=node_template_db.inherited_sensor_nodes, 
            state=node_template_db.state)
        node_template_update.uuid = uuid
        node_template_update.logbook.append(NodeTemplateLogbookEntry(type=NodeTemplateLogbookEnum.UPDATED, date=datetime.now(), user=UserOut(**logged_in_user.model_dump())))
        return self.node_template_repository.update_node_template(node_template=node_template_update)

    def delete_node_template(self, uuid: UUID):
        node_template_db = self.node_template_repository.find_node_template_by_uuid(uuid=uuid)
        if not node_template_db:
            raise NotFoundError("Node Template not found")
        if not node_template_db.inherited_sensor_nodes:
            raise ValueError("Node Template has inherited sensor nodes and cannot be deleted")
        self.node_template_repository.delete_node_template(uuid=uuid)


    def get_protobuf_schema(self, uuid: UUID) -> str:
        # TODO replace with calling external service
        return """
        edition = "2023";
        message Person {
        string name = 1;
        int32 id = 2;
        string email = 3;
        }
        """
    
    def get_protobuf_code(self, uuid: UUID):
        pass