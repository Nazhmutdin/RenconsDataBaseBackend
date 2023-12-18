from sqlalchemy import Select, select, desc

from app.models import WelderNDTModel, WelderModel
from app.utils.db_objects import (
    DBResponse,
    WelderNDTDataBaseRequest
)
from app.utils.base_repository import BaseRepository
from app.utils.UoW import SQLalchemyUnitOfWork
from app.shemas import WelderNDTShema


class WelderNDTRepository(BaseRepository[WelderNDTShema, WelderNDTModel]):
    __tablemodel__ = WelderNDTModel
    __shema__ = WelderNDTShema

    def get_many(self, request: WelderNDTDataBaseRequest) -> DBResponse[WelderNDTShema]:

        with SQLalchemyUnitOfWork() as transaction:

            stmt = select(WelderNDTModel)\
                .order_by(desc(WelderNDTModel.welding_date))

            filtrated_stmt = self._set_filters(stmt, request)
            count = self.count(filtrated_stmt, transaction.connection)

            filtrated_stmt = filtrated_stmt.limit(request.limit).offset(request.offset)
            res = [WelderNDTShema.model_validate(el) for el in transaction.connection.execute(filtrated_stmt).mappings().all()]

            return DBResponse(
                result=res,
                count=count
            )


    def _set_filters(self, stmt: Select, request: WelderNDTDataBaseRequest) -> Select:
        if request.kleymos:
            stmt = stmt.filter(WelderNDTModel.kleymo.in_(request.kleymos))

        if request.welding_date_before:
            stmt = stmt.filter(WelderNDTModel.welding_date <= request.welding_date_before)

        if request.welding_date_from:
            stmt = stmt.filter(WelderNDTModel.welding_date >= request.welding_date_from)

        return stmt
