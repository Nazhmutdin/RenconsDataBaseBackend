from sqlalchemy import Select, select, desc

from app.models import WelderNDTModel, WelderCertificationModel, WelderModel
from app.db_engine import get_session
from app.utils.db_objects import (
    DBResponse,
    WelderNDTDataBaseRequest
)
from app.utils.base_repository import BaseRepository
from app.shemas import WelderNDTShema


class WelderNDTRepository(BaseRepository[WelderNDTShema, WelderNDTModel]):
    __tablemodel__ = WelderNDTModel
    __shema__ = WelderNDTShema

    def get_many(self, request: WelderNDTDataBaseRequest) -> DBResponse[WelderNDTModel]:
        session = get_session()

        stmt = select(WelderNDTModel, WelderModel.name, WelderCertificationModel.certification_number)\
            .join(WelderNDTModel, WelderNDTModel.kleymo == WelderNDTModel.kleymo)\
            .join(WelderCertificationModel, WelderNDTModel.kleymo == WelderCertificationModel.kleymo)\
            .order_by(desc(WelderNDTModel.latest_welding_date))
        

        filtrated_stmt = self._set_filters(stmt, request)
        res = []

        for el in session.execute(filtrated_stmt).mappings().all():
            ndt_table_dict = el["NDTTable"].__dict__
            ndt_table_dict["full_name"] = el["full_name"]

            res.append(
                WelderNDTShema.model_validate(ndt_table_dict)
            )

        
        return DBResponse(
            result=res,
            count=len(list(session.execute(stmt)))
        )


    def _set_filters(self, stmt: Select, request: WelderNDTDataBaseRequest) -> Select:
        if request.kleymos:
            stmt = stmt.filter(WelderNDTModel.kleymo.in_(request.kleymos))

        if request.comps:
            stmt = stmt.filter(WelderNDTModel.comp.in_(request.comps))

        if request.subcomps:
            stmt = stmt.filter(WelderNDTModel.subcon.in_(request.subcomps))

        if request.projects:
            stmt = stmt.filter(WelderNDTModel.project.in_(request.projects))

        if request.welding_date_before:
            stmt = stmt.filter(WelderNDTModel.latest_welding_date <= request.welding_date_before)

        if request.welding_date_from:
            stmt = stmt.filter(WelderNDTModel.latest_welding_date >= request.welding_date_from)

        if request.names:
            stmt = stmt.filter(WelderModel.name.in_(request.names))

        return stmt
