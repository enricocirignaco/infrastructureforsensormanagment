from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

from app.models.project import ProjectStateEnum, ProjectBase, ProjectLink, ProjectOut


router = APIRouter(
    prefix="/projects",
    tags=["project"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ProjectOut])
async def read_all_projects() -> List[ProjectOut]:
    pass

@router.get("/{uuid}", response_model=ProjectOut)
async def read_specific_project(uuid: UUID) -> ProjectOut:
    pass

@router.post("/", response_model=ProjectOut)
async def create_new_project(project: ProjectBase) -> ProjectOut:
    pass

@router.put("/{uuid}", response_model=ProjectOut)
async def update_specific_project(uuid: UUID, project: ProjectOut) -> ProjectOut:
    pass

@router.delete("/{uuid}")
async def delete_specific_project(uuid: UUID):
    pass