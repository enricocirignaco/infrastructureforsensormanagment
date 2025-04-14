import os
import secrets
import string
from ..services.auth_service import AuthService
from ..utils.triplestore_client import TripleStoreClient
from ..repositories.user_repository import UserRepository
from ..models.user import UserIn, RoleEnum

def create_init_admin():
    auth_service = _build_auth_service()

    admin_email = os.environ.get("ADMIN_EMAIL", "admin@bfh.ch")
    admin_password = os.environ.get("ADMIN_PASSWORD", _generate_secure_password())

    if not auth_service.find_user_email(admin_email):
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
    else:
        print(f"Admin user with email {admin_email} already exists.")

def _generate_secure_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        # Mindestens 1 Gross-, Kleinbuchstabe, Ziffer und Sonderzeichen
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            return password

def _build_auth_service():
    triplestore = TripleStoreClient(endpoint_url="http://localhost:3030/testing/")
    user_repository = UserRepository(triplestore_client=triplestore)
    auth_service = AuthService(user_repository=user_repository)
    return auth_service