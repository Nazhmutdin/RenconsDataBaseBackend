from sqlalchemy import BinaryExpression, select, and_, or_, any_
from sqlalchemy.orm import subqueryload

from app.models import WelderCertificationModel, WelderModel
from app.utils.db_objects import (
    DBResponse,
    WelderDataBaseRequest
)
from app.utils.UoW import SQLalchemyUnitOfWork
from app.utils.base_repository import BaseRepository
from app.shemas import WelderShema


class WelderRepository(BaseRepository[WelderShema, WelderModel]):
    __tablemodel__ = WelderModel
    __shema__ = WelderShema


    def get_many(self, request: WelderDataBaseRequest) -> DBResponse[WelderShema]:
            
        with SQLalchemyUnitOfWork() as transaction:

            or_expressions, and_expressions = self._get_many_filtrating(request)

            stmt = select(WelderModel).join(
                WelderCertificationModel
            ).filter(
                and_(
                    *and_expressions,
                    or_(*or_expressions)
                )
            ).distinct()

            print(stmt)

            count = self.count(stmt, transaction.connection)

            stmt = stmt.limit(request.limit).offset(request.offset)

            welders = [WelderShema.model_validate(welder, from_attributes=True) for welder in transaction.connection.execute(stmt).all()]

            return DBResponse(
                result=welders,
                count=count
            )


    def _get_many_filtrating(self, request: WelderDataBaseRequest) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
        or_expressions: list[BinaryExpression] = []
        and_expressions: list[BinaryExpression] = []

        if request.names:
            names = [f"%{name}%" for name in request.names]
            or_expressions.append(WelderModel.name.ilike(any_(names)))

        if request.kleymos:
            or_expressions.append(WelderModel.kleymo.in_(request.kleymos))

        if request.status:
            or_expressions.append(WelderModel.status == request.status)

        if request.certification_numbers:
            or_expressions.append(WelderCertificationModel.certification_number.in_(request.certification_numbers))

        if request.expiration_date_fact_from:
            and_expressions.append(WelderCertificationModel.expiration_date_fact > request.expiration_date_fact_from)

        if request.expiration_date_fact_before:
            and_expressions.append(WelderCertificationModel.expiration_date_fact < request.expiration_date_fact_before)
            
        if request.expiration_date_from:
            and_expressions.append(WelderCertificationModel.expiration_date > request.expiration_date_from)

        if request.expiration_date_before:
            and_expressions.append(WelderCertificationModel.expiration_date < request.expiration_date_before)
            
        if request.certification_date_from:
            and_expressions.append(WelderCertificationModel.certification_date > request.certification_date_from)

        if request.certification_date_before:
            and_expressions.append(WelderCertificationModel.certification_date < request.certification_date_before)

        return (or_expressions, and_expressions)
