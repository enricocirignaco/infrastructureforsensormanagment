from fastapi import Depends, HTTPException, status, Request
from typing import List, Callable

from .models.user import UserInDB
from .utils.triplestore_client import TripleStoreClient
from .repositories.user_repository import UserRepository
from .repositories.project_repository import ProjectRepository
from .services.auth_service import AuthService, oauth2_scheme
from .services.project_service import ProjectService
from .config import settings

# Utils

def get_triplestore_client() -> TripleStoreClient:
    return TripleStoreClient(endpoint_url=settings.TRIPLESTORE_ENDPOINT)


# Repositories

def get_user_repository(
    triplestore_client: TripleStoreClient = Depends(get_triplestore_client),
) -> UserRepository:
    return UserRepository(triplestore_client)

def get_project_repository(
    triplestore_client: TripleStoreClient = Depends(get_triplestore_client),
) -> ProjectRepository:
    return ProjectRepository(triplestore_client)

# Services

def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository)

def get_project_service(
        project_repository: ProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(project_repository)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.get_current_user(token)


# Direct Callables

def require_roles_or_owner(
    allowed_roles: List[str],
    check_ownership: bool = False
) -> Callable:
    async def _check_user(
        request: Request,
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service),
    ) -> UserInDB:
        user = await auth_service.get_current_user(token)

        # Rolle erlaubt?
        if user.role in allowed_roles:
            return user

        # Optionaler Owner-Check
        if check_ownership:
            path_uuid = request.path_params.get("uuid")
            if path_uuid and str(user.uuid) == str(path_uuid):
                return user

        # Kein Zugriff
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return _check_user