from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from ..dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.models.user import UserLogin, Token

router = APIRouter(
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                auth_service: AuthService = Depends(get_auth_service)) -> Token:
    user_login = UserLogin(email=form_data.username, password=form_data.password)
    try:
        token = auth_service.login(user_login)
    except Exception as e:
        raise e
    return token


# i8mO&/<Mt5r1_u[a