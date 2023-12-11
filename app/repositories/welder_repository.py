from sqlalchemy import BinaryExpression, select, and_, or_

from app.models import WelderCertificationModel, WelderModel
from app.utils.db_objects import (
    DBResponse,
    WelderDataBaseRequest
)
from app.utils.UoW import SQLalchemyUnitOfWork
from app.utils.base_repository import BaseRepository
from app.shemas import WelderShema


class WelderRepository(BaseRepository[WelderModel, WelderModel]):
    __tablemodel__ = WelderModel
    __shema__ = WelderShema


    def get_many(self, request: WelderDataBaseRequest) -> DBResponse[WelderModel]:
            
        with SQLalchemyUnitOfWork() as transaction:

            or_expressions, and_expressions = self._get_many_filtrating(request)

            stmt = select(WelderModel).join(
                WelderCertificationModel
            ).filter(
                or_(*or_expressions),
                and_(*and_expressions)
            ).distinct()

            print()

            count = self.count(stmt, transaction.connection)

            if request.limit:
                stmt = stmt.limit(request.limit)
            
            if request.offset:
                stmt = stmt.offset(request.offset)

            welders = [WelderShema.model_validate(welder[0], from_attributes=True) for welder in transaction.session.execute(stmt).all()]

        return DBResponse(
            result=welders,
            count=count
        )


    def _get_many_filtrating(self, request: WelderDataBaseRequest) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
        or_expressions: list[BinaryExpression] = []
        and_expressions: list[BinaryExpression] = []

        if request.names:
            or_expressions.append(WelderModel.name.in_(request.names))

        if request.kleymos:
            or_expressions.append(WelderModel.kleymo.in_(request.kleymos))

        if request.certification_numbers:
            or_expressions.append(WelderCertificationModel.certification_number.in_(request.certification_numbers))

        return (or_expressions, and_expressions)
