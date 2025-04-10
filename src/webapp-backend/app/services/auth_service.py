from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from uuid import UUID, uuid4
from typing import List
from pydantic import EmailStr

from app.models.user import UserIn, UserInDB, UserPatch, UserLogin, RoleEnum
from app.repositories.user_repository import UserRepository

class AuthService:

    class _PasswordHasher:
        def __init__(self):
            self.ph = PasswordHasher()

        def hash_password(self, plain_password: str) -> str:
            return self.ph.hash(plain_password)

        def verify_password(self, hashed_password: str, plain_password: str) -> bool:
            try:
                return self.ph.verify(hashed_password, plain_password)
            except (VerifyMismatchError, VerificationError, InvalidHash):
                return False
            

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
        self._hasher = self._PasswordHasher()

    def create_user(self, user: UserIn) -> UserInDB:
        uuid = uuid4()
        pw_hash = self._hasher.hash_password(user.password)
        user_db = UserInDB(**user.model_dump(), uuid=uuid, hashed_password=pw_hash, role=RoleEnum.RESEARCHER)
        return self._user_repository.create_user(user_db)
    
    def update_user(self, uuid: UUID, user: UserPatch) -> UserInDB:
        pass
    
    def find_user_uuid(self, uuid: UUID) -> UserInDB:
        print("test")
        return self._user_repository.find_user_by_uuid(uuid)

    def find_user_email(self, email: EmailStr) -> UserInDB:
        return self._user_repository.find_user_by_email(email)
    
    def find_all_users(self) -> List[UserInDB]:
        return self._user_repository.find_all_users()

    def login(self, user: UserLogin):
        user_db = self._user_repository.find_user_by_email(user.email)