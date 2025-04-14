from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Annotated
from uuid import UUID

from ..dependencies import get_auth_service
from app.services.auth_service import AuthService
from app.models.user import UserIn, UserOut, UserBase, UserChangePw, UserLogin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    tags=["auth"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthService = Depends(get_auth_service)):
    user_login = UserLogin(email=form_data.username, password=form_data.password)
    try:
        user_db = auth_service.login(user_login)
    except Exception:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"access_token": user_db.email, "token_type": "bearer"}