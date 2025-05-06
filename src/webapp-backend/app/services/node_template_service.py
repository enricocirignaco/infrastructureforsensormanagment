from app.repositories.node_template_repository import NodeTemplateRepository

class NodeTemplateService:    
    def __init__(self, node_template_repository: NodeTemplateRepository):
        self.node_template_repository = node_template_repository