from fastapi import HTTPException, status

from app.shemas import UserShema
from app.repositories import UserRepository
from app.api.auth.auth_utils import verify_password
from app.utils.db_objects import BaseRequest, WelderRequest, WelderCertificationRequest, WelderNDTRequest


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


def set_limit_offset[Request: BaseRequest](request: Request, page: int, page_size: int):
    if page < 1:
        page = 1
    
    if page_size < 1:
        page_size = 100

    request.limit = page_size
    request.offset = page_size * (page - 1)
    return request


def set_welder_request(request: WelderRequest = WelderRequest(), page: int = 1, page_size: int = 100):

    return set_limit_offset(request, page, page_size)


def set_welder_ndt_request(request: WelderNDTRequest = WelderNDTRequest(), page: int = 1, page_size: int = 100):
        
    return set_limit_offset(request, page, page_size)


def set_welder_certification_request(request: WelderCertificationRequest = WelderCertificationRequest(), page: int = 1, page_size: int = 100):
    
    return set_limit_offset(request, page, page_size)
