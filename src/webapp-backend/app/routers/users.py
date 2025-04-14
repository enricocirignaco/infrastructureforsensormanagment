from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List, Annotated
from uuid import UUID

from ..dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.models.user import UserIn, UserOut, UserBase, UserChangePw

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/users",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[UserOut])
async def read_all_users(token: Annotated[str, Depends(oauth2_scheme)], auth_service: AuthService = Depends(get_auth_service)) -> List[UserOut]:
    return auth_service.find_all_users()

@router.get("/{uuid}", response_model=UserOut)
async def read_specific_user(uuid: UUID, auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.find_user_uuid(uuid)

@router.post("/", response_model=UserOut)
async def create_new_user(user: UserIn, auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.create_user(user)

@router.put("/{uuid}", response_model=UserOut)
async def update_specific_user(uuid: UUID, user: UserBase, auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.update_user(uuid, user)

@router.patch("/{uuid}", response_model=UserOut)
async def change_password(uuid: UUID, user: UserChangePw, auth_service: AuthService = Depends(get_auth_service)) -> UserOut:
    return auth_service.change_password(uuid, user)

