from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash

from app.models.user import UserIn, UserInDB
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
        pw_hash = self._hasher.hash_password(user.password)
        user_db = UserInDB(**user.model_dump(), hashed_password=pw_hash)
        print(user_db)
        return self._user_repository.create_user(user_db)
    