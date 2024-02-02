from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse, Response

from app.shemas.user_shemas import UserShema, BaseUserShema, DeleteUserShema
from app.repositories import UserRepository
from app.api.auth.utils import create_access_token, UserAuthData
from app.api.auth.dependecies import user_create, user_update, user_delete, get_user_repo, user_login

auth_router = APIRouter()


@auth_router.post("/auth/login")
def login_user(user_data: UserAuthData, user: BaseUserShema = Depends(user_login)) -> JSONResponse:

    res = JSONResponse(
        status_code=status.HTTP_200_OK,
        content=user.model_dump(mode="json")
    )
    res.set_cookie("access_token", create_access_token(user_data), httponly=True, secure=True)

    return res


@auth_router.post("/auth/create-user")
def create_user(user_data: UserShema = Depends(user_create), repo: UserRepository = Depends(get_user_repo)) -> Response:

    repo.add(user_data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "detail": "user has been created"
        }
    )


@auth_router.post("/auth/update-user")
def update_user(user_data: UserShema = Depends(user_update), repo: UserRepository = Depends(get_user_repo)) -> Response:

    repo.update(user_data.login, **user_data.model_dump(exclude_defaults=True))

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "detail": "user has updated"
        }
    )


@auth_router.post("/auth/delete-user")
def delete_user(user_data: DeleteUserShema = Depends(user_delete), repo: UserRepository = Depends(get_user_repo)) -> Response:

    if not repo.get(user_data.login):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user not found"
        )
    
    repo.delete(user_data.login)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "detail": "user has deleted"
        }
    )
