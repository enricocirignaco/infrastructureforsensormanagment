import os
import secrets
from fastapi import HTTPException
from ..services.auth_service import AuthService
from ..utils.triplestore_client import TripleStoreClient
from ..repositories.user_repository import UserRepository
from ..models.user import UserIn, RoleEnum
from ..config import settings

def create_init_admin():
    auth_service = _build_auth_service()

    admin_email = settings.INIT_ADMIN_MAIL
    admin_password = settings.INIT_ADMIN_PW or _generate_secure_password()

    try:
        auth_service.find_user_email(admin_email)
        print(f"Admin user with email {admin_email} already exists.")
    # Service throws 404 if user not found
    except HTTPException as error:
        if(error.status_code == 404):
            admin = UserIn(
                email=admin_email,
                full_name="Init Admin",
                password=admin_password,
                role=RoleEnum.ADMIN
            )
            auth_service.create_user(admin)

            border = "=" * 60
            print(f"\n{border}")
            print("Admin user has been created with the following credentials:")
            print(f"Email:    {admin_email}")
            print(f"Password: {admin_password}")
            print("‼Please store this password securely and change it after first login.")
            print(f"{border}\n")

def _generate_secure_password(length: int = 16) -> str:
    return secrets.token_urlsafe(length)

def _build_auth_service():
    triplestore = TripleStoreClient(endpoint_url=settings.TRIPLESTORE_ENDPOINT)
    user_repository = UserRepository(triplestore_client=triplestore)
    auth_service = AuthService(user_repository=user_repository)
    return auth_service