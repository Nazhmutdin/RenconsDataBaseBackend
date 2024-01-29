from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from pydantic import BaseModel, Field, ConfigDict

from app.repositories import UserRepository
from app.settings import Settings


class UserAuthData(BaseModel):
    login: str
    password: str


class TokenData(BaseModel):
    login: str
    password: str


class UserData(BaseModel):
    name: str
    login: str
    email: str | None
    is_superuser: bool = Field(alias="isSuperUser")

    model_config = ConfigDict(
        populate_by_name = True
    )


class Token(BaseModel):
    access_token: str


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user_repo = UserRepository()

crypt_ctx = CryptContext(["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return crypt_ctx.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return crypt_ctx.verify(password, hashed_password)


def create_access_token(user_data: UserAuthData) -> str:
    return jwt.encode(
        {
            "login": user_data.login,
            "password": user_data.password
        },
        Settings.SECRET_KEY(),
        algorithm=ALGORITHM
    )


def read_token(token: Token) -> TokenData:
    return TokenData(**jwt.decode(token.access_token, Settings.SECRET_KEY(), ALGORITHM))


def get_user(login: str, password: str) -> UserData:
    user = UserRepository().get(login)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not found"
        )
    
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid password"
        )
    
    return UserData.model_validate(user, from_attributes=True)
