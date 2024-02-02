import typing as t
from fastapi import HTTPException, status

from app.shemas.user_shemas import CreateUpdateUserShema, UserShema, DeleteUserShema, BaseUserShema
from app.api.auth.utils import hash_password, check_user_in_db, get_user, UserAuthData
from app.api.auth._types import UserValidationExeptionsOptions
from app.errs import UserNotFoundError, InvalidPasswordError
from app.repositories import UserRepository


def handle_user_validation_exceptions(ex: UserNotFoundError | InvalidPasswordError, **kwargs: t.Unpack[UserValidationExeptionsOptions]) -> t.NoReturn:
    if isinstance(ex, UserNotFoundError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=kwargs["user_not_found_text"]
        )

    if isinstance(ex, InvalidPasswordError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=kwargs["invalid_password_text"]
        )


def user_login(user_data: UserAuthData) -> BaseUserShema:
    try:
        user = get_user(user_data.login, user_data.password)
    except (UserNotFoundError, InvalidPasswordError) as e:
        handle_user_validation_exceptions(
            e, 
            user_not_found_text="user not found",
            invalid_password_text="invalid password"
        )
        
    return BaseUserShema.model_validate(user).set_date_field("login_date")


def user_create(user_data: CreateUpdateUserShema) -> UserShema:
    try:
        get_user(user_data.su_login, user_data.su_password)
    except (UserNotFoundError, InvalidPasswordError) as e:
        handle_user_validation_exceptions(
            e, 
            user_not_found_text="super user not found",
            invalid_password_text="invalid password"
        )

    if not user_data.login or not user_data.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="password and login is required"
        )
    
    if check_user_in_db(user_data.login):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user with this login already exists"
        )
    
    return UserShema.model_validate(user_data.model_dump() | {"hashed_password": hash_password(user_data.password)})


def user_update(user_data: CreateUpdateUserShema) -> UserShema:
    try:
        get_user(user_data.su_login, user_data.su_password)
    except (UserNotFoundError, InvalidPasswordError) as e:
        handle_user_validation_exceptions(
            e, 
            user_not_found_text="super user not found",
            invalid_password_text="invalid password"
        )
        
    if not user_data.login:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="login is required"
        )
    

    if user_data.password:
        return UserShema.model_validate(user_data.model_dump() | {"hashed_password": hash_password(user_data.password)})
    
    return UserShema.model_validate(user_data).set_date_field("update_date")


def user_delete(user_data: DeleteUserShema) -> DeleteUserShema:
    try:
        get_user(user_data.su_login, user_data.su_password)
    except (UserNotFoundError, InvalidPasswordError) as e:
        handle_user_validation_exceptions(
            e, 
            user_not_found_text="super user not found",
            invalid_password_text="invalid password"
        )
    
    return user_data

def get_user_repo() -> UserRepository:
    return UserRepository()
