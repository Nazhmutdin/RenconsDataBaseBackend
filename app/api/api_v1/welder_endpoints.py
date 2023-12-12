from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.shemas import WelderShema
from app.utils.db_objects import DBResponse, WelderDataBaseRequest
from app.repositories import WelderRepository


welder_router = APIRouter()


class WelderHTTPRequest(BaseModel):
    names: list[str] = Field(default=[])
    kleymos: list[str | int] = Field(default=[])
    certification_numbers: list[str] = Field(default=[], alias="certificationNumbers")
    expiration_date_fact_from: date | None = Field(default=None, alias="expirationDateFactFrom")
    expiration_date_fact_before: date | None = Field(default=None, alias="expirationDateFactBefore")
    expiration_date_from: date | None = Field(default=None, alias="expirationDateFrom")
    expiration_date_before: date | None = Field(default=None, alias="expirationDateBefore")
    certification_date_from: date | None = Field(default=None, alias="certificationDateFrom")
    certification_date_before: date | None = Field(default=None, alias="certificationDateBefore")


@welder_router.get(path="/{id}")
def get_welder(id: str | int):
    repo = WelderRepository()

    res = repo.get(id)

    if res != None:
        return res
    
    return {
        "result": res
    }


@welder_router.post(path="/",response_model=DBResponse[WelderShema])
def get_welders(request: WelderHTTPRequest = WelderHTTPRequest(), page: int = 1, page_size: int = 100):
    repo = WelderRepository()

    if page < 1:
        page = 1
    
    if page_size < 1:
        page_size = 100


    request = WelderDataBaseRequest(
        **request.model_dump(),
        limit=page_size,
        offset=(page - 1) * page_size
    )

    return repo.get_many(request)
