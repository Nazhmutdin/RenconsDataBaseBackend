from datetime import datetime

from pydantic import Field

from app.utils.base_shema import BaseShema
from app.models import UserModel


class BaseUserShema(BaseShema):
    __table_model__ = UserModel
    name: str
    login: str
    email: str | None
    sign_date: datetime
    update_date: datetime
    login_date: datetime
    is_active: bool
    is_superuser: bool


class UserShema(BaseUserShema):
    hashed_password: str


class CreateUserShema(BaseUserShema):
    password: str


class DeleteUserShema(BaseShema):
    login: str
    admin_login: str
    admin_password: str
