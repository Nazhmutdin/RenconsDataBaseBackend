from fastapi import HTTPException, status

from app.shemas import UserShema
from app.repositories import UserRepository
from app.api.auth.auth_service import verify_password


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
