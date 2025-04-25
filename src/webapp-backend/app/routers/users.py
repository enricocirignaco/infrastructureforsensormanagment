from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID

from ..dependencies import get_auth_service, require_roles_or_owner
from app.services.auth_service import AuthService
from app.models.user import UserIn, UserOut, UserBase, UserChangePw, UserInDB, RoleEnum, Token

router = APIRouter(
    prefix="/users",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[UserOut])
async def read_all_users(_: UserInDB = Depends(require_roles_or_owner([RoleEnum.ADMIN])),
                         auth_service: AuthService = Depends(get_auth_service)) -> List[UserOut]:
    return auth_service.find_all_users()

@router.get("/{uuid}", response_model=UserOut)
async def read_specific_user(uuid: UUID, 
                             _: UserInDB = Depends(require_roles_or_owner([RoleEnum.ADMIN], check_ownership=True)),
                             auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.find_user_uuid(uuid)

@router.post("/", response_model=UserOut)
async def create_new_user(user: UserIn,
                          _: UserInDB = Depends(require_roles_or_owner([RoleEnum.ADMIN])),
                          auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.create_user(user)

@router.put("/{uuid}", response_model=UserOut)
async def update_specific_user(uuid: UUID,
                               user: UserBase,
                               logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.ADMIN], check_ownership=True)),
                               auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.update_user(uuid, user, logged_in_user)

@router.patch("/{uuid}")
async def change_password(uuid: UUID,
                          user: UserChangePw,
                          logged_in_user: UserInDB = Depends(require_roles_or_owner([RoleEnum.ADMIN], check_ownership=True)),
                          auth_service: AuthService = Depends(get_auth_service)) -> Token:
    return auth_service.change_password(uuid, user, logged_in_user)

