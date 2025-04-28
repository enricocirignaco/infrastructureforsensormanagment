from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from ..dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.models.user import UserLogin, Token
from app.utils.exceptions import AuthenticationError

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
    except AuthenticationError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
