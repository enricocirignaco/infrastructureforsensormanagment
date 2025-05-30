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
        project_db = ProjectInDB(**project.model_dump(), uuid=uuid, state=ProjectStateEnum.PREPARED, logbook=logbook)
        return self._project_repository.create_project(project_db)
    
    def update_project(self, uuid: UUID, project: ProjectUpdate, logged_in_user: UserInDB) -> ProjectInDB:  
        project_db = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project_db:
            raise NotFoundError("Project not found")
        if project.uuid and project_db.uuid != project.uuid:
            raise ValueError("UUID must not be changed in payload")
        
        if project_db.state == ProjectStateEnum.PREPARED:
            # All modifications are allowed as project is not yet active
            project_update = ProjectInDB(**project.model_dump(), logbook=project_db.logbook)
            project_update.uuid = uuid
        elif project_db.state != ProjectStateEnum.PREPARED and project_db.state == project.state:
            # Update project that is already active or archived but state has not changed
            return project_db
        elif project_db.state == ProjectStateEnum.ACTIVE and project.state == ProjectStateEnum.ARCHIVED:
            # Only state change to archived is allowed when project is active
            project_update = ProjectInDB(**project_db.model_dump())
            project_update.state = ProjectStateEnum.ARCHIVED
        elif project_db.state == ProjectStateEnum.ARCHIVED and project.state == ProjectStateEnum.ACTIVE:
            # Only state change to active is allowed when project is archived
            project_update = ProjectInDB(**project_db.model_dump())
            project_update.state = ProjectStateEnum.ACTIVE
        else:
            raise ValueError("Invalid state transition")
            
        project_update.logbook.append(
            ProjectLogbookEntry(type=ProjectLogbookEnum.UPDATED, 
                                date=datetime.now(), 
                                user=UserOut(**logged_in_user.model_dump())))
        return self._project_repository.update_project(project=project_update)
        

    def set_active_project(self, uuid: UUID):
        """Used when a sensor node ist created in the project"""
        project_db = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project_db:
            raise NotFoundError("Project not found")
        if project_db.state != ProjectStateEnum.PREPARED:
            return
        project_db.state = ProjectStateEnum.ACTIVE
        self._project_repository.update_project(project=project_db)
        
    def set_prepared_project(self, uuid: UUID):
        """Used when all sensor nodes are deleted from an active project"""
        project_db = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project_db:
            raise NotFoundError("Project not found")
        if project_db.state != ProjectStateEnum.ACTIVE:
            return
        project_db.state = ProjectStateEnum.PREPARED
        self._project_repository.update_project(project=project_db)

    def delete_project(self, uuid: UUID):
        project_db = self._project_repository.find_project_by_uuid(uuid=uuid)
        if not project_db:
            raise NotFoundError("Project not found")
        if project_db.state != ProjectStateEnum.PREPARED:
            raise ValueError("Project cannot be deleted, it is not in the PREPARED state")
        self._project_repository.delete_project(uuid=uuid)