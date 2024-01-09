from app.utils.base_repository import BaseRepository
from app.shemas import UserShema
from app.models import UserModel


class UserRepository(BaseRepository[UserShema, UserModel]):
    __tablemodel__ = UserModel
    __shema__ = UserShema
