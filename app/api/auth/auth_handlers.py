from time import time_ns

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.api.auth.auth_utils import create_access_token, read_token, get_user, UserAuthData

auth_router = APIRouter()


class UserData(BaseModel):
    name: str = Field()
    email: str | None = Field()


class Token(BaseModel):
    access_token: str


@auth_router.post("/login")
def login(user_data: UserAuthData) -> dict[str, str]:

    return {"access_token": create_access_token(user_data)}


@auth_router.post("/me")
def me(token: Token) -> UserData:

    token_data = read_token(token.access_token)

    user = get_user(token_data.login, token_data.password)

    return UserData.model_validate(user, from_attributes=True)
