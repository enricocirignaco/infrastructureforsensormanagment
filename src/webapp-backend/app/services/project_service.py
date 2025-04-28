from app.repositories.project_repository import ProjectRepository
from app.models.project import ProjectIn, ProjectInDB, ProjectStateEnum, ProjectOutSlim, ProjectUpdate, ProjectLogbookEntry, ProjectLogbookEnum
from app.models.user import UserInDB, UserOut
from app.utils.exceptions import NotFoundError

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

class ProjectService:

    def __init__(self, project_repository: ProjectRepository):
        self._project_repository = project_repository

    def get_project_by_uuid(self, uuid: UUID) -> ProjectInDB:
        project_db = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project_db:
            raise NotFoundError("Project not found")
        return project_db

    def get_all_projects(self) -> List[ProjectOutSlim]:
        return self._project_repository.find_all_projects()

    def create_project(self, project: ProjectIn, logged_in_user: UserInDB) -> ProjectInDB:
        uuid = uuid4()
        logbook = [ProjectLogbookEntry(type=ProjectLogbookEnum.CREATED, date=datetime.now(), user=UserOut(**logged_in_user.model_dump()))]
        project_db = ProjectInDB(**project.model_dump(), uuid=uuid, state=ProjectStateEnum.ACTIVE, logbook=logbook)
        return self._project_repository.create_project(project_db)
    
    def update_project(self, uuid: UUID, project: ProjectUpdate, logged_in_user: UserInDB) -> ProjectInDB:
        project_db = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project_db:
            raise NotFoundError("Project not found")
        if project.uuid and project_db.uuid != project.uuid:
            raise ValueError("UUID must not be changed in payload")
        project_update = ProjectInDB(**project.model_dump(), logbook=project_db.logbook)
        project_update.uuid = uuid
        project_update.logbook.append(ProjectLogbookEntry(type=ProjectLogbookEnum.UPDATED, date=datetime.now(), user=UserOut(**logged_in_user.model_dump())))
        return self._project_repository.update_project(project=project_update)

    def delete_project(self, uuid: UUID):
        project_db = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project_db:
            raise NotFoundError("Project not found")
        # TODO Check if project is not used anywhere
        self._project_repository.delete_project(uuid=uuid)