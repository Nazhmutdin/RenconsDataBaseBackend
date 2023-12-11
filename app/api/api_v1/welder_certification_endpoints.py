from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.shemas import WelderCertificationShema
from app.repositories import WelderCertificationRepository
from app.utils.db_objects import DBResponse, WelderCertificationDataBaseRequest


class WelderCertificationHTTPRequest(BaseModel):
    kleymos: list[str] = Field(default=[])
    ids: list[str] = Field(default=[])
    certification_numbers: list[str] = Field(default=[], alias="certificationNumbers")
    certification_date_from: date | None = Field(default=None, alias="certificationDateFrom")
    certification_date_before: date | None = Field(default=None, alias="certificationDateBefore")
    expiration_date_from: date | None = Field(default=None, alias="expirationDateFrom")
    expiration_date_before: date | None = Field(default=None, alias="expirationDateBefore")
    expiration_date_fact_from: date | None = Field(default=None, alias="expirationDateFactFrom")
    expiration_date_fact_before: date | None = Field(default=None, alias="expirationDateFactBefore")
    details_thikness_from: float | None = Field(default=None, alias="detailsThiknessFrom")
    details_thikness_before: float | None = Field(default=None, alias="detailsThiknessBefore")
    outer_diameter_from: float | None = Field(default=None, alias="outerDiameterFrom")
    outer_diameter_before: float | None = Field(default=None, alias="outerDiameterBefore")
    rod_diameter_from: float | None = Field(default=None, alias="rodDiameterFrom")
    rod_diameter_before: float | None = Field(default=None, alias="rodDiameterBefore")
    details_diameter_from: float | None = Field(default=None, alias="detailsDiameterFrom")
    details_diameter_before: float | None = Field(default=None, alias="detailsDiameterBefore")


welder_certification_router = APIRouter()


@welder_certification_router.get(path="/{id}")
def get_welder_certification(id: str) -> WelderCertificationShema | None:
    repo = WelderCertificationRepository()

    res = repo.get(id)

    if res != None:
        return res
    
    return {
        "result": res
    }


@welder_certification_router.post(path="/",response_model=DBResponse[WelderCertificationShema])
def get_welders(request: WelderCertificationHTTPRequest = WelderCertificationHTTPRequest(), page: int = 1, page_size: int = 100):
    repo = WelderCertificationRepository()

    if page < 1:
        page = 1
    
    if page_size < 1:
        page_size = 100


    request = WelderCertificationDataBaseRequest(
        **request.model_dump(),
        limit=page_size,
        offset=(page - 1) * page_size
    )

    return repo.get_many(request)
