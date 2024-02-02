from datetime import datetime
import typing as t

from pydantic import BaseModel, ConfigDict, Field

from app.utils.base_shema import BaseShema
from app.models import UserModel


class BaseUserShema(BaseShema):
    __table_model__ = UserModel
    login: str = Field(default="")
    name: str = Field(default="")
    email: str | None = Field(default="")
    sign_date: datetime = Field(default=datetime.now())
    update_date: datetime = Field(default=datetime.now())
    login_date: datetime = Field(default=datetime.now())
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False, alias="isSuperUser")

    model_config = ConfigDict(
        populate_by_name=True,
    )

    def set_date_field(self, *fields) -> t.Self:
        for field in fields:
            setattr(self, field, datetime.now())
        
        return self


class UserShema(BaseUserShema):
    hashed_password: str


class CreateUpdateUserShema(BaseUserShema):
    password: str = Field(default="")
    su_login: str = Field(default="")
    su_password: str = Field(default="")


class DeleteUserShema(BaseModel):
    login: str = Field(default="")
    su_login: str = Field(default="")
    su_password: str = Field(default="")
