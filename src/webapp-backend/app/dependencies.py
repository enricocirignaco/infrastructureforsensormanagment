from fastapi import Depends

from .utils.triplestore_client import TripleStoreClient
from .repositories.user_repository import UserRepository
from .services.auth_service import AuthService

# Utils

def get_triplestore_client() -> TripleStoreClient:
    return TripleStoreClient(endpoint_url="http://localhost:3030/testing/sparql")


# Repositories

def get_user_repository(
    triplestore_client: TripleStoreClient = Depends(get_triplestore_client),
) -> UserRepository:
    return UserRepository(triplestore_client)


# Services

def get_auth_service(
        user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository)