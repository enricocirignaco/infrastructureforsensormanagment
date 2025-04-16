from app.repositories.project_repository import ProjectRepository

class ProjectService:

    def __init__(self, project_repository: ProjectRepository):
        self._project_repository = project_repository