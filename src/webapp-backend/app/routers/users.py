from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

from ..dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.models.user import UserIn, UserOut, UserPatch

router = APIRouter(
    prefix="/users",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[UserOut])
async def read_users(auth_service: AuthService = Depends(get_auth_service)) -> List[UserOut]:
    return auth_service.find_all_users()

@router.get("/{uuid}", response_model=UserOut)
async def read_user(uuid: UUID, auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.find_user_uuid(uuid)

@router.post("/", response_model=UserOut)
async def create_user(user: UserIn, auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.create_user(user)

@router.patch("/{uuid}", response_model=UserOut)
async def update_user(uuid: UUID, user: UserPatch, auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.update_user(uuid, user)