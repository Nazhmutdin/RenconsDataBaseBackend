from sqlalchemy import BinaryExpression, Select, select, desc, and_, or_

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
            or_expressions, and_expressions = self._get_many_filtrating(request)

            stmt = select(WelderNDTModel)\
                .order_by(desc(WelderNDTModel.welding_date))\
                .filter(
                    and_(
                        *and_expressions,
                        or_(*or_expressions)
                    )
                )
            
            count = self.count(stmt, transaction.connection)

            stmt = stmt.limit(request.limit).offset(request.offset)
            print(stmt)
            res = [WelderNDTShema.model_validate(el) for el in transaction.connection.execute(stmt).mappings().all()]

            return DBResponse(
                result=res,
                count=count
            )


    def _get_many_filtrating(self, request: WelderNDTDataBaseRequest) -> Select:
        or_expressions: list[BinaryExpression] = []
        and_expressions: list[BinaryExpression] = []

        if request.kleymos:
            or_expressions.append(WelderNDTModel.kleymo.in_(request.kleymos))

        if request.welding_date_before:
            and_expressions.append(WelderNDTModel.welding_date <= request.welding_date_before)

        if request.welding_date_from:
            and_expressions.append(WelderNDTModel.welding_date >= request.welding_date_from)

        if request.status_1_from:
            and_expressions.append(WelderNDTModel.repair_status_1 >= request.status_1_from)

        if request.status_1_before:
            and_expressions.append(WelderNDTModel.repair_status_1 <= request.status_1_before)

        if request.status_2_from:
            and_expressions.append(WelderNDTModel.repair_status_2 >= request.status_2_from)

        if request.status_2_before:
            and_expressions.append(WelderNDTModel.repair_status_2 <= request.status_2_before)

        if request.status_3_from:
            and_expressions.append(WelderNDTModel.repair_status_3 >= request.status_3_from)

        if request.status_3_before:
            and_expressions.append(WelderNDTModel.repair_status_3 <= request.status_3_before)

        return (or_expressions, and_expressions)
