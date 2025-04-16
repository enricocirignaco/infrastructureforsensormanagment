from typing import List
from uuid import UUID

from app.utils.triplestore_client import TripleStoreClient
from app.models.project import ProjectBase

class ProjectRepository:
    def __init__(self, triplestore_client: TripleStoreClient):
        self.triplestore_client = triplestore_client

    def create_project(self, project: ProjectBase) -> ProjectBase:
        pass

    