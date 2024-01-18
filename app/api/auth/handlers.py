from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse

from app.shemas.user_shemas import BaseUserShema
from app.api.auth.utils import create_access_token, read_token, get_user, UserAuthData, Token, UserData

auth_router = APIRouter()


@auth_router.post("/login")
def login(user_data: UserAuthData) -> JSONResponse:
    user = get_user(user_data.login, user_data.password)

    res = JSONResponse(
        status_code=status.HTTP_200_OK,
        content=user.model_dump(mode="json")
    )
    res.set_cookie("access_token", create_access_token(user_data), httponly=True, secure=True)

    return res
