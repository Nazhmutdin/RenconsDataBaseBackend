from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.repositories import UserRepository
from app.settings import Settings


class UserAuthData(BaseModel):
    login: str
    password: str


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user_repo = UserRepository()

crypt_ctx = CryptContext(["bcrypt"], deprecated="auto", )


def hash_password(password: str) -> str:
    return crypt_ctx.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return crypt_ctx.verify(password, hashed_password)


def create_access_token(user: UserAuthData) -> str:

    return jwt.encode(
        user.model_dump(mode="json"), 
        Settings.SECRET_KEY(), 
        algorithm=ALGORITHM
    )


def read_token(token: str) -> UserAuthData:
    return UserAuthData(**jwt.decode(token, Settings.SECRET_KEY(), ALGORITHM))
