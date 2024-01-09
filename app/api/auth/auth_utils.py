from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from pydantic import BaseModel

from app.repositories import UserRepository
from app.settings import Settings
from app.shemas import UserShema


class UserAuthData(BaseModel):
    login: str
    password: str


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user_repo = UserRepository()

crypt_ctx = CryptContext(["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return crypt_ctx.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return crypt_ctx.verify(password, hashed_password)


def create_access_token(user: UserAuthData) -> str:
    to_encode = user.model_dump(mode="json")

    password = to_encode.pop("password")

    to_encode["hashed_password"] = hash_password(password)

    return jwt.encode(
        to_encode,
        Settings.SECRET_KEY(),
        algorithm=ALGORITHM
    )


def read_token(token: str) -> UserAuthData:
    return UserAuthData(**jwt.decode(token, Settings.SECRET_KEY(), ALGORITHM))


def get_user(login: str, password: str) -> UserShema:
    user = UserRepository().get(login)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user not found"
        )
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid password"
        )
    
    return user