from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
from uuid import UUID, uuid4
from typing import List, Annotated
from pydantic import EmailStr
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models.user import UserIn, UserInDB, UserBase, UserLogin, UserChangePw, Token, RoleEnum
from app.repositories.user_repository import UserRepository

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:

    class _PasswordUtility:
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
        self._hasher = self._PasswordUtility()

    def create_user(self, user: UserIn) -> UserInDB:
        uuid = uuid4()
        pw_hash = self._hasher.hash_password(user.password)
        user_db = UserInDB(**user.model_dump(), uuid=uuid, hashed_password=pw_hash)
        return self._user_repository.create_user(user_db)
    
    def update_user(self, uuid: UUID, user: UserBase) -> UserInDB:
        user_db = self._user_repository.find_user_by_uuid(uuid=uuid)
        if user_db.role != user.role and user_db.role != RoleEnum.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The role can only be changed by an admin user",
            )

        user_new = UserInDB(**user.model_dump(), uuid=uuid, hashed_password=user_db.hashed_password)
        return self._user_repository.update_user(user_new)

    def change_password(self, uuid: UUID, user: UserChangePw) -> Token:
        user_db = self._user_repository.find_user_by_uuid(uuid=uuid)
        if not self._hasher.verify_password(user_db.hashed_password, user.current_password):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Provided password does not equal current password",
            )
        user_db.hashed_password = self._hasher.hash_password(user.new_password)
        user_db = self._user_repository.change_password(user_db)

        access_token = self.create_access_token(user_db)
        return Token(access_token=access_token, token_type="bearer")
    
    def find_user_uuid(self, uuid: UUID) -> UserInDB:
        return self._user_repository.find_user_by_uuid(uuid)

    def find_user_email(self, email: EmailStr) -> UserInDB:
        return self._user_repository.find_user_by_email(email)
    
    def find_all_users(self) -> List[UserInDB]:
        return self._user_repository.find_all_users()
    
    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            uuid = payload.get("sub")
            if uuid is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = self.find_user_uuid(uuid)
        if user is None:
            raise credentials_exception
        return user

    def login(self, user_login: UserLogin) -> Token:
        user_db = self._user_repository.find_user_by_email(user_login.email)

        if not user_db or not self._hasher.verify_password(user_db.hashed_password, user_login.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = self.create_access_token(user_db)
        return Token(access_token=access_token, token_type="bearer")


    def create_access_token(self, user: UserInDB, expires_delta: timedelta | None = None) -> str:
        if expires_delta is None:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {
            "sub": str(user.uuid),
            "role": user.role,
            "email": user.email,
            "full_name": user.full_name,
            "exp": expire,
        }
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
