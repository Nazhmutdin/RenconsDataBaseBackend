from time import time_ns

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.api.auth.auth_service import create_access_token, read_token, UserAuthData
from app.api.auth.dependecies import get_user

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
    start = time_ns()

    token_data = read_token(token.access_token)
    print(token_data, f"{(time_ns() - start) / 1_000_000_000}s")

    user = get_user(token_data.login, token_data.password)
    print(user, f"{(time_ns() - start) / 1_000_000_000}s")

    return UserData.model_validate(user, from_attributes=True)
