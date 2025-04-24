from app.repositories.project_repository import ProjectRepository
from app.models.project import ProjectIn, ProjectInDB, ProjectStateEnum, ProjectOutSlim, ProjectOutFull

from fastapi import HTTPException
from typing import List
from uuid import UUID, uuid4

class ProjectService:

    def __init__(self, project_repository: ProjectRepository):
        self._project_repository = project_repository

    def get_project_by_uuid(self, uuid: UUID) -> ProjectInDB:
        project = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    def get_all_projects(self) -> List[ProjectOutSlim]:
        return self._project_repository.find_all_projects()

    def create_project(self, project: ProjectIn) -> ProjectInDB:
        uuid = uuid4()
        project_db = ProjectInDB(**project.model_dump(), uuid=uuid, state=ProjectStateEnum.ACTIVE)
        return self._project_repository.create_project(project_db)
    
    def update_project(self, uuid: UUID, project: ProjectOutFull) -> ProjectInDB:
        project_db = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project_db:
            raise HTTPException(status_code=404, detail="Project not found")
        if project_db.uuid != project.uuid:
            raise HTTPException(status_code=400, detail="UUID must not be changed in payload")
        return self._project_repository.update_project(uuid=uuid, project=project)

    def delete_project(self, uuid: UUID):
        project = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        # TODO Check if project is not used anywhere
        self._project_repository.delete_project(uuid=uuid)